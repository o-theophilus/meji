from flask import Blueprint, jsonify, request
from ..tools import get_session
from ..postgres import db_open, db_close
from ..storage import storage
from ..log import log
from .get import item_schema

bp = Blueprint("item_file", __name__)


@bp.post("/item/file/<key>")
def add_file(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "item:edit_file" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute('SELECT * FROM item WHERE key = %s;', (key,))
    item = cur.fetchone()
    if 'files' not in request.files or not item:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    error = ""
    files = []

    for x in request.files.getlist("files"):
        err = ""
        if x.content_type not in ['image/jpeg', 'image/png']:
            err = f"{x.filename} => invalid file"

        if err:
            error = f"{error}, {err}" if error else err
        else:
            files.append(x)

    if files == []:
        if not error:
            error = "no file"
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": error
        })

    file_names = []
    for x in files:
        filename = storage.save(x, "item")
        file_names.append(filename)

    cur.execute("""
        UPDATE item
        SET files = %s
        WHERE key = %s
        RETURNING *;
    """, (
        item["files"] + file_names,
        item["key"]
    ))
    item = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="added photo to item",
        entity_key=item["key"],
        entity_type="item",
        misc={
            "added": ", ".join(file_names),
            "error": error
        }
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "item": item_schema(item),
        "error": error
    })


@bp.put("/item/file/<key>")
def order_delete_file(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "item:edit_file" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute('SELECT * FROM item WHERE key = %s;', (key,))
    item = cur.fetchone()

    files = request.json.get("files")

    if not item or type(files) is not list:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    files = [p.split("/")[-1] for p in files]

    if not all(x in item["files"] for x in files):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    for x in item["files"]:
        if x not in files:
            storage.delete(x, "item")

    log(
        cur=cur,
        user_key=user["key"],
        action="edited item photo",
        entity_key=item["key"],
        entity_type="item",
        misc={
            "from": item["files"],
            "to": files
        }
    )

    cur.execute("""
        UPDATE item
        SET files = %s
        WHERE key = %s
        RETURNING *;
    """, (
        files,
        item["key"]
    ))
    item = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "item": item_schema(item)
    })
