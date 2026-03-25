from flask import Blueprint, jsonify, request

from ..blog.get import get_comments as get_blog_comments
from ..item.get import get_comments as get_item_comments
from ..log import log
from ..postgres import db_close, db_open
from ..tools import get_session

bp = Blueprint("comment", __name__)


@bp.delete("/comments/<key>")
def delete(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute("""SELECT * FROM comment WHERE key = %s;""", (key,))
    comment = cur.fetchone()
    if not comment:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    misc = {}

    if comment["user_key"] != user["key"]:
        if "comment.delete_others" not in user["access"]:
            db_close(con, cur)
            return jsonify({
                "status": 403,
                "error": "unauthorized access"
            })

        _comment = request.json.get("comment", "").strip()

        error = {}
        if not _comment:
            error["comment"] = "This field is required"
        elif len(_comment) > 500:
            error["comment"] = "This field cannot exceed 500 characters"
        if error:
            db_close(con, cur)
            return jsonify({
                "status": 400,
                **error
            })

        misc["comment"] = _comment

    cur.execute("DELETE FROM comment WHERE key = %s;", (comment["key"],))
    # TODO: delete likes / reports

    log(
        cur=cur,
        user_key=user["key"],
        action="deleted comment",
        entity_type="comment",
        entity_key=comment["key"],
        misc=misc
    )

    if comment["entity_key"] == "item":
        comments = get_item_comments(comment["entity_key"], cur=cur)
    else:
        comments = get_blog_comments(comment["entity_key"], cur=cur)
    db_close(con, cur)
    return comments


@bp.post("/comments/<key>/like")
def like(key):
    con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    reaction = request.json.get("reaction")

    cur.execute("""SELECT * FROM comment WHERE key = %s;""", (key,))
    comment = cur.fetchone()
    if not comment or reaction not in ["like", "dislike"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute("""
        SELECT * FROM "like" WHERE user_key = %s AND entity_key = %s;
    """, (user["key"], comment["key"]))
    user_reaction = cur.fetchone()

    un = ""
    if not user_reaction:
        cur.execute("""
            INSERT INTO "like" (user_key, reaction, entity_key, entity_type)
            VALUES (%s, %s, %s, 'comment');
        """, (user["key"], reaction, comment["key"]))
    elif user_reaction["reaction"] == reaction:
        un = "un"
        cur.execute("""DELETE FROM "like" WHERE key = %s;""",
                    (user_reaction["key"],))
    else:
        cur.execute("""
            UPDATE "like"
            SET date_created = now(), reaction = %s WHERE key = %s;
        """, (reaction, user_reaction["key"]))

    log(
        cur=cur,
        user_key=user["key"],
        action=f"{un}{reaction} comment",
        entity_type="comment",
        entity_key=comment["key"]
    )

    cur.execute("""
        SELECT
            COUNT(CASE WHEN user_key != %s
                AND reaction = 'like' THEN 1 END) AS others_like,
            COUNT(CASE WHEN user_key != %s
                AND reaction = 'dislike' THEN 1 END) AS others_dislike,
            MAX(CASE WHEN user_key = %s THEN reaction END) AS user_reaction
        FROM "like"
        WHERE entity_key = %s;
    """, (user["key"], user["key"], user["key"], comment["key"]))
    reactions = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        **reactions
    })


@bp.post("/comments/<key>/report")
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

    cur.execute("""SELECT * FROM comment WHERE key = %s;""", (key,))
    reported_comment = cur.fetchone()
    if not reported_comment:
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute("""
        INSERT INTO report (reporter_key, reporter_comment,
            tags, entity_key, entity_type)
        VALUES (%s, %s, %s, %s, 'comment') RETURNING *;
    """, (user["key"], comment, tags, reported_comment["key"]))
    report = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="reported comment",
        entity_type="comment",
        entity_key=reported_comment["key"],
        misc={
            "entity_type": "report",
            "entity_key": report["key"]
        }
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
