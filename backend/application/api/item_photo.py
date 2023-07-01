from flask import Blueprint, jsonify, request, send_file
from .tools import token_to_user
from . import dd
from .schema import item_schema
from .database import database, query

bp = Blueprint("item_photo", __name__)


@bp.get("/photos/<key>")
@bp.get("/photos/<key>/<thumbnail>")
def get_photo(key, thumbnail=False):
    photo = dd.get(f"/photos/{key}", thumbnail)
    return send_file(photo, mimetype="image/jpg")


@bp.post("/photo_item/<key>")
def post_item(key):
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 401,
            "error": "invalid token"
        })

    if 'file' not in request.files or 'id' not in request.form:
        return jsonify({
            "status": 401,
            "error": "invalid request"
        })

    file = request.files["file"]

    ext = file.filename.split(".")[-1]
    if ext.lower() not in ['jpg', 'png', 'gif']:
        return jsonify({
            "status": 401,
            "error": "invalid file type"
        })

    item = query({"type": "item", "key": key}, db=db)
    if not item:
        return jsonify({
            "status": 401,
            "error": "invalid request"
        })

    photo = {
        "key": dd.add(file),
        "order": len(item["photos"]),
    }

    if len(item["photos"]) == 10:
        return jsonify({
            "status": 401,
            "error": "max image reached"
        })
    item["photos"].append(photo)

    item = database(item)

    return jsonify({
        "status": 200,
        "item": item_schema(item, db)
    })


@bp.put("/photo_item/<key>")
def rearrange(key):
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 401,
            "error": "invalid token"
        })

    if "photos" not in request.json or not request.json["photos"]:
        return jsonify({
            "status": 401,
            "error": "invalid request"
        })

    item = query({"type": "item", "key": key}, db=db)
    if not item:
        return jsonify({
            "status": 401,
            "error": "invalid request"
        })

    photo_keys = request.json["photos"]
    photo_keys = [key.split("/")[-1] for key in photo_keys]

    for photo in item["photos"]:
        photo["order"] = photo_keys.index(photo["key"])

    item = database(item)

    return jsonify({
        "status": 200,
        "item": item_schema(item, db)
    })


@bp.delete("/photo_item/<key>")
def delete(key):
    db = database()

    if (
        "active_photo" not in request.json
        or not request.json["active_photo"]
    ):
        return jsonify({
            "status": 401,
            "error": "invalid request"
        })

    item = query({"type": "item", "key": key}, db=db)
    if not item:
        return jsonify({
            "status": 401,
            "error": "invalid request"
        })

    temp = []
    i = 0

    active_photo = request.json["active_photo"].split("/")[-1]

    for photo in sorted(item["photos"], key=lambda d: d['order']):
        if photo["key"] != active_photo:
            photo["order"] = i
            i += 1
            temp.append(photo)

    dd.rem(active_photo)
    item["photos"] = temp
    item = database(item)

    return jsonify({
        "status": 200,
        "item": item_schema(item, db)
    })
