from flask import Blueprint, jsonify, request
from math import ceil
import re
from ..postgres import db_open, db_close
from ..tools import get_session

bp = Blueprint("item_get", __name__)


def item_schema(x):
    x["files"] = [f"{request.host_url}photo/item/{x}" for x in x["files"]]
    return x


def get_tags(cur=None):
    close_conn = not cur
    if not cur:
        con, cur = db_open()

    cur.execute("SELECT tags FROM item WHERE status = 'active';")
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

    if close_conn:
        db_close(con, cur)
    return jsonify({
        "status": 200,
        "tags": [x["tag"] for x in tags_count]
    })


@bp.get("/item/<key>")
def get(key):
    con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute("""
        SELECT * FROM item WHERE slug = %s OR key::TEXT = %s
    """, (key, key))
    item = cur.fetchone()

    if not item:
        db_close(con, cur)
        return jsonify({
            "status": 404,
            "error": "Oops! The item you're looking for doesn't exist"
        })

    if (
        item["status"] != "active"
        and "item:add" not in user["access"]
        and "item:edit_status" not in user["access"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "item": item_schema(item)
    })


@bp.get("/items")
def get_many(cur=None, _order="latest", _page_size=24):
    close_conn = not cur
    if not cur:
        con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        if close_conn:
            db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if (
        "item:edit_status" not in user["access"]
        or "item:add" not in user["access"]
    ):
        status = "active"

    searchParams = {
        "search": "",
        "status": "active",
        "tag": "",
        "order": _order,
        "page_no": 1,
        "page_size": _page_size
    }
    search = request.args.get("search", searchParams["search"]).strip()
    status = request.args.get("status", searchParams["status"])
    tag = request.args.get("tag", searchParams["tag"])
    order = request.args.get("order", searchParams["order"])
    page_no = int(request.args.get("page_no", searchParams["page_no"]))
    page_size = int(request.args.get("page_size", searchParams["page_size"]))

    order_by = {
        'latest': 'item.date_created',
        'oldest': 'item.date_created',
        'name (a-z)': 'item.name',
        'name (z-a)': 'item.name',
        'cheap': 'item.price',
        'costly': 'item.price',
        'discount': 'discount',
        'rating': 'rating'
    }
    order_dir = {
        'latest': 'DESC',
        'oldest': 'ASC',
        'name (a-z)': 'ASC',
        'name (z-a)': 'DESC',
        'cheap': 'ASC',
        'costly': 'DESC',
        'discount': 'DESC',
        'rating': 'DESC',
    }

    multiply = False
    if tag[-4:] == ":all":
        multiply = True
        tag = tag[:-4]
    tags = tag.split(",")
    tags = [] if not tags[0] else tags

    # TEST check for sql injection
    params = [status, search, f"%{search}%"]
    tag_query = ""
    if tags != []:
        op = "@>" if multiply else "&&"
        tag_query = f"AND cardinality(item.tags) > 0 AND item.tags {op} %s"
        params.append(tags)
    params.append(page_size)
    params.append((page_no - 1) * page_size)

    cur.execute(f"""
        WITH rating AS (
            SELECT
                review.item_key AS key,
                AVG(review.rating) as rating
            FROM review
            WHERE review.parent_key IS NULL
            GROUP BY review.item_key
        )

        SELECT item.*,
            CASE
                WHEN item.price = 0 OR item.price_old = 0 THEN 0
                ELSE ((item.price_old - item.price) * 100) / item.price_old
            END AS discount,
            COALESCE(rating.rating, 0) AS rating,
            COUNT(*) OVER() AS _count
        FROM item
        LEFT JOIN rating ON item.key = rating.key
        WHERE
            item.status = %s
            AND (%s = '' OR item.name ILIKE %s) {tag_query}
        ORDER BY {order_by[order]} {order_dir[order]}
        LIMIT %s OFFSET %s;
    """, params)
    items = cur.fetchall()

    if close_conn:
        db_close(con, cur)
    return jsonify({
        "status": 200,
        "items": [item_schema(x) for x in items],
        "total_page": ceil(items[0]["_count"] / page_size) if items else 0,
        "order_by": list(order_by.keys()),
        "searchParams": searchParams,
        "_status": ['active', 'draft']
    })


@bp.get("/home")
def home_page():
    con, cur = db_open()

    new_arrivals = get_many(cur, "latest", 8).json['items']
    discount = get_many(cur, "discount", 8).json['items']

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "new_arrivals": new_arrivals,
        "discount": discount
    })


@bp.get("/like")
def like_page():
    con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    searchParams = {
        "search": "",
        "order": "latest",
        "page_no": 1,
        "page_size": 24
    }
    search = request.args.get("search", searchParams["search"]).strip()
    order = request.args.get("order", searchParams["order"])
    page_no = int(request.args.get("page_no", searchParams["page_no"]))
    page_size = int(request.args.get("page_size", searchParams["page_size"]))

    order_by = {
        'latest': 'item.date_created',
        'oldest': 'item.date_created',
        'name (a-z)': 'item.name',
        'name (z-a)': 'item.name',
        'cheap': 'item.price',
        'costly': 'item.price'
    }

    order_dir = {
        'latest': 'DESC',
        'oldest': 'ASC',
        'name (a-z)': 'ASC',
        'name (z-a)': 'DESC',
        'cheap': 'ASC',
        'costly': 'DESC'
    }

    cur.execute(f"""
        SELECT
            item.*,
            COUNT(*) OVER() AS _count
        FROM item
        LEFT JOIN "like" ON
            item.key = "like".item_key
        WHERE
            item.status = 'active'
            AND "like".user_key = %s
            AND "like".reaction = 'like'
            AND (%s = '' OR item.name ILIKE %s)
        ORDER BY {order_by[order]} {order_dir[order]}
        LIMIT %s OFFSET %s;
    """, (
        user["key"],
        search, f"%{search}%",
        page_size, (page_no - 1) * page_size
    ))
    items = cur.fetchall()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "items": [item_schema(x) for x in items],
        "total_page": ceil(items[0]["_count"] / page_size) if items else 0,
        "order_by": list(order_by.keys()),
        "searchParams": searchParams,
    })


@bp.get("/item/similar/<key>")
def similar_items(key):
    con, cur = db_open()

    cur.execute("""
        SELECT * FROM item WHERE key = %s;
    """, (key,))
    item = cur.fetchone()

    if not item:
        db_close(con, cur)
        return jsonify({
            "status": 200,
            "items": []
        })

    keywords = list(set(
        item["tags"] + re.split(r'\s+', item["name"].lower())))

    cur.execute("""
        WITH likeness AS (
            SELECT key, COUNT(*) AS score
            FROM item,
                unnest(tags || STRING_TO_ARRAY(lower(name), ' ')) AS tn
            WHERE tn = ANY(%s)
            GROUP BY key
        )
        SELECT item.*
        FROM item
        JOIN likeness ON item.key = likeness.key
        WHERE item.status = 'active'
            AND item.key != %s
            AND likeness.score > 0
        ORDER BY likeness.score DESC
        LIMIT 4;
    """, (keywords, key))
    items = cur.fetchall()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "items": [item_schema(x) for x in items]
    })
