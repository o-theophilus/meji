from datetime import datetime, timezone

from flask import Blueprint, jsonify, request

from ...log import log
from ...postgres import db_close, db_open
from ...tools import get_session
from .get import get_many

bp = Blueprint("review", __name__)


@bp.post("/review/<key>")
def create(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute("""
        SELECT * FROM item WHERE slug = %s OR key = %s;
    """, (key, key))
    item = cur.fetchone()
    if not item:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    parent_key = request.json.get("parent_key")
    if parent_key:
        if "review:reply" not in user["access"]:
            db_close(con, cur)
            return jsonify({
                "status": 400,
                "error": "unauthorized access"
            })

        cur.execute("SELECT * FROM review WHERE key = %s;", (parent_key,))
        if not cur.fetchone():
            db_close(con, cur)
            return jsonify({
                "status": 400,
                "error": "Invalid request"
            })

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

    if not user_review_info["can_review"]:
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    rating = request.json.get("rating", 0)
    comment = request.json.get("comment")
    error = {}
    if rating not in [1, 2, 3, 4, 5]:
        error["rating"] = "This field is required"

    if not comment:
        error["comment"] = "This field is required"
    elif len(comment) > 500:
        error["comment"] = "This field cannot exceed 500 characters"
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    cur.execute("""
        INSERT INTO review (user_key, item_key, rating, comment, parent_key)
        VALUES (%s, %s, %s, %s, %s) RETURNING *;
    """, (user["key"], item["key"], rating, comment, parent_key))
    comment = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="added item review",
        entity_key=comment["key"],
        entity_type="review",
        misc={"item_key": item["key"]}
    )

    reviews = get_many(item["key"], cur=cur)
    db_close(con, cur)
    return reviews


@bp.delete("/review/<key>")
def delete(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute("""SELECT * FROM review WHERE key = %s;""", (key,))
    review = cur.fetchone()
    if not review:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    if review["user_key"] != user["key"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })
    elif review["user_key"] != user["key"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute("""DELETE FROM review WHERE key = %s;""", (review["key"],))

    log(
        cur=cur,
        user_key=user["key"],
        action="deleted item review",
        entity_key=review["key"],
        entity_type="review",
        misc={"item_key": review["item_key"]}
    )

    reviews = get_many(review["item_key"], cur=cur)
    db_close(con, cur)
    return reviews


@bp.post("/review/like/<key>")
def like(key):
    con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    reaction = request.json.get("reaction")

    cur.execute("""SELECT * FROM review WHERE key = %s;""", (key,))
    review = cur.fetchone()
    if (not review or reaction not in ["like", "dislike"]):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute("""
        SELECT * FROM review_like
        WHERE user_key = %s AND review_key = %s;
    """, (user["key"], review["key"]))
    user_reaction = cur.fetchone()

    un = ""
    if not user_reaction:
        cur.execute("""
            INSERT INTO review_like (user_key, review_key, reaction)
            VALUES (%s, %s, %s);
        """, (user["key"], review["key"], reaction))
    elif user_reaction["reaction"] == reaction:
        un = "un"
        cur.execute("""DELETE FROM review_like WHERE key = %s;""",
                    (user_reaction["key"],))
    else:
        cur.execute("""
            UPDATE review_like
            SET date_created = %s, reaction = %s WHERE key = %s;
        """, (datetime.now(timezone.utc), reaction, user_reaction["key"]))

    log(
        cur=cur,
        user_key=user["key"],
        action=f"{un}{reaction} review",
        entity_key=review["key"],
        entity_type="review",
        misc={"item_key": review["item_key"]}
    )

    cur.execute("""
        SELECT
            COUNT(CASE WHEN user_key != %s
                AND reaction = 'like' THEN 1 END) AS others_like,
            COUNT(CASE WHEN user_key != %s
                AND reaction = 'dislike' THEN 1 END) AS others_dislike,
            MAX(CASE WHEN user_key = %s THEN reaction END) AS user_reaction
        FROM review_like
        WHERE review_key = %s
    """, (user["key"], user["key"], user["key"], review["key"]))
    reactions = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        **reactions
    })
