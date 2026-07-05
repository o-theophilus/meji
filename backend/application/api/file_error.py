from flask import Blueprint, request

from ..log import log
from ..postgres import db_close, db_open
from ..storage import storage
from ..tools import get_session

bp = Blueprint("file_error", __name__)


@bp.get("/file_error")
def get_file_error(cur=None):
    close_conn = not cur
    if not cur:
        con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        if close_conn:
            db_close(con, cur)
        return session
    user = session["user"]

    if "admin.manage_files" not in user["access"]:
        if close_conn:
            db_close(con, cur)
        return {
            "status": 403,
            "error": "unauthorized access"
        }, 403

    cur.execute("""SELECT photo FROM "user";""")
    users_photo = cur.fetchall()
    users_photo = [x["photo"] for x in users_photo if x["photo"]]
    user_store_photo = storage.get_all("user")
    if '.emptyFolderPlaceholder' in user_store_photo:
        user_store_photo.remove('.emptyFolderPlaceholder')
    cur.execute("""
        SELECT username, name FROM "user"
        WHERE photo IS NOT NULL AND photo <> ALL(%s);
    """, (user_store_photo,))
    users_with_missing_photo = cur.fetchall()

    cur.execute("""SELECT files FROM item;""")
    temp = cur.fetchall()
    item_photo = []
    for x in temp:
        item_photo += x["files"]
    item_store_photo = storage.get_all("item")
    if '.emptyFolderPlaceholder' in item_store_photo:
        item_store_photo.remove('.emptyFolderPlaceholder')
    cur.execute("""
        SELECT slug, name FROM item
        WHERE NOT %s @> files;
    """, (item_store_photo,))
    items_with_missing_photo = cur.fetchall()

    if close_conn:
        db_close(con, cur)
    return {
        "status": 200,
        "unused_item_photo": [
            f"{request.host_url}photo/item/{x}"
            for x in item_store_photo if x not in item_photo],
        "unused_user_photo": [
            f"{request.host_url}photo/user/{x}"
            for x in user_store_photo if x not in users_photo],
        "users": users_with_missing_photo,
        "items": items_with_missing_photo
    }, 200


@bp.delete("/file_error")
def delete_file():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return session
    user = session["user"]

    if "admin.manage_files" not in user["access"]:
        db_close(con, cur)
        return {
            "status": 403,
            "error": "unauthorized access"
        }, 403

    photos = request.json.get("photos")
    entity = request.json.get("entity")

    if (
        not photos or type(photos) is not list
        or not entity or entity not in ["user", "item"]
    ):
        db_close(con, cur)
        return {
            "status": 422,
            "error": "Invalid request"
        }, 422

    for x in photos:
        storage.delete(x.split("/")[-1], entity)

    log(
        cur=cur,
        user_key=user["key"],
        action="deleted unused photo(s)",
        entity_type="app",
        entity_key="maintenance",
        misc={
            "photo(s)": photos,
            "from": entity
        }
    )

    db_close(con, cur)
    return {
        "status": 200
    }, 200
