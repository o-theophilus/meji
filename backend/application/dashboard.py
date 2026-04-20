import os

from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash

from .log import log
from .order.get import order_status
from .postgres import db_close, db_open
from .tools import access_pass, get_session

bp = Blueprint("admin_dashboard", __name__)


def default_admin(cur):
    email = os.environ["MAIL_USERNAME"]

    cur.execute('SELECT * FROM "user" WHERE email = %s;', (email,))
    if not cur.fetchone():
        cur.execute("""
                INSERT INTO "user"
                (status, name, username, email, password, access)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING *;
            """, (
            "active",
            "Theophilus",
            "omni",
            email,
            generate_password_hash(
                os.environ["MAIL_PASSWORD"], method="scrypt"),
            [f"{x}.{y[0]}" for x in access_pass for y in access_pass[x]]
        ))
        user = cur.fetchone()

        log(
            cur=cur,
            user_key=user["key"],
            action="created",
            entity_type="user",
            entity_key=user["key"]
        )
        log(
            cur=cur,
            user_key=user["key"],
            action="signedup",
            entity_type="user",
            entity_key=user["key"]
        )
        log(
            cur=cur,
            user_key=user["key"],
            action="activated account",
            entity_type="user",
            entity_key=user["key"]
        )


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
        WHERE o.status NOT IN ('cart','canceled','returned')
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
            WHERE o.status NOT IN ('cart', 'canceled', 'returning', 'returned')
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
    # TODO: subtract coupon from total
    cur.execute("""
        SELECT
            o.key,
            o.status,
            o.order_cost + o.delivery_cost AS total,
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
            i.name,
            i.slug,
            SUM(oi.quantity) AS units,
            SUM(oi.quantity * i.price) AS total
        FROM order_item oi
        JOIN "order" o ON o.key = oi.order_key
        JOIN item_version i
            ON i.key = oi.item_key
        WHERE o.status NOT IN ('cart', 'canceled', 'returned')
        AND (o.timeline->>'created')::timestamp
            >= NOW() - INTERVAL '{interval}'
        GROUP BY i.item_key, i.name, i.slug
        ORDER BY units DESC
        LIMIT 10;
    """)
    return cur.fetchall()
    # TODO: JOIN item_version


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


@bp.get("/dashboard")
def dashboard():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    # user = session["user"]

    default_admin(cur)

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
    _sales_chart = sales_chart(cur, intervals[interval])
    _order_revenue = order_revenue(cur, intervals[interval])
    _order_count = order_count(cur, intervals[interval])
    _order_recent = order_recent(cur)
    _item_available = item_available(cur)
    _item_low_quantity = item_low_quantity(cur)
    _item_top_purchase = item_top_purchase(cur, intervals[interval])

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "new_users": _new_users,
        "top_users": _top_users,
        "order_summary": _order_summary,
        "sales_chart": _sales_chart,
        "order_revenue": _order_revenue,
        "order_count": _order_count,
        "order_recent": _order_recent,
        "item_available": _item_available,
        "item_low_quantity": _item_low_quantity,
        "item_top_purchase": _item_top_purchase,
        "searchParams": searchParams,
        "filters": list(intervals.keys()),
    })
