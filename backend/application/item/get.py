from math import ceil

from flask import Blueprint, jsonify, request

from ..postgres import db_close, db_open
from ..tools import get_session, item_schema
from .get_group import (customer_view, recently_viewed, recommended,
                        similar_items)

bp = Blueprint("item_get", __name__)


def get_item_tags(cur=None):
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
    return [x["tag"] for x in tags_count]


@bp.get("/items/<key>")
def get(key):
    con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "v" in request.args:
        cur.execute("""
            SELECT item_version.*, item.slug AS item_slug,
                to_jsonb(item) AS latest
            FROM item_version
            LEFT JOIN item on item_version.item_key = item.key
            WHERE item_version.key::TEXT = %s;
        """, (key,))
        item = cur.fetchone()
        if item and item["item_slug"]:
            item["latest"] = item_schema(item["latest"])
            del item["item_key"]

    else:
        cur.execute("""
            SELECT * FROM item WHERE slug = %s OR key::TEXT = %s;
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
        and "item.add" not in user["access"]
        and "item.edit_status" not in user["access"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 403,
            "error": "unauthorized access"
        })

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "item": item_schema(item)
    })


@bp.get("/items")
def get_items(cur=None, _order="latest", _page_size=24):
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
        "item.edit_status" not in user["access"]
        or "item.add" not in user["access"]
    ):
        status = "active"

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
    page_size = min(page_size, 100)

    params = [status, search, f"%{search}%"]

    op = "&&"
    tag_query = ""
    if tag[-4:] == ":all":
        op = "@>"
        tag = tag[:-4]
    tags = tag.split(",") if tag else []
    if tags != []:
        tag_query = f"AND cardinality(item.tags) > 0 AND item.tags {op} %s"
        params.append(tags)

    params.append(page_size)
    params.append((page_no - 1) * page_size)

    cur.execute(f"""
        WITH rating AS (
            SELECT
                comment.item_key AS key,
                AVG(comment.rating) as rating
            FROM comment
            WHERE comment.item_key IS NOT NULL AND comment.parent_key IS NULL
            GROUP BY comment.item_key
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
        ORDER BY {order_by[order]} {order_dir[order]}, item.key DESC
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


@bp.get("/items/<key>/comments")
def get_comments(key, _page_size=24, cur=None):
    close_conn = not cur
    if not cur:
        con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        if close_conn:
            db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    order_by = {
        'latest': 'date_created',
        'oldest': 'date_created',
        'reply': 'reply_count',
        'most relevant ▼': 'most_like',
        'least relevant ▲': 'most_like',
        'rating ▼': 'rating',
        'rating ▲': 'rating',
    }
    order_dir = {
        'latest': 'DESC',
        'oldest': 'ASC',
        'reply': 'DESC',
        'most relevant ▼': 'DESC',
        'least relevant ▲': 'ASC',
        'rating ▼': 'DESC',
        'rating ▲': 'ASC',
    }

    searchParams = {
        "order": 'most relevant ▼',
        "page_no": 1,
        "page_size": _page_size
    }
    order = request.args.get("order", searchParams["order"])
    page_no = int(request.args.get("page_no", searchParams["page_no"]))
    page_size = int(request.args.get("page_size", searchParams["page_size"]))
    page_size = min(page_size, 100)

    cur.execute("""
        SELECT * FROM item WHERE slug = %s OR key::TEXT = %s;
    """, (key, key))
    item = cur.fetchone()
    if not item:
        if close_conn:
            db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute(f"""
        SELECT
            c.key, c.date_created, c.comment, c.rating,
            u.key AS user_key, u.name, u.username, u.photo,
            COALESCE(sub_c.reply_count, 0) AS reply_count,
            COALESCE(l.most_like, 0) AS most_like

        FROM comment c
        JOIN "user" u ON u.key = c.user_key

        LEFT JOIN (
            SELECT parent_key, COUNT(*) AS reply_count
            FROM comment
            WHERE parent_key IS NOT NULL
            GROUP BY parent_key
        ) sub_c ON sub_c.parent_key = c.key

        LEFT JOIN (
            SELECT
                comment_key,
                COUNT(*) FILTER (WHERE reaction = 'like') -
                COUNT(*) FILTER (WHERE reaction = 'dislike') AS most_like
            FROM "like"
            WHERE comment_key IS NOT NULL
            GROUP BY comment_key
        ) l ON l.comment_key = c.key

        WHERE c.item_key = %s AND c.parent_key IS NULL
        ORDER BY {order_by[order]} {order_dir[order]}, c.key DESC
        LIMIT %s OFFSET %s
    """, (
        item["key"],
        page_size,
        (page_no - 1) * page_size
    ))
    _comments = cur.fetchall()
    comment_keys = [r["key"] for r in _comments]

    replies = []
    likes = []

    if comment_keys:
        cur.execute("""
            SELECT
                c.key, c.date_created, c.comment, c.rating, c.parent_key,
                u.key AS user_key, u.name, u.username, u.photo
            FROM comment c
            JOIN "user" u ON u.key = c.user_key
            WHERE c.parent_key::TEXT = ANY(%s)
            ORDER BY c.date_created ASC
        """, (comment_keys,))
        replies = cur.fetchall()

        for x in replies:
            comment_keys.append(x["key"])

        cur.execute("""
            SELECT
                comment_key,
                COUNT(*) FILTER (WHERE reaction = 'like' AND user_key != %s)
                    AS others_like,
                COUNT(*) FILTER (WHERE reaction = 'dislike' AND user_key != %s)
                    AS others_dislike,
                MAX(reaction) FILTER (WHERE user_key = %s) AS user_reaction
            FROM "like"
            WHERE comment_key::TEXT = ANY(%s)
            GROUP BY comment_key
        """, (user["key"], user["key"], user["key"], comment_keys))
        likes = cur.fetchall()

    likes_map = {
        x["comment_key"]: {
            "others_like": x["others_like"],
            "others_dislike": x["others_dislike"],
            "user_reaction": x["user_reaction"]
        }
        for x in likes
    }

    replies_map = {}
    for x in replies:
        replies_map.setdefault(x["parent_key"], []).append({
            "key": x["key"],
            "date_created": x["date_created"],
            "comment": x["comment"],
            "rating": x["rating"],
            "user": {
                "key": x["user_key"],
                "name": x["name"],
                "username": x["username"],
                "photo": f'{request.host_url}photo/user/{x["photo"]}' if x[
                    "photo"] else None
            },
            "stats": likes_map.get(x["key"], {
                "others_like": 0,
                "others_dislike": 0,
                "user_reaction": None
            }),
        })

    comments = []
    for x in _comments:
        comments.append({
            "key": x["key"],
            "date_created": x["date_created"],
            "comment": x["comment"],
            "rating": x["rating"],
            "user": {
                "key": x["user_key"],
                "name": x["name"],
                "username": x["username"],
                "photo": f'{request.host_url}photo/user/{x["photo"]}' if x[
                    "photo"] else None
            },
            "stats": likes_map.get(x["key"], {
                "others_like": 0,
                "others_dislike": 0,
                "user_reaction": None
            }),
            "replies": replies_map.get(x["key"], [])
        })

    cur.execute("""
        SELECT
            r.rating,
            COUNT(comment.rating) AS count
        FROM generate_series(1, 5) AS r(rating)
        LEFT JOIN comment
            ON comment.rating = r.rating
            AND comment.item_key = %s
            AND comment.parent_key IS NULL
        GROUP BY r.rating
        ORDER BY r.rating DESC
    """, (item["key"],))
    ratings = cur.fetchall()

    cur.execute("""
        WITH purchase_check AS (
            SELECT EXISTS (
                SELECT 1
                FROM item_version item
                JOIN order_item ON item.key = order_item.item_key
                JOIN "order" o ON order_item.order_key = o.key
                WHERE o.user_key = %s AND item.key = %s
                    AND o.status = 'delivered'
            ) AS has_purchased
        )
        SELECT
            has_purchased,
            has_purchased
            AND NOT EXISTS (
                SELECT 1 FROM comment
                WHERE comment.user_key = %s
                    AND comment.item_key = %s
            ) AS can_comment
        FROM purchase_check;
    """, (user["key"], item["key"], user["key"], item["key"]))
    user_comment_info = cur.fetchone()

    cur.execute("""
        SELECT
            COUNT(*) AS total_comment,
            COUNT(*) FILTER (WHERE parent_key IS NULL) AS total_parent
        FROM comment
        WHERE item_key = %s;
    """, (key,))
    total = cur.fetchone()
    total_comment = total["total_comment"]
    total_parent = total["total_parent"]

    if close_conn:
        db_close(con, cur)
    return jsonify({
        "status": 200,
        "item": item,
        "comments": comments,
        "ratings": ratings,
        "total_comment": total_comment,
        "total_page": ceil(total_parent / page_size),
        "order_by": list(order_by.keys()),
        "searchParams": searchParams,
        "has_purchased": user_comment_info["has_purchased"],
        "can_comment": user_comment_info["can_comment"],
    })


@bp.get("/items/<key>/after")
def after_get(key):
    con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute("""SELECT * FROM item WHERE key = %s;""", (key,))
    if not cur.fetchone():
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    item_group = []
    _similar_items = similar_items(cur, key)
    if _similar_items:
        item_group.append({
            "name": "Similar Items",
            "items": _similar_items,
            "style": "grid",
            "open": True
        })

    _recently_viewed = recently_viewed(cur, user["key"], key)
    if _recently_viewed:
        item_group.append({
            "name": "Recently Viewed",
            "items": _recently_viewed,
            "style": "line",
            "open": True
        })

    _customer_view = customer_view(cur, user["key"], key)
    if _customer_view:
        item_group.append({
            "name": "Customers who viewed this also viewed",
            "items": _customer_view,
            "style": "line",
            "open": True
        })

    _recommended = recommended(cur, user["key"], key)
    if _recommended:
        item_group.append({
            "name": "You may also like",
            "items": _recommended,
            "style": "line",
            "open": True
        })

    comments = get_comments(key, 3, cur).json

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "comments": comments,
        "item_group": item_group
    })


@bp.get("/items/home")
def home_page():
    con, cur = db_open()

    new_arrivals = get_items(cur, "latest", 8).json['items']
    discount = get_items(cur, "discount", 16).json['items']

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "new_arrivals": new_arrivals,
        "discount": discount
    })


@bp.get("/items/like")
def like_page():
    con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

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
    page_size = min(page_size, 100)

    cur.execute(f"""
        WITH rating AS (
            SELECT
                comment.item_key AS key,
                AVG(comment.rating) as rating
            FROM comment
            WHERE comment.item_key IS NOT NULL AND comment.parent_key IS NULL
            GROUP BY comment.item_key
        )

        SELECT
            item.*,
            COALESCE(rating.rating, 0) AS rating,
            COUNT(*) OVER() AS _count
        FROM item
        LEFT JOIN "like" ON item.key = "like".item_key
        LEFT JOIN rating ON item.key = rating.key
        WHERE
            item.status = 'active'
            AND "like".user_key = %s
            AND "like".item_key IS NOT NULL
            AND (%s = '' OR item.name ILIKE %s)
        ORDER BY {order_by[order]} {order_dir[order]}, item.key DESC
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
