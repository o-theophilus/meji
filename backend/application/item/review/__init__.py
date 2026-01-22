from flask import Blueprint, jsonify, request
from ...tools import get_session
from ...postgres import db_close, db_open
from ...log import log
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
        cur.execute("SELECT * FROM review WHERE key = %s;", (parent_key,))
        if not cur.fetchone():
            db_close(con, cur)
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
    if error != {}:
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
        action="created",
        entity_key=comment["key"],
        entity_type="review",
        misc={"item_key": item["key"]}
    )

    reviews = get_many(item["key"], cur)
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

    cur.execute("""
        SELECT * FROM review WHERE key = %s AND user_key = %s;
    """, (key, user["key"]))
    review = cur.fetchone()
    if not review:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    if (
        review["user_key"] != user["key"]
        and "review:delete" not in user["access"]
    ):
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

    cur.execute("""
        DELETE FROM "like"
        WHERE entity_type = 'review' AND entity_key = %s;
    """, (review["key"],))

    cur.execute("""DELETE FROM review WHERE key = %s;""", (review["key"],))

    log(
        cur=cur,
        user_key=user["key"],
        action="deleted",
        entity_key=review["key"],
        entity_type="review",
        misc={"item_key": review["item_key"]}
    )

    reviews = get_many(review["item_key"], cur)
    db_close(con, cur)
    return reviews
