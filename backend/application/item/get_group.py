from flask import Blueprint, jsonify
import re
import time
from ..tools import get_session
from .get import item_schema
from ..postgres import db_close, db_open
from .review import get_many


bp = Blueprint("item_get_group", __name__)


def recently_viewed(cur, user_key, item_key):
    cur.execute("""
        SELECT DISTINCT ON (item.key)
            item.*
        FROM log
        JOIN item ON item.key::TEXT = log.entity_key
        WHERE
            item.status = 'active'
            AND log.user_key = %s
            AND log.action = 'viewed'
            AND log.entity_type = 'item'
            AND log.entity_key != %s
        ORDER BY
            item.key,
            log.date_created DESC
        LIMIT 8;
    """, (user_key, item_key))
    items = cur.fetchall()
    return [item_schema(x) for x in items]


def customer_view(cur, user_key, item_key):
    cur.execute("""
        WITH ordered_views AS (
            SELECT
                log.user_key,
                log.entity_key AS current_item,
                LEAD(log.entity_key) OVER (
                    PARTITION BY log.user_key
                    ORDER BY log.date_created
                ) AS next_item
            FROM log
            WHERE
                log.entity_type = 'item'
                AND log.action = 'viewed'
                AND log.user_key != %s
        )
        SELECT
            item.*,
            COUNT(*) AS view_count
        FROM ordered_views ov
        JOIN item ON item.key::TEXT = ov.next_item
        WHERE
            ov.current_item = %s
            AND ov.next_item IS NOT NULL
            AND item.status = 'active'
        GROUP BY item.key
        ORDER BY view_count DESC
        LIMIT 8;
    """, (user_key, item_key))

    items = cur.fetchall()
    return [item_schema(x) for x in items]


def likeness(cur, excluded_item_keys, keywords):
    cur.execute("""
        WITH scored_items AS (
            SELECT item.*,
                COUNT(*) FILTER (WHERE token = ANY(%s)) AS likeness
            FROM item
            CROSS JOIN LATERAL unnest(
                item.tags || string_to_array(lower(item.name), ' ')
            ) AS token
            WHERE
                item.status = 'active'
                AND NOT item.key::TEXT = ANY(%s)
            GROUP BY item.key
        )
        SELECT *
        FROM scored_items
        WHERE likeness > 0
        ORDER BY likeness DESC
        LIMIT 8;
    """, (keywords, excluded_item_keys))

    items = cur.fetchall()
    return [item_schema(x) for x in items]


def similar_items(cur, item_key):
    cur.execute("""
        SELECT * FROM item WHERE key = %s;
    """, (item_key,))
    item = cur.fetchone()
    if not item:
        return []

    keywords = list(set(
        item["tags"] +
        re.split(r'\s+', item["name"].lower())
    ))

    return likeness(cur, [item["key"]], keywords)


def recommended(cur, user_key, item_key=None):
    cur.execute("""
        SELECT item.* FROM item
        JOIN "like" ON item.key = "like".item_key
        WHERE "like".user_key = %s;
    """, (user_key,))
    liked_items = cur.fetchall()

    cur.execute("""
        SELECT item.* FROM item
        JOIN order_item ON item.key = order_item.item_key
        JOIN "order" ON order_item.order_key = "order".key
        WHERE "order".user_key = %s;
    """, (user_key,))
    ordered_items = cur.fetchall()

    keywords = []
    excluded_keys = [item_key] if item_key else []

    for x in liked_items + ordered_items:
        keywords.extend(x["tags"])
        keywords.extend(re.split(r'\s+', x["name"].lower()))
        excluded_keys.append(x["key"])

    if not keywords:
        return []

    return likeness(cur, list(set(excluded_keys)), list(set(keywords)))


@bp.get("/item_group/<item_key>")
def get_group(item_key):
    con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute("""SELECT * FROM item WHERE key = %s;""", (item_key,))
    if not cur.fetchone():
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    a = time.time()
    print("start group")
    _recently_viewed = recently_viewed(cur, user["key"], item_key)
    _similar_items = similar_items(cur, item_key)
    _customer_view = customer_view(cur, user["key"], item_key)
    _recommended = recommended(cur, user["key"], item_key)
    print("end group: ", time.time()-a)

    review = get_many(item_key, 3, cur).json

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "review": review,
        "item_group": [
            {
                "name": "Similar Items",
                "items": _similar_items,
                "style": "grid",
                "open": True
            }, {
                "name": "Recently Viewed",
                "items": _recently_viewed,
                "style": "line",
                "open": True
            }, {
                "name": "Customers who viewed this also viewed",
                "items": _customer_view,
                "style": "line",
                "open": False
            }, {
                "name": "You may also like",
                "items": _recommended,
                "style": "line",
                "open": False
            }
        ]
    })
