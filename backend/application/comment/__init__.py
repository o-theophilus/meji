from flask import Blueprint, request

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
        return session
    user = session["user"]

    cur.execute("""SELECT * FROM comment WHERE key = %s;""", (key,))
    comment = cur.fetchone()
    if not comment:
        db_close(con, cur)
        return {
            "status": 404,
            "error": "Invalid request"
        }, 404

    _comment = request.json.get("comment", "").strip()
    misc = {}

    if comment["user_key"] != user["key"]:
        if "comment.delete_others" not in user["access"]:
            db_close(con, cur)
            return {
                "status": 403,
                "error": "unauthorized access"
            }, 403

        error = {}
        if not _comment:
            error["comment"] = "This field is required"
        elif len(_comment) > 500:
            error["comment"] = "This field cannot exceed 500 characters"
        if error:
            db_close(con, cur)
            return {
                "status": 422,
                **error
            }, 422

        misc["comment"] = _comment

    cur.execute("DELETE FROM comment WHERE key = %s;", (comment["key"],))

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
        return session
    user = session["user"]

    cur.execute("""SELECT * FROM comment WHERE key = %s;""", (key,))
    comment = cur.fetchone()
    if not comment:
        db_close(con, cur)
        return {
            "status": 404,
            "error": "Invalid request"
        }, 404

    reaction = request.json.get("reaction")

    if reaction not in ["like", "dislike"]:
        db_close(con, cur)
        return {
            "status": 422,
            "error": "Invalid request"
        }, 422

    cur.execute("""
        SELECT * FROM "like" WHERE user_key = %s AND comment_key = %s;
    """, (user["key"], comment["key"]))
    user_reaction = cur.fetchone()

    un = ""
    if not user_reaction:
        cur.execute("""
            INSERT INTO "like" (user_key, reaction, comment_key)
            VALUES (%s, %s, %s);
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
        WHERE comment_key = %s;
    """, (user["key"], user["key"], user["key"], comment["key"]))
    reactions = cur.fetchone()

    db_close(con, cur)
    return {
        "status": 200,
        **reactions
    }, 200


@bp.post("/comments/<key>/report")
def report(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return session
    user = session["user"]

    cur.execute("""SELECT * FROM comment WHERE key = %s;""", (key,))
    comment = cur.fetchone()
    if not comment:
        return {
            "status": 404,
            "error": "Comment not found"
        }, 404

    _comment = request.json.get("comment", "").strip()
    tags = request.json.get("tags")

    if type(tags) is not list:
        db_close(con, cur)
        return {
            "status": 422,
            "error": "Invalid request"
        }, 422

    error = {}
    if not _comment:
        error["comment"] = "This field is required"
    elif len(_comment) > 500:
        error["comment"] = "This field cannot exceed 500 characters"
    if error:
        db_close(con, cur)
        return {
            "status": 422,
            **error
        }, 422

    cur.execute("""
        INSERT INTO report (reporter_key, reporter_comment, tags,
            reported_key, reported_comment_key)
        VALUES (%s, %s, %s, %s, %s) RETURNING *;
    """, (
        user["key"], _comment, tags,
        comment["user_key"], comment["key"])
    )
    report = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="reported comment",
        entity_type="comment",
        entity_key=comment["key"],
        misc={
            "report_key": report["key"]
        }
    )

    db_close(con, cur)
    return {
        "status": 200
    }, 200
