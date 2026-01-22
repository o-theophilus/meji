from flask import Blueprint, jsonify, request
from datetime import datetime, timezone
from ...tools import get_session
from ...postgres import db_close, db_open
from ...log import log

bp = Blueprint("review_like", __name__)


@bp.post("/review/like")
def like_review():
    con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    entity_key = request.json.get("entity_key")
    reaction = request.json.get("reaction")

    cur.execute("""
        SELECT * FROM review WHERE key = %s;
    """, (entity_key,))
    if not cur.fetchone() or reaction not in ["like", "dislike"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute("""
        SELECT * FROM "like"
        WHERE user_key = %s AND entity_type = 'review' AND entity_key = %s;
    """, (user["key"], entity_key))
    others_like = cur.fetchone()

    un = ""
    if not others_like:
        cur.execute("""
            INSERT INTO "like" (user_key, entity_type, entity_key, reaction)
            VALUES (%s, 'review', %s,  %s);
        """, (user["key"],  entity_key, reaction))
    elif others_like["reaction"] == reaction:
        un = "un"
        cur.execute("""DELETE FROM "like" WHERE key = %s;""",
                    (others_like["key"],))
    else:
        cur.execute("""
            UPDATE "like"
            SET date_created = %s, reaction = %s WHERE key = %s;
        """, (datetime.now(timezone.utc), reaction, others_like["key"]))

    # TODO: make all other log action more (full) descriptive
    log(
        cur=cur,
        user_key=user["key"],
        action=f"{un}{reaction} review",
        entity_key=entity_key,
        entity_type="review"
    )

    cur.execute("""
        WITH entity_likes AS (
            SELECT reaction, user_key
            FROM "like"
            WHERE entity_type = 'review' AND entity_key = %s
        )
        SELECT
            COUNT(CASE WHEN user_key != %s
                AND reaction = 'like' THEN 1 END) AS others_like,
            COUNT(CASE WHEN user_key != %s
                AND reaction = 'dislike' THEN 1 END) AS others_dislike,
            MAX(CASE WHEN user_key = %s THEN reaction END) AS user_reaction
        FROM entity_likes
    """, (entity_key, user["key"], user["key"], user["key"]))
    reactions = cur.fetchone()
    print(reactions)

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "others_like": reactions['others_like'],
        "others_dislike": reactions['others_dislike'],
        "user_reaction": reactions['user_reaction']
    })
