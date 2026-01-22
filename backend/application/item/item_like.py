from flask import Blueprint, jsonify, request
from ..tools import get_session
from ..postgres import db_close, db_open
from ..log import log

bp = Blueprint("item_like", __name__)


@bp.post("/item/like")
def like_item():
    con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    entity_key = request.json.get("entity_key")

    cur.execute("""
        SELECT * FROM item WHERE key = %s;
    """, (entity_key,))
    if not cur.fetchone():
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute("""
        SELECT * FROM "like"
        WHERE user_key = %s AND entity_type = 'item' AND entity_key = %s;
    """, (user["key"], entity_key))
    like = cur.fetchone()

    if not like:
        cur.execute("""
            INSERT INTO "like" (user_key, entity_key, entity_type, reaction)
            VALUES (%s, %s, 'item', 'like');
        """, (user["key"], entity_key,))
    else:
        cur.execute("""DELETE FROM "like" WHERE key = %s;""", (like["key"],))

    log(
        cur=cur,
        user_key=user["key"],
        action="unlike" if like else "like",
        entity_key=entity_key,
        entity_type="item"
    )

    cur.execute("""
        SELECT entity_key  FROM "like"
        WHERE user_key = %s AND entity_type = 'item'
    ;""", (user["key"],))
    likes = cur.fetchall()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "likes": [x["entity_key"] for x in likes]
    })
