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

    review = request.json.get("review")
    error = {}
    if not review:
        error["review"] = "This field is required"
    elif len(review) > 500:
        error["review"] = "This field cannot exceed 500 characters"
    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    cur.execute("""
        INSERT INTO review (user_key, item, review, parent_key)
        VALUES (%s, %s, %s, %s) RETURNING *;
    """, (user["key"], item["key"], review, parent_key))
    review = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="created",
        entity_key=review["key"],
        entity_type="review",
        misc={"item_key": item["key"]}
    )

    items = get_many(item["key"], cur)
    db_close(con, cur)
    return items


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

    cur.execute("""
        DELETE FROM "like"
        WHERE entity_type = 'review' entity_key = %s;
    """, (review["key"],))

    cur.execute("""
        WITH RECURSIVE to_delete AS (
            SELECT key
            FROM review
            WHERE key = %s

            UNION ALL

            SELECT c.key
            FROM review c
            INNER JOIN to_delete td ON c.parent_key = td.key
        )
        DELETE FROM review
        WHERE key IN (SELECT key FROM to_delete);
    """, (review["key"],))

    log(
        cur=cur,
        user_key=user["key"],
        action="deleted",
        entity_key=review["key"],
        entity_type="review",
        misc={"item_key": review["item_key"]}
    )

    items = get_many(review["item_key"], cur)
    db_close(con, cur)
    return items
