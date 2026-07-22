from flask import Blueprint, request

from ..storage import storage
from ..tools import log, rate_limit, session

bp = Blueprint("file_error", __name__)


def file_error(cur):
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

    return {
        "unused_item_photo": [
            f"{request.host_url}photo/item/{x}"
            for x in item_store_photo if x not in item_photo],
        "unused_user_photo": [
            f"{request.host_url}photo/user/{x}"
            for x in user_store_photo if x not in users_photo],
        "users": users_with_missing_photo,
        "items": items_with_missing_photo
    }


@bp.get("/file_error")
@session(True)
@rate_limit(20, 1)
def _get_file_error(cur, user):
    if "admin.manage_files" not in user["access"]:
        return {
            "error": "unauthorized access"
        }, 403

    return file_error(cur), 200


@bp.delete("/file_error")
@session(True)
@rate_limit(20, 1)
@log("app")
def delete_file(cur, user):
    if "admin.manage_files" not in user["access"]:
        return {
            "error": "unauthorized access"
        }, 403

    photos = request.json.get("photos")
    entity = request.json.get("entity")

    if (
        not photos or type(photos) is not list
        or not entity or entity not in ["user", "item"]
    ):
        return {
            "error": "Invalid request"
        }, 422

    for x in photos:
        storage.delete(x.split("/")[-1], entity)

    return {
        "log": {
            "misc": {
                "photo(s)": photos,
                "from": entity
            }
        }
    }, 200
