from flask import Blueprint, jsonify, request
from .tools import token_to_user, item_schema
from .log import log_template
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
        SELECT *,
        (
            SELECT ARRAY_AGG(rating)
            FROM feedback
            WHERE feedback.item_key = item.key
        ) AS ratings
        FROM item
        WHERE slug = %s or key = %s;
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

    cur.execute(log_template, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "viewed",
        item["key"],
        "item",
        200,
        None
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

    cur.execute("""
        SELECT
            item.*,
            COUNT(*) OVER() AS total_items,
            COALESCE(
                100 * (item.old_price - item.price) / item.old_price, 0
            ) AS discount,
            CASE
                WHEN COUNT(feedback.*) = 0 THEN NULL
                ELSE SUM(feedback.rating) / COUNT(feedback.*)
            END AS rating,
            ARRAY_AGG(feedback.rating) AS ratings
        FROM item
        LEFT JOIN log ON item.key = log.entity_key
            AND log.action = 'created'
            AND log.entity_type = 'item'
        LEFT JOIN feedback ON item.key = feedback.item_key
        WHERE
            item.status = %s
            AND item.name ILIKE %s
            AND
                CASE
                    WHEN %s THEN %s = ALL(item.tags)
                    ELSE %s = ANY(item.tags)
                END

        GROUP BY item.key, log.date

        ORDER BY {} {}
        LIMIT %s OFFSET %s;
    """.format(
        order_by[sort], order_dir[sort]
    ), (
        status, f"%{search}%", multiply, tags, tags,
        page_size, (page_no - 1) * page_size
    ))
    items = cur.fetchall()

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "items": [item_schema(item) for item in items],
        "total_page": ceil(items[0][-1] / page_size) if items else 0
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
        SELECT DISTINCT *
        FROM (
            SELECT item.*
            FROM (
                SELECT *
                FROM log
                WHERE
                    user_key = %s
                    AND action = "viewed"
                    AND entity_type = "item"
                    AND entity_key != %s
            ) AS l
            LEFT JOIN item ON
                log.entity_key = item.key
                AND item.status = 'live'
            ORDER BY log.date DESC
        )
        LIMIT 8 OFFSET 0;
    """, (user_key, item_key))
    items = cur.fetchall()

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "items": [item_schema(x) for x in items]
    })


@bp.get("/similar_items/<key>")
def similar_items(item_key):
    con, cur = db_open()

    cur.execute("""
        SELECT *
        FROM item
        WHERE key = %s OR slug = %s
    """, (item_key, item_key))
    item = cur.fetchall()

    if not item:
        return jsonify({
            "status": 200,
            "items": []
        })

    def get_keywords(x):
        tags = [*x["tags"], *re.split(r'\s+', x["name"].lower())]
        return list(set(tags))

    item_keywords = get_keywords(item)

    cur.execute("""
        SELECT *,
            COUNT(INTERSECT(tags_list + STRING_TO_ARRAY(name), %s)) AS likeness
        FROM item
        WHERE status = 'live'
        ORDER BY likeness DESC
        LIMIT 8 OFFSET 0;
    """, (item_keywords,))
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
        WITH p_log AS (
            SELECT *,
                ROW_NUMBER() OVER (
                    PARTITION BY user_key
                    ORDER BY date
                ) AS row_num
            FROM log
            WHERE action = 'viewed'
            AND entity_type = 'item'
            AND user_key != %s
        )

        SELECT item.*
        FROM p_log
        LEFT JOIN item ON
            p_log.entity_key = item.key
            AND item.status = 'live'
        WHERE row_num = (
            SELECT row_num + 1
            FROM p_log
            WHERE entity_key = %s
        )
        LIMIT 8 OFFSET 0;
    """, (user_key, item_key,))
    items = cur.fetchall()

    cur.execute("""
        SELECT item.*, log.user_key AS user_key
        FROM log
        LEFT JOIN item ON log.entity_key = item.key
        WHERE log.action = 'viewed'
        AND log.entity_type = 'item'
        AND log.user_key != %s
        ORDER BY log.date ASC;
    """, (user_key, item_key,))
    views = cur.fetchall()

    unique_user = []
    unique_items = []
    pick_next_item = []
    items = []
    all_item_keys = []

    for x in views:
        if x["user_key"] not in unique_user:
            if x["entity_key"] == item_key:
                pick_next_item.append(x["user_key"])

            elif x["user_key"] in pick_next_item:
                pick_next_item.remove(x["user_key"])
                unique_user.append(x["user_key"])
                all_item_keys.append(x["item_key"])

                if x["item_key"] not in unique_items:
                    items.append(x)
                    unique_items.append(x["item_key"])

    item_count = []
    for x in items:
        item_count.append({
            "item":  x,
            "count":  all_item_keys.count(x["item_key"])
        })

    item_count = sorted(item_count, key=lambda d: d["count"], reverse=True)

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "items": [item_schema(x["item"]) for x in item_count]
    })

    # TODO: "You may also like",
