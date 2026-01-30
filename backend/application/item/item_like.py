from flask import Blueprint, jsonify
from ..tools import get_session
from ..postgres import db_close, db_open
from ..log import log

bp = Blueprint("item_like", __name__)


@bp.post("/item/like/<key>")
def like_item(key):
    con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute("""SELECT * FROM item WHERE key = %s;""", (key,))
    item = cur.fetchone()
    if not item:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute("""
        SELECT * FROM "like"
        WHERE user_key = %s AND item_key = %s;
    """, (user["key"], item["key"]))
    user_reaction = cur.fetchone()

    if not user_reaction:
        cur.execute("""
            INSERT INTO "like" (user_key, item_key, reaction)
            VALUES (%s, %s, 'like');
        """, (user["key"], item["key"]))
    else:
        cur.execute("""DELETE FROM "like" WHERE key = %s;""", (
            user_reaction["key"],))

    log(
        cur=cur,
        user_key=user["key"],
        action=f"{'un' if user_reaction else ''}like item",
        entity_key=item["key"],
        entity_type="item"
    )

    cur.execute("""
        SELECT "like".item_key
        FROM "like"
        LEFT JOIN item ON "like".item_key = item.key
        WHERE
            "like".user_key = %s
            AND "like".item_key IS NOT NULL
            AND item.status = 'active'
    ;""", (user["key"],))
    likes = cur.fetchall()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "likes": [x["item_key"] for x in likes]
    })
