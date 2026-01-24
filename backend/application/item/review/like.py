from flask import Blueprint, jsonify, request
from datetime import datetime, timezone
from ...tools import get_session
from ...postgres import db_close, db_open
from ...log import log

bp = Blueprint("review_like", __name__)


@bp.post("/review/like/<key>")
def like_review(key):
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
        SELECT * FROM "like"
        WHERE user_key = %s AND review_key = %s;
    """, (user["key"], review["key"]))
    user_reaction = cur.fetchone()

    un = ""
    if not user_reaction:
        cur.execute("""
            INSERT INTO "like" (user_key, review_key, reaction)
            VALUES (%s, %s, %s);
        """, (user["key"], review["key"], reaction))
    elif user_reaction["reaction"] == reaction:
        un = "un"
        cur.execute("""DELETE FROM "like" WHERE key = %s;""",
                    (user_reaction["key"],))
    else:
        cur.execute("""
            UPDATE "like"
            SET date_created = %s, reaction = %s WHERE key = %s;
        """, (datetime.now(timezone.utc), reaction, user_reaction["key"]))

    # TODO: make all other log action more (full) descriptive
    log(
        cur=cur,
        user_key=user["key"],
        action=f"{un}{reaction} review",
        entity_key=review["key"],
        entity_type="review"
    )

    cur.execute("""
        SELECT
            COUNT(CASE WHEN user_key != %s
                AND reaction = 'like' THEN 1 END) AS others_like,
            COUNT(CASE WHEN user_key != %s
                AND reaction = 'dislike' THEN 1 END) AS others_dislike,
            MAX(CASE WHEN user_key = %s THEN reaction END) AS user_reaction
        FROM "like"
        WHERE review_key = %s
    """, (user["key"], user["key"], user["key"], review["key"]))
    reactions = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        **reactions
        # FIXME: use the below instead
        # "others_like": reactions['others_like'],
        # "others_dislike": reactions['others_dislike'],
        # "user_reaction": reactions['user_reaction']
    })
