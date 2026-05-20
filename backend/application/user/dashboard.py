

def order_count(cur, user_key):
    cur.execute("""
        SELECT COUNT(*) AS value
        FROM "order" o
        WHERE o.user_key = %s AND o.status != 'cart';
    """, (user_key,))
    return cur.fetchone()


def last_order_date(cur, user_key):
    cur.execute("""
        SELECT MAX((o.timeline->>'created')::timestamp) AS value
        FROM "order" o
        WHERE o.user_key = %s AND o.status = 'created';
    """, (user_key,))
    return cur.fetchone()


# TODO: collect logs for failed ops
def order_recent(cur, user_key):
    cur.execute("""
        SELECT
            o.key,
            o.status,
            o.payment
        FROM "order" o
        LEFT JOIN "user" u ON o.user_key = u.key
        WHERE o.status != 'cart' AND o.user_key = %s
        ORDER BY (o.timeline->>'created')::timestamp DESC
        LIMIT 6;
    """, (user_key,))
    data = cur.fetchall()
    return data


def give_feedback(cur, user_key):
    cur.execute("""
        SELECT iv.name, iv.slug

        FROM "order" o
        LEFT JOIN order_item oi ON o.key = oi.order_key
        LEFT JOIN item_version iv ON oi.item_version_key = iv.key
        LEFT JOIN item i ON iv.item_key = i.key
        LEFT JOIN comment c ON i.key = c.item_key AND c.user_key = %s
        WHERE o.user_key = %s
            AND o.status = 'delivered'
            AND i.status = 'active'
            AND c.key IS NULL
        ORDER BY (o.timeline->>'delivered')::timestamp DESC
        LIMIT 6;
    """, (user_key, user_key))
    items = cur.fetchall()
    return items


def recently_viewed(cur, user_key):
    cur.execute("""
        SELECT i.name, i.slug, i.price
        FROM (
            SELECT DISTINCT ON (item.key)
                item.*,
                log.date_created AS viewed_at
            FROM log
            JOIN item ON item.key::TEXT = log.entity_key
            WHERE
                item.status = 'active'
                AND log.user_key = %s
                AND log.action = 'viewed item'
                AND log.entity_type = 'item'
            ORDER BY
                item.key,
                log.date_created DESC
        ) i
        ORDER BY viewed_at DESC
        LIMIT 6;
    """, (user_key,))
    return cur.fetchall()


def activity_log(cur, user_key):
    cur.execute("""
        WITH _log AS (
            SELECT
                DISTINCT ON (log.user_key, log.entity_type, log.entity_key)
                log.key,
                log.date_created,
                log.status,
                log.action,
                log.user_key,
                log.entity_key,

                jsonb_build_object(
                    'slug', COALESCE(usr.username, item.slug, blog.slug,
                        log.entity_key),
                    'type', log.entity_type,
                    'name', COALESCE(usr.name, item.name, blog.title,
                        log.entity_key)
                ) AS entity,

                COUNT(*) OVER() AS _count

            FROM log
            LEFT JOIN "user" usr ON log.entity_key = usr.key::TEXT
                AND log.entity_type = 'user'
            LEFT JOIN
                item ON log.entity_key = item.key::TEXT
                AND log.entity_type = 'item'
            LEFT JOIN
                blog ON log.entity_key = blog.key::TEXT
                AND log.entity_type = 'blog'

            WHERE
                log.user_key = %s
                AND NOT (
                    log.entity_type = 'user' AND log.action = 'changed theme'
                )

            ORDER BY
                log.user_key,
                log.entity_type,
                log.entity_key,
                log.date_created DESC
        )

        SELECT * FROM _log
        ORDER BY _log.date_created DESC
        LIMIT 6;
    """, (user_key,))
    logs = cur.fetchall()

    for x in logs:
        if x["action"] == "viewed user" and x["user_key"] == x["entity_key"]:
            x["action"] = "viewed profile"
            del x["entity"]
        elif x["entity"]["type"] == "page":
            x["action"] = "viewed page"

    return logs


def dashboard(cur, user_key):
    _order_count = order_count(cur, user_key)
    _last_order_date = last_order_date(cur, user_key)
    _order_recent = order_recent(cur, user_key)
    _give_feedback = give_feedback(cur, user_key)
    _recently_viewed = recently_viewed(cur, user_key)
    _activity_log = activity_log(cur, user_key)

    return {
        "order_count": _order_count,
        "last_order_date": _last_order_date,
        "order_recent": _order_recent,
        "give_feedback": _give_feedback,
        "recently_viewed": _recently_viewed,
        "activity_log": _activity_log
    }
