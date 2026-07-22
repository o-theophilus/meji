from flask import Blueprint, request

from ..tools import log, rate_limit, session
from .get import get_user_like

bp = Blueprint("like", __name__)


@bp.post("/items/<key>/like")
@session(False)
@rate_limit(20, 1)
@log("item")
def like_item(cur, user, key):
    cur.execute("""SELECT * FROM item WHERE key = %s;""", (key,))
    item = cur.fetchone()
    if not item:
        return {
            "error": "Invalid request"
        }, 404

    cur.execute("""
        SELECT * FROM "like" WHERE user_key = %s AND item_key = %s;
    """, (user["key"], item["key"]))
    user_reaction = cur.fetchone()

    if not user_reaction:
        cur.execute("""
            INSERT INTO "like" (user_key, item_key)
            VALUES (%s, %s);
        """, (user["key"], item["key"]))
    else:
        cur.execute("""DELETE FROM "like" WHERE key = %s;""", (
            user_reaction["key"],))

    return {
        "likes": get_user_like(cur, user["key"]),
        "log": {
            "entity_key": item["key"],
            "misc": {
                "action": f"{'un' if user_reaction else ''}like"
            }
        }
    }, 200


@bp.post("/blogs/<key>/like")
@session(True)
@rate_limit(20, 1)
@log("blog")
def like_blog(cur, user, key):
    reaction = request.json.get("reaction")

    cur.execute("""SELECT * FROM blog WHERE key = %s;""", (key,))
    if not cur.fetchone():
        return {
            "error": "Invalid request"
        }, 404

    if reaction not in ["like", "dislike"]:
        return {
            "error": "Invalid request"
        }, 422

    cur.execute("""
        SELECT * FROM "like" WHERE user_key = %s AND blog_key = %s;
    """, (user["key"], key))
    user_reaction = cur.fetchone()

    un = ""
    if not user_reaction:
        cur.execute("""
            INSERT INTO "like" (user_key, reaction, blog_key)
            VALUES (%s, %s, %s);
        """, (user["key"], reaction, key))
    elif user_reaction["reaction"] == reaction:
        un = "un"
        cur.execute("""DELETE FROM "like" WHERE key = %s;""",
                    (user_reaction["key"],))
    else:
        cur.execute("""
            UPDATE "like"
            SET date_created = now(), reaction = %s WHERE key = %s;
        """, (reaction, user_reaction["key"]))

    cur.execute("""
        SELECT
            COUNT(CASE WHEN user_key != %s`
                AND reaction = 'like' THEN 1 END) AS others_like,
            COUNT(CASE WHEN user_key != %s
                AND reaction = 'dislike' THEN 1 END) AS others_dislike,
            MAX(CASE WHEN user_key = %s THEN reaction END) AS user_reaction
        FROM "like"
        WHERE blog_key = %s;
    """, (user["key"], user["key"], user["key"], key))
    reactions = cur.fetchone()

    return {
        **reactions,
        "log": {
            "entity_key": key,
            "misc": {
                "action": f"{un}{reaction}"
            }
        }
    }, 200


@bp.post("/comments/<key>/like")
@session(True)
@rate_limit(20, 1)
@log("comment")
def like(cur, user, key):
    cur.execute("""SELECT * FROM comment WHERE key = %s;""", (key,))
    comment = cur.fetchone()
    if not comment:
        return {
            "error": "Invalid request"
        }, 404

    reaction = request.json.get("reaction")

    if reaction not in ["like", "dislike"]:
        return {
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

    return {
        **reactions,
        "log": {
            "entity_key": key,
            "misc": {
                "action": f"{un}{reaction}"
            }
        }
    }, 200
