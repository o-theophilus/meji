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

    session = get_session(cur, True)
    if session["status"] != 200:
        if close_conn:
            db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute("""
        SELECT * FROM item WHERE slug = %s OR key::TEXT = %s;
    """, (key, key))
    item = cur.fetchone()
    if not item:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    order_by = {
        'latest': 'review.date_created',
        'oldest': 'review.date_created',
        'like': 'engagement."like"',
        'dislike': 'engagement.dislike',
        'most_like': 'engagement.most_like',
        'reply': 'engagement.reply',
        'most_engaged': 'engagement.total',
    }

    order_dir = {
        'latest': 'DESC',
        'oldest': 'ASC',
        'like': 'DESC',
        'dislike': 'DESC',
        'most_like': 'DESC',
        'reply': 'DESC',
        'most_engaged': 'DESC',
    }

    order = request.args.get("order", "oldest")
    page_no = int(request.args.get("page_no", 1))
    page_size = int(request.args.get("page_size", 24))

    cur.execute(f"""
        WITH
        _like AS (
            SELECT
                entity_key AS key,
                COUNT(*) FILTER (WHERE reaction = 'like') AS "like",
                COUNT(*) FILTER (WHERE reaction = 'dislike') AS dislike
            FROM "like"
            WHERE entity_type = 'review' AND user_key != %s
            GROUP BY entity_key
        ),
        user_like AS (
            SELECT
                entity_key AS key, reaction
            FROM "like"
            WHERE entity_type = 'review' AND user_key = %s
        ),
        reply AS (
            SELECT
                parent_key AS key,
                COUNT(*) AS reply_count
            FROM review
            WHERE parent_key IS NOT NULL
            GROUP BY parent_key
        ),
        engagement AS (
            SELECT
                review.key,
                COALESCE(_like."like", 0) AS "like",
                COALESCE(_like.dislike, 0) AS dislike,
                COALESCE(_like."like", 0)
                - COALESCE(_like.dislike, 0) AS most_like,
                COALESCE(reply.reply_count, 0) AS reply,
                COALESCE(_like."like", 0)
                + COALESCE(_like.dislike, 0)
                + COALESCE(reply.reply_count, 0) AS total,
                user_like.reaction AS reaction
            FROM review
            LEFT JOIN _like ON review.key::TEXT = _like.key
            LEFT JOIN reply ON review.key = reply.key
            LEFT JOIN user_like ON review.key::TEXT = user_like.key
        ),


        parent AS (
            SELECT
                review.key,
                review.date_created,
                review.comment,
                review.rating,
                jsonb_build_object(
                    'key', "user".key,
                    'name', "user".name,
                    'username', "user".username,
                    'photo', "user".photo
                ) AS user
            FROM review
            LEFT JOIN "user" ON review.user_key = "user".key
        )


        SELECT
            review.key,
            review.date_created,
            review.comment,
            review.rating,
            review.parent_key,
            jsonb_build_object(
                'key', "user".key,
                'name', "user".name,
                'username', "user".username,
                'photo', "user".photo
            ) AS user,
            jsonb_build_object(
                'like', COALESCE(engagement."like", 0),
                'dislike', COALESCE(engagement.dislike, 0),
                'most_like', COALESCE(engagement.most_like, 0),
                'reply', COALESCE(engagement.reply, 0),
                'most_engaged', COALESCE(engagement.total, 0),
                'user_like', engagement.reaction
            ) AS engagement,
            jsonb_build_object(
                'key', parent.key,
                'date_created', parent.date_created,
                'comment', parent.comment,
                'rating', parent.rating,
                'user', parent.user
            ) AS parent,
            COUNT(*) OVER() AS _count
        FROM review
        LEFT JOIN "user" ON review.user_key = "user".key
        LEFT JOIN engagement ON review.key = engagement.key
        LEFT JOIN parent ON review.parent_key = parent.key
        WHERE review.item_key = %s
        ORDER BY {order_by[order]} {order_dir[order]}
        LIMIT %s OFFSET %s;
    """, (
        user["key"], user["key"],
        item['key'],
        page_size, (page_no - 1) * page_size
    ))

    reviews = cur.fetchall()

    for x in reviews:
        if x["user"]["photo"]:
            x["user"]["photo"] = f'{request.host_url}photo/user/{
                x["user"]["photo"]}'
        if (
            x["parent"]["user"]
            and "photo" in x["parent"]["user"]
            and x["parent"]["user"]["photo"]
        ):
            x["parent"]["user"]["photo"] = f'{request.host_url}photo/user/{
                x["parent"]["user"]["photo"]}'

    if close_conn:
        db_close(con, cur)
    return jsonify({
        "status": 200,
        "item": item,
        "reviews": reviews,
        "order_by": list(order_by.keys()),
        "total_page": ceil(reviews[0]["_count"] / page_size) if reviews else 0
    })
