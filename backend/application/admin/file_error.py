from flask import Blueprint, jsonify, request
from ..postgres import db_open, db_close
from ..log import log
from ..tools import get_session
from ..storage import storage


bp = Blueprint("file_error", __name__)


@bp.get("/file_error")
def get_file_error():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "admin:manage_files" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute("""SELECT photo FROM "user";""")
    users_photo = cur.fetchall()
    users_photo = [x["photo"] for x in users_photo if x["photo"]]
    user_store_photo = storage.get_all("user")
    cur.execute("""
        SELECT username, name FROM "user"
        WHERE photo IS NOT NULL AND NOT photo = ANY(%s);
    """, (user_store_photo,))
    users_with_missing_photo = cur.fetchall()

    cur.execute("""SELECT files FROM item;""")
    temp = cur.fetchall()
    items_photo = []
    for x in temp:
        items_photo += x["files"]
    item_store_photo = storage.get_all("item")
    cur.execute("""
        SELECT slug, name FROM item
        WHERE NOT ARRAY[%s] @> files;
    """, (item_store_photo,))
    items_with_missing_photo = cur.fetchall()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "unused_item_photo": [f"{request.host_url}photo/item/{x}"
                   for x in item_store_photo if x not in items_photo],
        "unused_user_photo": [f"{request.host_url}photo/user/{x}"
                   for x in user_store_photo if x not in users_photo],
        "users": users_with_missing_photo,
        "items": items_with_missing_photo
    })


@bp.delete("/file_error")
def delete_file():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "admin:manage_files" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    photos = request.json.get("photos")
    entity = request.json.get("entity")

    if (
        not photos or type(photos) is not list
        or not entity or entity not in ["user", "item"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    for x in photos:
        storage.delete(x.split("/")[-1], entity)

    log(
        cur=cur,
        user_key=user["key"],
        action="deleted unuded photo(s)",
        entity_key="app",
        entity_type="photo",
        misc={
            "photo(s)": photos,
            "from": entity
        }
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
