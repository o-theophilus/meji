from datetime import datetime, timezone

from flask import Blueprint, jsonify, request

from ..log import log
from ..postgres import db_close, db_open
from ..tools import get_session
from .get import get_reviews

bp = Blueprint("review", __name__)


@bp.delete("/reviews/<key>")
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

    comment = request.json.get("comment", "").strip()

    misc = {"item_key": review["item_key"]}

    if review["user_key"] != user["key"]:
        if "review:delete_others" not in user["access"]:
            db_close(con, cur)
            return jsonify({
                "status": 403,
                "error": "unauthorized access"
            })

        error = {}
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

        misc["comment"] = comment

    cur.execute("DELETE FROM review WHERE key = %s;", (review["key"],))

    log(
        cur=cur,
        user_key=user["key"],
        action="deleted review",
        entity_key=review["key"],
        entity_type="review",
        misc=misc
    )

    reviews = get_reviews(review["item_key"], cur=cur)
    db_close(con, cur)
    return reviews


@bp.post("/reviews/<key>/like")
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


@bp.post("/reviews/<key>/report")
def report(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    comment = request.json.get("comment", "").strip()
    tags = request.json.get("tags")

    if type(tags) is not list:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    error = {}
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

    cur.execute("""SELECT * FROM review WHERE key = %s;""", (key,))
    reported_review = cur.fetchone()
    if not reported_review:
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute("""
        INSERT INTO report (reporter_key, reported_review_key,
            reporter_comment, tags)
        VALUES (%s, %s, %s, %s) RETURNING *;
    """, (user["key"], reported_review["key"], comment, tags))
    report = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="reported review",
        entity_key=report["key"],
        entity_type="report",
        misc={"key": reported_review["key"]}
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
