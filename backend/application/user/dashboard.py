

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


def order_recent(cur, user_key):
    # TODO: subtract coupon from total
    cur.execute("""
        SELECT
            o.key,
            o.status,
            o.order_cost + o.delivery_cost AS total
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
                AND log.action = 'viewed'
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
        SELECT *
        FROM log
        WHERE user_key = %s
        ORDER BY date_created DESC
        LIMIT 6;
    """, (user_key,))
    data = cur.fetchall()
    return data


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
