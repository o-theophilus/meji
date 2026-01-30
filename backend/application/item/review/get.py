from flask import Blueprint, jsonify, request
from ...postgres import db_close, db_open
from ...tools import get_session
from math import ceil

bp = Blueprint("review_get", __name__)


@bp.get("/review/<key>")
def get_many(key, cur=None):
    close_conn = not cur
    if not cur:
        con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        if close_conn:
            db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    # PORTFOLIO upgrade on portfolio website
    searchParams = {
        "order": 'most relevant ▼',
        "page_no": 1,
        "page_size": 24
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

    cur.execute("""
        WITH series AS (
            SELECT generate_series(1, 5) as rating
        )

        SELECT series.rating, COUNT(review.key) as count
        FROM series
        LEFT JOIN review ON
            series.rating = review.rating
            AND review.parent_key IS NULL
            AND review.item_key = %s
        GROUP BY series.rating
        ORDER BY series.rating DESC;
    """, (item["key"],))
    ratings = cur.fetchall()

    cur.execute(f"""
        WITH
        replies AS (
            SELECT
                review.parent_key,
                jsonb_agg(jsonb_build_object(
                    'key', review.key,
                    'date_created', review.date_created,
                    'comment', review.comment,
                    'user', jsonb_build_object(
                        'key', "user".key,
                        'name', "user".name,
                        'username', "user".username,
                        'photo', "user".photo
                    )
                ) ORDER BY review.date_created ASC) AS replies_array,
                COUNT(*) AS _count
            FROM review
            LEFT JOIN "user" ON review.user_key = "user".key
            WHERE review.parent_key IS NOT NULL
            GROUP BY review.parent_key
        ),
        like_info AS (
            SELECT
                review_key,
                COUNT(CASE WHEN user_key != %s
                    AND reaction = 'like' THEN 1 END) AS others_like,
                COUNT(CASE WHEN user_key != %s
                    AND reaction = 'dislike' THEN 1 END) AS others_dislike,
                (COUNT(CASE WHEN reaction = 'like' THEN 1 END) - COUNT(
                    CASE WHEN reaction = 'dislike' THEN 1 END)) AS most_like,
                MAX(CASE WHEN user_key = %s THEN reaction END) AS user_reaction
            FROM "like"
            WHERE review_key IS NOT NULL
            GROUP BY review_key
        )

        SELECT
            review.key,
            review.date_created,
            review.comment,
            review.rating,
            COALESCE(replies.replies_array, '[]'::jsonb) AS replies,
            jsonb_build_object(
                'key', "user".key,
                'name', "user".name,
                'username', "user".username,
                'photo', "user".photo
            ) AS user,
            jsonb_build_object(
                'others_like', COALESCE(like_info.others_like, 0),
                'others_dislike', COALESCE(like_info.others_dislike, 0),
                'user_reaction', like_info.user_reaction
            ) AS stats,
            COUNT(*) OVER() AS _count,
            COALESCE(replies._count, 0) AS reply_count,
            COALESCE(like_info.most_like, 0) AS most_like
        FROM review
        LEFT JOIN "user" ON review.user_key = "user".key
        LEFT JOIN replies ON review.key = replies.parent_key
        LEFT JOIN like_info ON review.key = like_info.review_key
        WHERE
            review.item_key = %s
            AND review.parent_key IS NULL
        ORDER BY {order_by[order]} {order_dir[order]}
        LIMIT %s OFFSET %s;
    """, (
        user["key"], user["key"], user["key"],
        item['key'],
        page_size, (page_no - 1) * page_size
    ))

    reviews = cur.fetchall()
    for review in reviews:
        if review["user"]["photo"]:
            review["user"]["photo"] = f'{request.host_url}photo/user/{review[
                "user"]["photo"]}'
        if review.get("replies"):
            for reply in review["replies"]:
                if reply["user"]["photo"]:
                    reply["user"]["photo"] = f'{request.host_url}photo/user/{
                        reply["user"]["photo"]}'

    if close_conn:
        db_close(con, cur)
    return jsonify({
        "status": 200,
        "item": item,
        "reviews": reviews,
        "ratings": ratings,
        "total_page": ceil(reviews[0]["_count"] / page_size) if reviews else 0,
        "order_by": list(order_by.keys()),
        "searchParams": searchParams,
    })
