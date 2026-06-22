
from flask import Blueprint, request

from .order.get import order_status
from .postgres import db_close, db_open
from .tools import get_session

bp = Blueprint("admin_dashboard", __name__)


def new_users(cur, interval):
    cur.execute(f"""
        WITH revenue AS (
            SELECT
                SUM(
                    CASE
                        WHEN log.date_created
                            >= NOW() - INTERVAL '{interval}'
                        THEN 1
                    END
                ) AS value,

                SUM(
                    CASE
                        WHEN log.date_created
                            >= NOW() - INTERVAL '{interval}' * 2
                        AND log.date_created
                            < NOW() - INTERVAL '{interval}'
                        THEN 1
                    END
                ) AS prev_value
            FROM log
            WHERE log.entity_type = 'user'
            AND log.action = 'signedup'
        )

        SELECT
            COALESCE(value, 0) AS value,

            CASE
                WHEN prev_value = 0 AND value > 0 THEN 100
                WHEN prev_value = 0 AND value = 0 THEN 0
                ELSE ROUND(((value - prev_value) * 100.0) / prev_value, 0)
            END AS change

        FROM revenue;
    """)
    return cur.fetchone()


def top_users(cur):
    cur.execute("""
        SELECT
            u.username,
            u.name,
            COUNT(o.key) AS orders,
            SUM(o.order_cost + o.delivery_cost) AS spent
        FROM "order" o
        LEFT JOIN "user" u ON o.user_key = u.key
        WHERE o.status NOT IN ('cart','canceled','returning','returned')
        GROUP BY u.key, u.username, u.name
        ORDER BY spent DESC
        LIMIT 5;
    """)
    return cur.fetchall()


def sales_chart(cur, interval):
    cur.execute(f"""
        SELECT
            date_trunc(
                CASE
                    WHEN '{interval}' IN ('24 hours','today') THEN 'hour'
                    WHEN '{interval}' = '7days' THEN 'day'
                    ELSE 'month'
                END,
                (o.timeline->>'created')::timestamp
            ) AS period,

            SUM(o.order_cost + o.delivery_cost) AS value

        FROM "order" o
        WHERE o.status NOT IN ('cart','canceled','returned')
        AND (o.timeline->>'created')::timestamp
            >= NOW() - INTERVAL '{interval}'

        GROUP BY period
        ORDER BY period;
    """)

    rows = cur.fetchall()

    return [
        {
            "label": r["period"].strftime("%b") if interval == "1 month"
            else r["period"].strftime("%d %b")
            if interval == "7 days"
            else r["period"].strftime("%H:%M"),
            "value": r["value"]
        }
        for r in rows
    ]


def order_count(cur, interval):
    cur.execute(f"""
        WITH revenue AS (
            SELECT
                SUM(
                    CASE
                        WHEN (o.timeline->>'created')::timestamp
                            >= NOW() - INTERVAL '{interval}'
                        THEN 1
                    END
                ) AS value,

                SUM(
                    CASE
                        WHEN (o.timeline->>'created')::timestamp
                            >= NOW() - INTERVAL '{interval}' * 2
                        AND (o.timeline->>'created')::timestamp
                            < NOW() - INTERVAL '{interval}'
                        THEN 1
                    END
                ) AS prev_value
            FROM "order" o
            WHERE o.status NOT IN ('cart')
        )

        SELECT
            COALESCE(value, 0) AS value,

            CASE
                WHEN prev_value = 0 AND value > 0 THEN 100
                WHEN prev_value = 0 AND value = 0 THEN 0
                ELSE ROUND(((value - prev_value) * 100.0) / prev_value, 0)
            END AS change

        FROM revenue;
    """)
    return cur.fetchone()


def order_revenue(cur, interval):
    cur.execute(f"""
        WITH revenue AS (
            SELECT
                SUM(
                    CASE
                        WHEN (o.timeline->>'created')::timestamp
                            >= NOW() - INTERVAL '{interval}'
                        THEN o.order_cost + o.delivery_cost
                        ELSE 0
                    END
                ) AS value,

                SUM(
                    CASE
                        WHEN (o.timeline->>'created')::timestamp
                            >= NOW() - INTERVAL '{interval}' * 2
                        AND (o.timeline->>'created')::timestamp
                            < NOW() - INTERVAL '{interval}'
                        THEN o.order_cost + o.delivery_cost
                        ELSE 0
                    END
                ) AS prev_value
            FROM "order" o
            WHERE o.status NOT IN ('cart','canceled','returning','returned')
        )

        SELECT
            COALESCE(value, 0) AS value,

            CASE
                WHEN prev_value = 0 AND value > 0 THEN 100
                WHEN prev_value = 0 AND value = 0 THEN 0
                ELSE ROUND(((value - prev_value) * 100.0) / prev_value, 0)
            END AS change

        FROM revenue;
    """)
    return cur.fetchone()


def order_recent(cur):
    cur.execute("""
        SELECT
            o.key,
            o.status,
            o.payment,
            u.username,
            u.name
        FROM "order" o
        LEFT JOIN "user" u ON o.user_key = u.key
        WHERE o.status != 'cart'
        ORDER BY (o.timeline->>'created')::timestamp DESC
        LIMIT 5;
    """)
    return cur.fetchall()


def order_summary(cur):
    cur.execute("""
        SELECT s.status AS label, COUNT(o.*) AS count
        FROM unnest(%s::text[]) AS s(status)
        LEFT JOIN "order" o ON o.status = s.status
        GROUP BY s.status
        ORDER BY array_position(%s, s.status);
    """, (order_status, order_status))
    return cur.fetchall()


def conversion_rate(cur):
    cur.execute("""
        SELECT
            COUNT(*) FILTER (WHERE o.status = 'cart') AS cart,
            COUNT(*) FILTER (WHERE o.status != 'cart') AS checkout
        FROM "order" o
        LEFT JOIN order_item oi ON o.key = oi.order_key
        WHERE oi.key IS NOT NULL;
    """)
    row = cur.fetchone()
    return [
        {"label": "cart", "count": row["cart"]},
        {"label": "checkout", "count": row["checkout"]}
    ]


def item_available(cur):
    cur.execute("""
        SELECT COUNT(*) AS value
        FROM item
        WHERE status = 'active';
    """)
    return cur.fetchone()


def item_low_quantity(cur):
    cur.execute("""
        SELECT name, slug, quantity
        FROM item
        WHERE quantity < 10
        ORDER BY quantity ASC
        LIMIT 5;
    """)
    return cur.fetchall()


def item_top_purchase(cur, interval):
    cur.execute(f"""
        SELECT
            iv.item_key,
            iv.slug,
            iv.name,
            SUM(oi.quantity) AS units,
            SUM(oi.quantity * iv.price) AS total
        FROM "order" o
        LEFT JOIN order_item oi ON o.key = oi.order_key
        LEFT JOIN item_version iv ON iv.key = oi.item_version_key
        WHERE o.status NOT IN ('cart','canceled','returning','returned')
        AND (o.timeline->>'created')::timestamp
            >= NOW() - INTERVAL '{interval}'
        GROUP BY iv.item_key, iv.name, iv.slug
        ORDER BY units DESC
        LIMIT 10;
    """)
    return cur.fetchall()


# def coupon_usage(cur):
#     cur.execute("""
#         SELECT
#             o.key,
#             o.status,
#             o.order_cost + o.delivery_cost AS total,
#             u.username,
#             u.name
#         FROM coupon
#         LEFT JOIN "user" u ON o.user_key = u.key
#         WHERE o.status != 'cart'
#         ORDER BY (o.timeline->>'created')::timestamp DESC
#         LIMIT 5;
#     """)
#     return cur.fetchall()


def activity_log(cur):
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
                    'key', "user".key,
                    'username', "user".username,
                    'name', "user".name
                ) AS user,

                jsonb_build_object(
                    'slug', COALESCE(usr.username, item.slug, blog.slug,
                        log.entity_key),
                    'type', log.entity_type,
                    'name', COALESCE(usr.name, item.name, blog.title,
                        log.entity_key)
                ) AS entity,

                COUNT(*) OVER() AS _count

            FROM log
            LEFT JOIN "user" ON log.user_key = "user".key
            LEFT JOIN "user" usr ON log.entity_key = usr.key::TEXT
                AND log.entity_type = 'user'
            LEFT JOIN
                item ON log.entity_key = item.key::TEXT
                AND log.entity_type = 'item'
            LEFT JOIN
                blog ON log.entity_key = blog.key::TEXT
                AND log.entity_type = 'blog'

            WHERE NOT (
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
        LIMIT 12;
    """)
    logs = cur.fetchall()

    for x in logs:
        if x["action"] == "viewed user" and x["user_key"] == x["entity_key"]:
            x["action"] = "viewed profile"
            del x["entity"]
        elif x["entity"]["type"] == "page":
            x["action"] = "viewed page"

    return logs


@bp.get("/dashboard")
def dashboard():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return session

    intervals = {
        "today": "1 day",
        "24 hours": "24 hours",
        "7 days": "7 days",
        "1 month": "1 month",
    }

    searchParams = {"interval": "24 hours", }
    interval = request.args.get("interval", searchParams["interval"])

    _new_users = new_users(cur, intervals[interval])
    _top_users = top_users(cur)
    _order_summary = order_summary(cur)
    _conversion_rate = conversion_rate(cur)
    _sales_chart = sales_chart(cur, intervals[interval])
    _order_revenue = order_revenue(cur, intervals[interval])
    _order_count = order_count(cur, intervals[interval])
    _order_recent = order_recent(cur)
    _item_available = item_available(cur)
    _item_low_quantity = item_low_quantity(cur)
    _item_top_purchase = item_top_purchase(cur, intervals[interval])
    _activity_log = activity_log(cur)

    db_close(con, cur)
    return {
        "status": 200,
        "new_users": _new_users,
        "top_users": _top_users,
        "order_summary": _order_summary,
        "conversion_rate": _conversion_rate,
        "sales_chart": _sales_chart,
        "order_revenue": _order_revenue,
        "order_count": _order_count,
        "order_recent": _order_recent,
        "item_available": _item_available,
        "item_low_quantity": _item_low_quantity,
        "item_top_purchase": _item_top_purchase,
        "activity_log": _activity_log,
        "searchParams": searchParams,
        "filters": list(intervals.keys()),
    }, 200
