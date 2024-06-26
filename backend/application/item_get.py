import time
from flask import Blueprint, jsonify, request
from .tools import token_to_user, item_schema
from math import ceil
import re
from .postgres import db_close, db_open


bp = Blueprint("item_get", __name__)


def recently_viewed(cur, user_key, item_key):
    cur.execute("""
        WITH
            item_sub AS (
                SELECT
                    DISTINCT ON (log.entity_key) log.entity_key AS key,
                    (log.misc->>'price')::float AS old_price,
                    log.date
                FROM log
                LEFT JOIN item ON item.key = log.entity_key
                WHERE
                    log.action = 'edited'
                    AND log.entity_type = 'item'
                    AND (log.misc->>'price')::float > item.price
                ORDER BY log.entity_key, log.date DESC
            ),

            item AS (
                SELECT
                    DISTINCT ON (item.key) item.*,
                    log.date AS date
                FROM item
                LEFT JOIN log ON item.key = log.entity_key
                WHERE
                    item.status = 'live'
                    AND log.user_key = %s
                    AND log.action = 'viewed'
                    AND log.entity_type = 'item'
                    AND log.entity_key != %s
                GROUP BY item.key, log.date
                ORDER BY item.key, log.date DESC
            )

        SELECT
            item.*,
            CASE
                WHEN item.show_discount = 'true' THEN item_sub.old_price
                WHEN item.show_discount = 'false' THEN NULL
                WHEN item_sub.date > item.show_discount::timestamp THEN NULL
                ELSE item_sub.old_price
            END AS old_price,
            COALESCE(ARRAY_AGG(feedback.rating), ARRAY[]::int[]) AS ratings
        FROM item
        LEFT JOIN item_sub ON item.key = item_sub.key
        LEFT JOIN feedback ON item.key = feedback.item_key
        GROUP BY
            item.date, item.key, item.status, item.name, item.slug, item.price,
            item.show_discount, item.information, item.photos, item.tags,
            item.variation, item.available_quantity, item_sub.old_price,
            item_sub.date
        ORDER BY item.date DESC
        LIMIT 8 OFFSET 0
        ;
    """, (user_key, item_key))
    items = cur.fetchall()
    return [item_schema(x) for x in items]


def customer_view(cur, user_key, item_key):
    cur.execute("""
        WITH item_sub AS (
            SELECT
                DISTINCT ON (log.entity_key) log.entity_key AS key,
                (log.misc->>'price')::float AS old_price,
                log.date
            FROM log
            LEFT JOIN item ON item.key = log.entity_key
            WHERE
                log.action = 'edited'
                AND log.entity_type = 'item'
                AND (log.misc->>'price')::float > item.price
            ORDER BY log.entity_key, log.date DESC
        )

        SELECT
            item.*,
            CASE
                WHEN item.show_discount = 'true' THEN item_sub.old_price
                WHEN item.show_discount = 'false' THEN NULL
                WHEN item_sub.date > item.show_discount::timestamp THEN NULL
                ELSE item_sub.old_price
            END AS old_price,
            log.user_key AS user_key,
            COALESCE(ARRAY_AGG(feedback.rating), ARRAY[]::int[]) AS ratings
        FROM item
        LEFT JOIN item_sub ON item.key = item_sub.key
        LEFT JOIN log ON item.key = log.entity_key
        LEFT JOIN feedback ON item.key = feedback.item_key
        WHERE
            log.entity_type = 'item'
            AND log.action = 'viewed'
            AND log.user_key != %s
            AND item.status = 'live'
        GROUP BY
            item.key, log.user_key, log.date, item_sub.old_price, item_sub.date
        ORDER BY log.date ASC;
    """, (user_key,))
    views = cur.fetchall()

    picked_user = []
    picked_items = []
    pick_next_item = []
    items = []
    all_picked_item_keys = []

    for x in views:
        if x["user_key"] not in picked_user:
            if x["key"] == item_key:
                pick_next_item.append(x["user_key"])

            elif x["user_key"] in pick_next_item:
                pick_next_item.remove(x["user_key"])
                picked_user.append(x["user_key"])
                all_picked_item_keys.append(x["key"])

                if x["key"] not in picked_items:
                    items.append(x)
                    picked_items.append(x["key"])

    item_count = []
    for x in items:
        item_count.append({
            "item":  x,
            "count":  all_picked_item_keys.count(x["key"])
        })

    item_count = sorted(item_count, key=lambda d: d["count"], reverse=True)
    return [item_schema(x["item"]) for x in item_count]


def likeness(cur, item_keys, keywords):
    cur.execute("""
        WITH
            likeness AS (
                SELECT
                    item.key,
                    (
                        SELECT COUNT(*)
                        FROM unnest(tags || STRING_TO_ARRAY(name, ' ')) AS tn
                        WHERE tn = ANY(%s)
                    ) AS likeness
                FROM item
            ),

            item_sub AS (
                SELECT
                    DISTINCT ON (log.entity_key) log.entity_key AS key,
                    (log.misc->>'price')::float AS old_price,
                    log.date
                FROM log
                LEFT JOIN item ON item.key = log.entity_key
                WHERE
                    log.action = 'edited'
                    AND log.entity_type = 'item'
                    AND (log.misc->>'price')::float > item.price
                ORDER BY log.entity_key, log.date DESC
            )

        SELECT
            item.*,
            CASE
                WHEN item.show_discount = 'true' THEN item_sub.old_price
                WHEN item.show_discount = 'false' THEN NULL
                WHEN item_sub.date > item.show_discount::timestamp THEN NULL
                ELSE item_sub.old_price
            END AS old_price,
            COALESCE(ARRAY_AGG(feedback.rating), ARRAY[]::int[]) AS ratings,
            likeness.likeness
        FROM item
        LEFT JOIN item_sub ON item.key = item_sub.key
        LEFT JOIN feedback ON item.key = feedback.item_key
        LEFT JOIN likeness ON item.key = likeness.key
        WHERE
            item.status = 'live'
            AND NOT item.key = ANY(%s)
            AND likeness.likeness > 0
        GROUP BY item.key, item_sub.old_price, item_sub.date,
            likeness.likeness
        ORDER BY likeness DESC
        LIMIT 8 OFFSET 0;
    """, (keywords, [x for x in item_keys if x]))
    items = cur.fetchall()
    return [item_schema(x) for x in items]


def similar_items(cur, item_key):
    cur.execute("""
        SELECT *
        FROM item
        WHERE key = %s OR slug = %s
    """, (item_key, item_key))
    item = cur.fetchone()

    if not item:
        return []

    keywords = list(set(
        item["tags"] + re.split(r'\s+', item["name"].lower())))

    return likeness(cur, [item_key], keywords)


def recommended(cur, user_key, item_key=None):
    cur.execute("""
        SELECT item.key, item.name, item.tags
        FROM item
        LEFT JOIN save ON item.key = save.item_key
        WHERE save.user_key = %s;
    """, (user_key,))
    save_items = cur.fetchall()

    cur.execute("""
        SELECT item.key, item.name, item.tags
        FROM item
        LEFT JOIN order_item ON item.key = order_item.item_key
        LEFT JOIN "order" ON order_item.order_key = "order".key
        WHERE "order".user_key = %s;
    """, (user_key,))
    order_items = cur.fetchall()

    item_keys = [item_key]
    keywords = []
    for x in list(save_items) + list(order_items):
        keywords += re.split(r'\s+', x["name"].lower()) + x["tags"]
        item_keys.append(x["key"])

    return likeness(cur, item_keys, keywords)


@bp.get("/item/group/<item_key>/<user_key>")
def get_group(item_key, user_key):
    con, cur = db_open()

    a = time.time()
    print("start group")
    _recently_viewed = recently_viewed(cur, user_key, item_key)
    _similar_items = similar_items(cur, item_key)
    _customer_view = customer_view(cur, user_key, item_key)
    _recommended = recommended(cur, user_key, item_key)
    print("end group: ", time.time()-a)

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "groups": [
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


@bp.get("/tag")
def all_tags():
    con, cur = db_open()

    cur.execute("SELECT tags FROM item WHERE status = 'live';")
    temp = cur.fetchall()

    tags = []
    for x in temp:
        tags += x["tags"]

    tags_count = []
    unique_tags = []
    for x in tags:
        if x not in unique_tags:
            unique_tags.append(x)
            tags_count.append({
                "tag":  x,
                "count":  tags.count(x)
            })

    tags_count = sorted(tags_count, key=lambda d: d["count"], reverse=True)

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "tags": [x["tag"] for x in tags_count]
    })


@bp.get("/item/<key>")
def get_item(key, cur=None):
    aa = time.time()
    print("start get item")

    close_conn = not cur
    if not cur:
        con, cur = db_open()

    cur.execute("""
        WITH item_sub AS (
            SELECT
                DISTINCT ON (log.entity_key) log.entity_key AS key,
                (log.misc->>'price')::float AS old_price,
                log.date
            FROM log
            LEFT JOIN item ON item.key = log.entity_key
            WHERE
                log.action = 'edited'
                AND log.entity_type = 'item'
                AND (log.misc->>'price')::float > item.price
            ORDER BY log.entity_key, log.date DESC
        )

        SELECT
            item.*,
            CASE
                WHEN item.show_discount = 'true' THEN item_sub.old_price
                WHEN item.show_discount = 'false' THEN NULL
                WHEN item_sub.date > item.show_discount::timestamp THEN NULL
                ELSE item_sub.old_price
            END AS old_price,
            COALESCE(ARRAY_AGG(feedback.rating), ARRAY[]::int[]) AS ratings
        FROM item
        LEFT JOIN item_sub ON item.key = item_sub.key
        LEFT JOIN feedback ON item.key = feedback.item_key
        WHERE item.slug = %s OR item.key = %s
        GROUP BY item.key, item_sub.old_price, item_sub.date;
    """, (key, key))
    item = cur.fetchone()

    bb = time.time()
    print("get item 1: ", bb-aa)

    if not item:
        if close_conn:
            db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if close_conn and item["status"] != "live":
        user = token_to_user(cur)
        if not user:
            db_close(con, cur)
            return jsonify({
                "status": 400,
                "error": "invalid token"
            })

        if set([
            "item:add",
            "item:edit_status"
        ]).isdisjoint(user["permissions"]):
            db_close(con, cur)
            return jsonify({
                "status": 400,
                "error": "unauthorized access"
            })

    print("end get item: ", time.time()-bb)

    if close_conn:
        db_close(con, cur)
    return jsonify({
        "status": 200,
        "item": item_schema(item)
    })


@bp.get("/shop")
def shop(order="latest", page_size=24):
    ss = time.time()
    print("start shop")
    con, cur = db_open()
    user = token_to_user(cur)

    status = "live"
    search = ""
    tag = ""
    page_no = 1

    if (
        "status" in request.args and user and (
            "item:edit_status" in user["permissions"]
            or "item:add" in user["permissions"]
        )
    ):
        status = request.args["status"]
    if "search" in request.args:
        search = request.args["search"].strip()
    if "order" in request.args:
        order = request.args["order"]
    if "page_no" in request.args:
        page_no = int(request.args["page_no"])
    if "page_size" in request.args:
        page_size = int(request.args["page_size"])
    if "tag" in request.args:
        tag = request.args["tag"]
    multiply = False
    if tag[-2:] == ":x":
        multiply = True
        tag = tag[:-2]
    tags = tag.split(",")
    tags = [] if not tags[0] else tags

    order_by = {
        'latest': 'log.date',
        'oldest': 'log.date',
        'name (a-z)': 'item.name',
        'name (z-a)': 'item.name',
        'cheap': 'item.price',
        'expensive': 'item.price',
        'discount': 'discount',
        'rating': 'rating'
    }

    order_dir = {
        'latest': 'DESC',
        'oldest': 'ASC',
        'name (a-z)': 'ASC',
        'name (z-a)': 'DESC',
        'cheap': 'ASC',
        'expensive': 'DESC',
        'discount': 'DESC',
        'rating': 'DESC'
    }

    query = ""
    if tags != []:
        query = f"""
            AND cardinality(item.tags) > 0
            AND item.tags {"@>" if multiply else "&&"} ARRAY[{tags}]
        """

    cur.execute("""
        WITH item_sub AS (
            SELECT
                DISTINCT ON (log.entity_key) log.entity_key AS key,
                (log.misc->>'price')::float AS old_price,
                (100 * ((log.misc->>'price')::float - item.price))
                    / (log.misc->>'price')::float AS discount,
                log.date
            FROM log
            LEFT JOIN item ON item.key = log.entity_key
            WHERE
                log.action = 'edited'
                AND log.entity_type = 'item'
                AND (log.misc->>'price')::float > item.price
            ORDER BY log.entity_key, log.date DESC
        )

        SELECT
            item.*,
            CASE
                WHEN item.show_discount = 'true' THEN item_sub.old_price
                WHEN item.show_discount = 'false' THEN NULL
                WHEN item_sub.date > item.show_discount::timestamp THEN NULL
                ELSE item_sub.old_price
            END AS old_price,
            COALESCE(item_sub.discount, 0) AS discount,
            COALESCE(AVG(feedback.rating), 0) AS rating,
            COALESCE(ARRAY_AGG(feedback.rating), ARRAY[]::int[]) AS ratings,
            COUNT(*) OVER() AS total_items
        FROM item
        LEFT JOIN item_sub ON item.key = item_sub.key
        LEFT JOIN feedback ON item.key = feedback.item_key
        LEFT JOIN log ON item.key = log.entity_key
        WHERE
            item.status = %s
            AND (%s = '' OR item.name ILIKE %s) {}
            AND log.action = 'created'
            AND log.entity_type = 'item'
        GROUP BY
            item.key, item.status, item.name, item.slug,
            item.price, item.show_discount, item.information, item.photos,
            item.tags, item.variation, item.available_quantity,
            item_sub.discount, item_sub.old_price, item_sub.date, log.date
        ORDER BY {} {}
        LIMIT %s OFFSET %s;
    """.format(
        query,
        order_by[order], order_dir[order]
    ), (
        status,
        search, f"%{search}%",
        page_size, (page_no - 1) * page_size
    ))
    items = cur.fetchall()

    db_close(con, cur)
    print("end shop: ", time.time() - ss)
    return jsonify({
        "status": 200,
        "items": [item_schema(x) for x in items],
        "order_by": list(order_by.keys()),
        "item_status": ['live', 'draft', 'delete'],
        "total_page": ceil(items[0]["total_items"] / page_size) if items else 0
    })
