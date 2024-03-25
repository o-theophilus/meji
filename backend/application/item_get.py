from flask import Blueprint, jsonify, request
from .tools import token_to_user, item_schema
from math import ceil
from .advert import get_all_advert
import re
from .postgres import db_close, db_open
from datetime import datetime
from uuid import uuid4

bp = Blueprint("item_get", __name__)


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
def get(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    cur.execute("""
        SELECT item.*,
            CASE
                WHEN COUNT(feedback.*) = 0 THEN ARRAY[]::integer[]
                ELSE ARRAY_AGG(feedback.rating)
            END AS ratings
        FROM item
        LEFT JOIN feedback ON item.key = feedback.item_key
        WHERE item.slug = %s or item.key = %s
        GROUP BY item.key;
    """, (key, key))
    item = cur.fetchone()

    if not item:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if (
        item["status"] != "live"
        and "item:add" not in user["roles"]
        and "item:edit_status" not in user["roles"]
    ):
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute("""
        INSERT INTO log (
            key, date, user_key, action, entity_key, entity_type
        ) VALUES (%s, %s, %s, %s, %s, %s);
    """, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "viewed",
        item["key"],
        "item"
    ))

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "item": item_schema(item)
    })


@bp.get("/shop")
def shop(
    status="live",
    search="",
    tag="",
    sort="latest",
    page_no=1,
    page_size=24
):
    con, cur = db_open()
    user = token_to_user(cur)

    if (
        "status" in request.args and user and (
            "item:edit_status" in user["roles"]
            or "item:add" in user["roles"]
        )
    ):
        status = request.args["status"]
    if "search" in request.args:
        search = request.args["search"]
    if "tag" in request.args:
        tag = request.args["tag"]
    if "sort" in request.args:
        sort = request.args["sort"]
    if "page_no" in request.args:
        page_no = int(request.args["page_no"])
    if "page_size" in request.args:
        page_size = int(request.args["page_size"])

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
        query = "AND ARRAY[%s] && item.tags"
        if multiply:
            query = "AND ARRAY[%s] @> item.tags"

    cur.execute("""
        SELECT
            item.*,
            CASE
                WHEN item.old_price = 0 THEN 0
                ELSE (100 * (item.old_price - item.price)) / item.old_price
            END AS discount,
            CASE
                WHEN COUNT(feedback.*) = 0 THEN 0
                ELSE SUM(feedback.rating) / COUNT(feedback.*)
            END AS rating,
            ARRAY_AGG(feedback.rating) AS ratings,
            COUNT(*) OVER() AS total_items
        FROM item
        LEFT JOIN feedback ON item.key = feedback.item_key
        LEFT JOIN log ON item.key = log.entity_key
            AND log.action = 'created'
            AND log.entity_type = 'item'
        WHERE
            item.status = %s
            AND (%s IS NULL OR item.name ILIKE %s) {}
        GROUP BY item.key, log.date
        ORDER BY {} {}
        LIMIT %s OFFSET %s;
    """.format(
        query,
        order_by[sort], order_dir[sort]
    ), (
        status,
        f"%{search}%", f"%{search}%",
        page_size, (page_no - 1) * page_size
    ))
    items = cur.fetchall()

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "items": [item_schema(x) for x in items],
        "total_page": ceil(items[0]["total_items"] / page_size) if items else 0
    })


@bp.get("/home")
def home():
    return jsonify({
        "status": 200,
        "tags": all_tags().json["tags"],
        "new_arrivals": shop(sort="latest", page_size=8).json["items"],
        "offers": shop(sort="discount", page_size=8).json["items"],
        "adverts": get_all_advert("home_1").json["adverts"]
    })


@bp.get("/recently_viewed/<user_key>/<item_key>")
def recently_viewed(user_key, item_key):
    con, cur = db_open()

    cur.execute("""
        SELECT *
        FROM (
            SELECT
                DISTINCT ON (item.key) item.*,
                log.date AS date,
                CASE
                    WHEN COUNT(feedback.*) = 0 THEN ARRAY[]::integer[]
                    ELSE ARRAY_AGG(feedback.rating)
                END AS ratings
            FROM item
            LEFT JOIN log ON
                item.key = log.entity_key
                AND item.status = 'live'
            LEFT JOIN feedback ON item.key = feedback.item_key
            WHERE
                log.user_key = %s
                AND log.action = 'viewed'
                AND log.entity_type = 'item'
                AND log.entity_key != %s
            GROUP BY item.key, log.date
            ORDER BY item.key DESC
        ) as x
        ORDER BY x.date DESC
        LIMIT 8 OFFSET 0
        ;
    """, (user_key, item_key))
    items = cur.fetchall()

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "items": [item_schema(x) for x in items]
    })


@bp.get("/similar_items/<item_key>")
def similar_items(item_key):
    con, cur = db_open()

    cur.execute("""
        SELECT *
        FROM item
        WHERE key = %s OR slug = %s
    """, (item_key, item_key))
    item = cur.fetchone()

    if not item:
        return jsonify({
            "status": 200,
            "items": []
        })

    item_keywords = list(set(
        item["tags"] + re.split(r'\s+', item["name"].lower())))

    cur.execute("""
        SELECT item.*,
            CASE
                WHEN COUNT(feedback.*) = 0 THEN ARRAY[]::integer[]
                ELSE ARRAY_AGG(feedback.rating)
            END AS ratings,
            (
                SELECT COUNT(*)
                FROM unnest(tags || STRING_TO_ARRAY(name, ' ')) AS tag_or_name
                WHERE tag_or_name = ANY(%s)
            ) AS likeness
        FROM item
        LEFT JOIN feedback ON item.key = feedback.item_key
        WHERE item.status = 'live' AND item.key != %s
        GROUP BY item.key
        ORDER BY likeness DESC
        LIMIT 8 OFFSET 0;
    """, (item_keywords, item["key"]))
    items = cur.fetchall()

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "items": [item_schema(x) for x in items]
    })


@bp.get("/customer_view/<user_key>/<item_key>")
def customer_view(user_key, item_key):
    con, cur = db_open()

    cur.execute("""
        SELECT
            item.*,
            log.user_key AS user_key,
            CASE
                WHEN COUNT(feedback.*) = 0 THEN ARRAY[]::integer[]
                ELSE ARRAY_AGG(feedback.rating)
            END AS ratings
        FROM item
        LEFT JOIN log ON item.key = log.entity_key
        LEFT JOIN feedback ON item.key = feedback.item_key
        WHERE
            log.entity_type = 'item'
            AND log.action = 'viewed'
            AND log.user_key != %s
            AND item.status = 'live'
        GROUP BY item.key, log.user_key, log.date
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

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "items": [item_schema(x["item"]) for x in item_count]
    })

    # TODO: "You may also like",
