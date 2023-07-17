from flask import Blueprint, jsonify, request, send_file
from .tools import token_to_user
from .schema import user_schema, item_schema
from .database import database, query
from .storage import storage

bp = Blueprint("photo", __name__)


@bp.get("/photos/<key>")
@bp.get("/photos/<key>/<thumbnail>")
def get_photo(key, thumbnail=False):
    photo = storage(key, thumbnail=thumbnail)
    return send_file(photo, mimetype="image/jpg")


@bp.post("/photo/<key>")
def post_many(key):
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "admin" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorised access"
        })

    entity = query({"key": key}, db=db)
    if (
        'files' not in request.files
        or not entity
        or entity["type"] not in ["item", "user"]
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    files = []
    bad_files = []
    for file in request.files.getlist("files"):
        media, format = file.content_type.split("/")
        if media != "image" or format in ['svg+xml', 'x-icon']:
            bad_files.append(file)
        else:
            files.append(file)

    if files == []:
        return jsonify({
            "status": 400,
            "error": ', '.join([x.name for x in bad_files])
        })

    type_ = entity["type"]

    if type_ == "item":
        trim = 10 - len(entity["photos"])
        bad_files += files[trim:]
        files = files[:trim]

        for file in files:
            entity["photos"].append(storage(file))

    else:
        bad_files += files[1:]
        if entity["photo"]:
            storage(entity["photo"], delete=True)
        entity["photo"] = storage(files[0])

    database(entity)

    if type_ == "item":
        entity = item_schema(entity, db)
    else:
        entity = user_schema(entity, db)

    return jsonify({
        "status": 200,
        type_: entity,
        "error": ', '.join([x.name for x in bad_files])
    })


@bp.put("/photo/<key>")
def arrange(key):

    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "admin" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorised access"
        })

    def fix(arr):
        return [p.split("/")[-1] for p in arr]

    item = query({"type": "item", "key": key}, db=db)
    if (
        not item
        or "photos" not in request.json
        or type(request.json["photos"]) != list
        or set(item["photos"]) != set(fix(request.json["photos"]))
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    item["photos"] = fix(request.json["photos"])
    database(item)

    return jsonify({
        "status": 200,
        "item": item_schema(item, db)
    })


@bp.delete("/photo/<key>")
def delete(key):

    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "admin" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorised access"
        })

    def fix(p):
        return p.split("/")[-1]

    entity = query({"key": key}, db=db)
    if not entity or entity["type"] not in ["item", "user"]:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    type_ = entity["type"]
    file_name = None

    if type_ == "item":
        if (
            "active_photo" not in request.json
            or not request.json["active_photo"]
            or fix(request.json["active_photo"]) not in entity["photos"]
        ):
            return jsonify({
                "status": 400,
                "error": "invalid request"
            })

        file_name = fix(request.json["active_photo"])
        entity["photos"].remove(file_name)

    else:
        file_name = entity["photo"]
        entity["photo"] = None

    storage(file_name, delete=True)
    database(entity)

    if type_ == "item":
        entity = item_schema(entity, db)
    else:
        entity = user_schema(entity, db)

    return jsonify({
        "status": 200,
        type_: entity,
    })
