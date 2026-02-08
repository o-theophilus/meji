from flask import Blueprint, jsonify, request
from ...postgres import db_close, db_open
from ...tools import get_session
from math import ceil

bp = Blueprint("review_get", __name__)


@bp.get("/review/<key>")
def get_many(key, _page_size=24, cur=None):
    close_conn = not cur
    if not cur:
        con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        if close_conn:
            db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    searchParams = {
        "order": 'most relevant ▼',
        "page_no": 1,
        "page_size": _page_size
    }
    order = request.args.get("order", searchParams["order"])
    page_no = int(request.args.get("page_no", searchParams["page_no"]))
    page_size = int(request.args.get("page_size", searchParams["page_size"]))

    order_by = {
        'latest': 'date_created',
        'oldest': 'date_created',
        'most relevant ▼': 'most_like',
        'least relevant ▲': 'most_like',
        'reply': 'reply_count',
        'rating ▼': 'rating',
        'rating ▲': 'rating',
    }
    order_dir = {
        'latest': 'DESC',
        'oldest': 'ASC',
        'most relevant ▼': 'DESC',
        'least relevant ▲': 'ASC',
        'reply': 'DESC',
        'rating ▼': 'DESC',
        'rating ▲': 'ASC',
    }

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
            r.key, r.date_created, r.comment, r.rating,
            u.key AS user_key, u.name, u.username, u.photo,
            COALESCE(l.most_like, 0) AS most_like,
            COALESCE(rc.reply_count, 0) AS reply_count
        FROM review r
        JOIN "user" u ON u.key = r.user_key

        LEFT JOIN (
            SELECT
                review_key,
                COUNT(*) FILTER (WHERE reaction = 'like') -
                COUNT(*) FILTER (WHERE reaction = 'dislike') AS most_like
            FROM "like"
            GROUP BY review_key
        ) l ON l.review_key = r.key

        LEFT JOIN (
            SELECT parent_key, COUNT(*) AS reply_count
            FROM review
            WHERE parent_key IS NOT NULL
            GROUP BY parent_key
        ) rc ON rc.parent_key = r.key

        WHERE r.item_key = %s
        AND r.parent_key IS NULL

        ORDER BY {order_by[order]} {order_dir[order]}
        LIMIT %s OFFSET %s
    """, (
        item["key"],
        page_size,
        (page_no - 1) * page_size
    ))
    reviews = cur.fetchall()
    review_keys = [r["key"] for r in reviews]

    if review_keys:
        cur.execute("""
            SELECT
                r.key, r.date_created, r.comment, r.rating, r.parent_key,
                u.key AS user_key, u.name, u.username, u.photo
            FROM review r
            JOIN "user" u ON u.key = r.user_key
            WHERE r.parent_key::TEXT = ANY(%s)
            ORDER BY r.date_created ASC
        """, (review_keys,))
        replies_raw = cur.fetchall()

        cur.execute("""
            SELECT
                review_key,
                COUNT(*) FILTER (WHERE reaction = 'like' AND user_key != %s)
                    AS others_like,
                COUNT(*) FILTER (WHERE reaction = 'dislike' AND user_key != %s)
                    AS others_dislike,
                MAX(reaction) FILTER (WHERE user_key = %s) AS user_reaction
            FROM "like"
            WHERE review_key::TEXT = ANY(%s)
            GROUP BY review_key
        """, (user["key"], user["key"], user["key"], review_keys))
        likes_raw = cur.fetchall()
    else:
        replies_raw = []
        likes_raw = []

    replies_map = {}
    for x in replies_raw:
        replies_map.setdefault(x["parent_key"], []).append({
            "key": x["key"],
            "date_created": x["date_created"],
            "comment": x["comment"],
            "rating": x["rating"],
            "user": {
                "key": x["user_key"],
                "name": x["name"],
                "username": x["username"],
                "photo": f'{request.host_url}photo/user/{
                    x["photo"]}' if x["photo"] else None
            }
        })

    likes_map = {
        x["review_key"]: {
            "others_like": x["others_like"],
            "others_dislike": x["others_dislike"],
            "user_reaction": x["user_reaction"]
        }
        for x in likes_raw
    }

    final_reviews = []
    for x in reviews:
        final_reviews.append({
            "key": x["key"],
            "date_created": x["date_created"],
            "comment": x["comment"],
            "rating": x["rating"],
            "user": {
                "key": x["user_key"],
                "name": x["name"],
                "username": x["username"],
                "photo": f'{request.host_url}photo/user/{
                    x["photo"]}' if x["photo"] else None
            },
            "stats": likes_map.get(x["key"], {
                "others_like": 0,
                "others_dislike": 0,
                "user_reaction": None
            }),
            "replies": replies_map.get(x["key"], [])
        })

    cur.execute("""
        SELECT rating, COUNT(*) AS count FROM review
        WHERE item_key = %s AND parent_key IS NULL
        GROUP BY rating
        ORDER BY rating DESC
    """, (item["key"],))
    ratings = cur.fetchall()

    cur.execute("""
        WITH purchase_check AS (
            SELECT EXISTS (
                SELECT 1
                FROM item_snap i
                JOIN "order" o ON o.key = i.order_key
                WHERE o.user_key = %s AND i.item_key = %s
                    AND o.status = 'delivered'
            ) AS has_purchased
        )
        SELECT
            has_purchased,
            has_purchased
            AND NOT EXISTS (
                SELECT 1 FROM review r
                WHERE r.user_key = %s AND r.item_key = %s
            ) AS can_review
        FROM purchase_check;
    """, (user["key"], item["key"], user["key"], item["key"]))
    user_review_info = cur.fetchone()

    cur.execute("""
        SELECT COUNT(*) FROM review
        WHERE item_key = %s AND parent_key IS NULL
    """, (item["key"],))
    total_page = cur.fetchone()["count"]

    if close_conn:
        db_close(con, cur)
    return jsonify({
        "status": 200,
        "item": item,
        "reviews": final_reviews,
        "ratings": ratings,
        "total_page": ceil(total_page / page_size),
        "order_by": list(order_by.keys()),
        "searchParams": searchParams,
        "has_purchased": user_review_info["has_purchased"],
        "can_review": user_review_info["can_review"],
    })
