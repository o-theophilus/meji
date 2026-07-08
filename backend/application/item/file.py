from flask import Blueprint, request

from ..storage import storage
from ..tools import item_schema, log, rate_limit, session

bp = Blueprint("item_file", __name__)


@bp.post("/items/<key>/file")
@session(True)
@rate_limit(20, 1)
@log("item")
def add_file(cur, user, key):
    if "item.edit_file" not in user["access"]:
        return {
            "status": 403,
            "error": "unauthorized access"
        }, 403

    cur.execute('SELECT * FROM item WHERE key = %s;', (key,))
    item = cur.fetchone()
    if not item:
        return {
            "status": 404,
            "error": "Invalid request"
        }, 404

    if 'files' not in request.files:
        return {
            "status": 422,
            "error": "Invalid request"
        }, 422

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
        return {
            "status": 422,
            "error": error
        }, 422

    file_names = []
    for x in files:
        filename = storage.save(x, item["name"], "item", True)
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

    return {
        "status": 200,
        "item": item_schema(item),
        "error": error,
        "log": {
            "entity_key": item["key"],
            "misc": {
                "added": ", ".join(file_names),
                "error": error
            }
        }
    }, 200


@bp.put("/items/<key>/file")
@session(True)
@rate_limit(20, 1)
@log("item")
def order_delete_file(cur, user, key):
    if "item.edit_file" not in user["access"]:
        return {
            "status": 403,
            "error": "unauthorized access"
        }, 403

    cur.execute('SELECT * FROM item WHERE key = %s;', (key,))
    item = cur.fetchone()
    if not item:
        return {
            "status": 404,
            "error": "Invalid request"
        }, 404

    files = request.json.get("files")
    if not item or type(files) is not list:
        return {
            "status": 422,
            "error": "Invalid request"
        }, 422

    files = [p.split("/")[-1] for p in files]
    if not all(x in item["files"] for x in files):
        return {
            "status": 422,
            "error": "Invalid request"
        }, 422

    # for x in item["files"]:
    #     if x not in files:
    #         storage.delete(x, "item")

    previous = item
    cur.execute("""
        UPDATE item SET files = %s
        WHERE key = %s RETURNING *;
    """, (
        files,
        item["key"]
    ))
    item = cur.fetchone()

    return {
        "status": 200,
        "item": item_schema(item),
        "": {
            "entity_key": item["key"],
            "misc": {
                "from": previous["files"],
                "to": item["files"],
            }
        }
    }, 200
