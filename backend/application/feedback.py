from flask import Blueprint, jsonify, request
from .tools import token_to_user, item_schema
from uuid import uuid4
from math import ceil
from .log import log_template
from .postgres import db_close, db_open
from datetime import datetime
import json

bp = Blueprint("feedback", __name__)


@bp.post("/feedback/<key>")
def add_feedback(item_key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    cur.execute("""
        SELECT * FROM item WHERE slug = %s OR key = %s;
    """, (item_key,))
    item = cur.fetchone()

    if not item:
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
        return jsonify({
            "status": 400,
            **error
        })

    cur.execute("""
        SELECT order_item.*
        FROM order_item
        LEFT JOIN `order` ON order_item.order_key = `order`.key
        WHERE
            order_item.item_key = %s
            AND `order`.user_key = %s
            AND `order`.status = "delivered";
    """, (item["key"], user["key"]))

    if not cur.fetchone():
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("""
        INSERT INTO feedback (key, version, user_key, item_key, rating, review)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (user_key, item_key)
        DO UPDATE SET
            rating = EXCLUDED.rating,
            review = EXCLUDED.review
        RETURNING *;
    """, (
        uuid4().hex,
        uuid4().hex,
        user["key"],
        item["key"],
        request.json["rating"],
        request.json["review"]
    ))
    feedback = cur.fetchone()

    # TODO: Add [feedback]->[added_feedback] to frontend log
    cur.execute(log_template, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "added_feedback",
        feedback["key"],
        "feedback",
        200,
        json.dumps({
            "rating":  request.json["rating"],
            "review": request.json["review"]
        })
    ))

    db_close(con, cur)

    return get_feedbacks(user["key"], item["key"])


@bp.get("/feedback/<user_key>/<item_key>")
def get_feedbacks(user_key, item_key):
    con, cur = db_open()

    sort = request.args["sort"] if "sort" in request.args else "latest"
    page_no = int(request.args["page_no"]) if "page_no" in request.args else 1
    page_size = int(request.args["size"]) if "size" in request.args else 24

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
    """, (item_key, item_key))
    item = cur.fetchone()

    if not item:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    order_by = {
        'latest': 'log.date',
        'oldest': 'log.date',
        'high_rating': 'feedback.rating',
        'low_rating': 'feedback.rating'
    }

    order_dir = {
        'latest': 'DESC',
        'oldest': 'ASC',
        'high_rating': 'DESC',
        'low_rating': 'ASC'
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
            AND log.action = 'added_feedback'
            AND log.entity_type = 'feedback'
        LEFT JOIN "user" ON feedback.user_key = "user".key
        WHERE feedback.item_key = %s
        ORDER BY {} {}
        LIMIT %s OFFSET %s;
    """.format(
        order_by[sort], order_dir[sort]
    ), (
        item["key"],
        page_size,
        (page_no - 1) * page_size
    ))
    feedbacks = cur.fetchall()

    cur.execute("""
        SELECT * FROM feedback
        WHERE item_key = %s AND user_key = %s;
    """, (item["key"], user_key))
    has_feedback = cur.fetchone()

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
        """, (item["key"], user_key))
        has_purchased = cur.fetchone()

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "item": item_schema(item),
        "feedbacks": feedbacks,
        "give_feedback": has_purchased and not has_feedback,
        "total_page": ceil(feedbacks[0]["total_items"] / page_size) if feedbacks else 0
    })
