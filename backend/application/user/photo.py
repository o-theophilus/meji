from flask import Blueprint, request

from ..storage import storage
from ..tools import log, rate_limit, session, user_schema

bp = Blueprint("user_photo", __name__)


@bp.put("/user/photo")
@session(True)
@rate_limit(20, 1)
@log("user")
def add_photo(cur, user):
    if 'file' not in request.files:
        return {
            "error": "Invalid request"
        }, 422

    file = request.files["file"]
    if file.content_type not in ['image/jpeg', 'image/png']:
        return {
            "error": "invalid file"
        }, 422

    if user["photo"]:
        storage.delete(user["photo"], "user")

    file_name = storage.save(file, user["username"], "user")

    previous = user
    cur.execute("""
        UPDATE "user" SET photo = %s
        WHERE key = %s RETURNING *;
    """, (
        file_name,
        user["key"]
    ))
    user = cur.fetchone()

    return {
        "user": user_schema(user),
        "log": {
            "entity_key": user["key"],
            "misc": {
                "from": previous["photo"],
                "to": user["photo"],
            }
        }
    }, 200


@bp.delete("/user/photo")
@session(True)
@rate_limit(20, 1)
@log("user")
def delete_photo(cur, user):
    if not user["photo"]:
        return {
            "error": "Invalid request"
        }, 422

    storage.delete(user["photo"], "user")

    previous = user
    cur.execute("""
        UPDATE "user"
        SET photo = NULL
        WHERE key = %s
        RETURNING *;
    """, (user["key"],))
    user = cur.fetchone()

    return {
        "user": user_schema(user),
        "log": {
            "entity_key": user["key"],
            "misc": {
                "from": previous["photo"],
                "to": None,
            }
        }
    }, 200
