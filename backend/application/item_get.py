from flask import Blueprint, jsonify, request
from .tools import token_to_user, item_schema
from math import ceil
from .advert import get_all_advert
from .feedback import get_feedbacks
import re
from .postgres import db_close, db_open


bp = Blueprint("item_get", __name__)


def recently_viewed(cur, user_key, item_key):
    cur.execute("""
        SELECT
            item.*,
            CASE
                WHEN COUNT(feedback.*) = 0 THEN ARRAY[]::integer[]
                ELSE ARRAY_AGG(feedback.rating)
            END AS ratings
        FROM (
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
        ) as item
        LEFT JOIN feedback ON item.key = feedback.item_key
        GROUP BY
            item.date, item.key, item.status, item.name, item.slug, item.price,
            item.old_price, item.information, item.photos, item.tags,
            item.variation, item.available_quantity
        ORDER BY item.date DESC
        LIMIT 8 OFFSET 0
        ;
    """, (user_key, item_key))
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

    return [item_schema(x) for x in items]


def customer_view(cur, user_key, item_key):
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

    return [item_schema(x["item"]) for x in item_count]


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
        and "item:add" not in user["permissions"]
        and "item:edit_status" not in user["permissions"]
    ):
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    _recently_viewed = recently_viewed(cur, user["key"], item["key"])
    _similar_items = similar_items(cur, item["key"])
    _customer_view = customer_view(cur, user["key"], item["key"])

    db_close(con, cur)

    fb = get_feedbacks(user["key"], item["key"]).json

    return jsonify({
        "status": 200,
        "item": item_schema(item),
        "feedbacks": fb["feedbacks"],
        "give_feedback": fb["give_feedback"],
        "recently_viewed": _recently_viewed,
        "similar_items": _similar_items,
        "customer_view": _customer_view
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
            "item:edit_status" in user["permissions"]
            or "item:add" in user["permissions"]
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
        query = f"""
            AND cardinality(item.tags) > 0
            AND item.tags {"@>" if multiply else "&&"} ARRAY[{tags}]
        """

    cur.execute("""
        SELECT
            item.*,
            CASE
                WHEN COUNT(feedback.*) = 0 THEN 0
                ELSE SUM(feedback.rating) / COUNT(feedback.*)
            END AS rating,
            CASE
                WHEN COUNT(feedback.*) = 0 THEN ARRAY[]::integer[]
                ELSE ARRAY_AGG(feedback.rating)
            END AS ratings,
            COUNT(*) OVER() AS total_items
        FROM (
            SELECT *,
                CASE
                    WHEN old_price = 0 THEN 0
                    ELSE (100 * (old_price - price)) / old_price
                END AS discount
            FROM item
        ) AS item
        LEFT JOIN feedback ON item.key = feedback.item_key
        LEFT JOIN log ON item.key = log.entity_key
            AND log.action = 'created'
            AND log.entity_type = 'item'
        WHERE
            item.status = %s
            AND (%s = '' OR item.name ILIKE %s) {}
        GROUP BY
            item.key, item.status, item.name, item.slug,
            item.price, item.old_price, item.information, item.photos,
            item.tags, item.variation, item.available_quantity,
            item.discount, log.date
        ORDER BY {} {}
        LIMIT %s OFFSET %s;
    """.format(
        query,
        order_by[sort], order_dir[sort]
    ), (
        status,
        search, f"%{search}%",
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
        "adverts": get_all_advert("live", "home_1").json["adverts"]
    })
