from flask import Blueprint, jsonify, request
from .tools import token_to_user
from uuid import uuid4
from math import ceil
from .postgres import db_close, db_open
from .log import log

bp = Blueprint("feedback", __name__)


@bp.post("/feedback/<item_key>")
def create(item_key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    cur.execute("""
        SELECT * FROM item WHERE slug = %s OR key = %s;
    """, (item_key, item_key))
    item = cur.fetchone()

    if not item:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = {}
    if "rating" not in request.json or not request.json["rating"]:
        error["rating"] = "this field is required"
    elif request.json["rating"] not in range(1, 6):
        error["rating"] = "invalid rating"
    if "review" not in request.json or not request.json["review"]:
        error["review"] = "This field is required"

    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    cur.execute("""
        SELECT order_item.*
        FROM order_item
        LEFT JOIN "order" ON order_item.order_key = "order".key
        WHERE
            order_item.item_key = %s
            AND "order".user_key = %s
            AND "order".status = 'delivered';
    """, (item["key"], user["key"]))

    if not cur.fetchone():
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("""
        SELECT * FROM feedback WHERE user_key = %s AND item_key = %s;
    """, (user["key"], item["key"]))
    feedback = cur.fetchone()

    # if feedback:
    #     cur.execute("""
    #         DELETE FROM feedback WHERE WHERE user_key = %s AND item_key = %s;
    #     """, (user["key"], item["key"]))

    cur.execute("""
        INSERT INTO feedback (key, user_key, item_key, rating, review)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING *;
    """, (
        uuid4().hex,
        user["key"],
        item["key"],
        request.json["rating"],
        request.json["review"]
    ))
    feedback = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="added_feedback",
        entity_key=feedback["key"],
        entity_type="feedback",
        misc={
            "rating":  request.json["rating"],
            "review": request.json["review"]
        }
    )

    db_close(con, cur)
    return get_many(item["key"], user["key"])


@bp.get("/feedback/<item_key>/<user_key>")
def get_many(item_key, user_key):
    con, cur = db_open()

    page_no = int(request.args["page_no"]) if "page_no" in request.args else 1
    page_size = int(request.args["size"]) if "size" in request.args else 24
    order = request.args["order"] if "order" in request.args else "latest"

    order_by = {
        'latest': 'log.date',
        'oldest': 'log.date',
        'high_rating': 'feedback.rating',
        'low_rating': 'feedback.rating',
        'name (a-z)': '"user".name',
        'name (z-a)': '"user".name'
    }

    order_dir = {
        'latest': 'DESC',
        'oldest': 'ASC',
        'high_rating': 'DESC',
        'low_rating': 'ASC',
        'name (a-z)': 'ASC',
        'name (z-a)': 'DESC'
    }

    cur.execute("""
        SELECT
            feedback.key,
            feedback.rating,
            feedback.review,
            log.date AS date,
            "user".key AS user_key,
            "user".name AS user_name,
            "user".photo AS user_photo,
            COUNT(*) OVER() AS total_items
        FROM feedback
        LEFT JOIN log ON feedback.key = log.entity_key
        LEFT JOIN "user" ON feedback.user_key = "user".key
        WHERE
            feedback.item_key = %s
            AND log.action = 'added_feedback'
            AND log.entity_type = 'feedback'
        ORDER BY {} {}
        LIMIT %s OFFSET %s;
    """.format(
        order_by[order], order_dir[order]
    ), (
        item_key,
        page_size,
        (page_no - 1) * page_size
    ))
    feedbacks = cur.fetchall()

    has_feedback = False
    for x in feedbacks:
        if x["user_photo"]:
            x["user_photo"] = f"{request.host_url}photo/{x['user_photo']}"

        if not has_feedback and x["user_key"] == user_key:
            has_feedback = True

    has_purchased = True
    if not has_feedback:
        cur.execute("""
            SELECT order_item.*
            FROM order_item
            LEFT JOIN "order" ON order_item.order_key = "order".key
            WHERE
                order_item.item_key = %s
                AND "order".user_key = %s
                AND "order".status = 'delivered';
        """, (item_key, user_key))
        has_purchased = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "feedbacks": feedbacks,
        "give_feedback": True if has_purchased and not has_feedback else False,
        "order_by": list(order_by.keys()),
        "total_page": ceil(feedbacks[0][
            "total_items"] / page_size) if feedbacks else 0
    })
