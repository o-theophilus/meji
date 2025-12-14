from flask import Blueprint, jsonify, request
from psycopg2.extras import Json
from ...postgres import db_open, db_close
from ...log import log
from ...tools import get_session
from .get import get_many


bp = Blueprint("highlight", __name__)


@bp.post("/highlight")
def set_highlight():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "item:edit_highlight" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error":  "unauthorized access"
        })

    key = request.json.get("key")

    if not key:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "key": "This field is required"
        })

    cur.execute("""
        SELECT * FROM item WHERE key::TEXT = %s OR slug = %s;
    """, (key, key))
    item = cur.fetchone()
    if not item:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Item not found"
        })

    if item["status"] != "active":
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "not active"
        })

    cur.execute("SELECT * FROM app WHERE alias = 'highlight';",)
    keys = cur.fetchone()["value"]["item_keys"]
    _from = [*keys]

    if item["key"] in keys:
        keys.remove(item["key"])
    else:
        keys.append(item["key"])

    cur.execute("UPDATE app SET value = %s WHERE alias = 'highlight';",
                (Json({"item_keys": keys}),))

    log(
        cur=cur,
        user_key=user["key"],
        action="edited_highlight",
        entity_key="app",
        entity_type="app",
        misc={
            "from": ", ".join(_from),
            "to": ", ".join(keys)
        }
    )

    items = get_many(cur).json["items"]

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "items": items
    })


@bp.put("/highlight")
def edit_highlight():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "item:edit_highlight" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error":  "unauthorized access"
        })

    new_key = request.json.get("keys")

    if not new_key or type(new_key) is not list:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute("SELECT * FROM app WHERE alias = 'highlight';",)
    keys = cur.fetchone()["value"]["item_keys"]

    if new_key == keys:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error":  "No changes were made"
        })

    cur.execute("UPDATE app SET value = %s WHERE alias = 'highlight';",
                (Json({"item_keys": new_key}),))

    log(
        cur=cur,
        user_key=user["key"],
        action="edited_highlight",
        entity_key="app",
        entity_type="app",
        misc={
            "from": ", ".join(keys),
            "to": ", ".join(new_key)
        }
    )

    items = get_many(cur).json["items"]

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "items": items
    })
