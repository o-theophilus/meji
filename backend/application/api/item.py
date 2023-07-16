from flask import Blueprint, jsonify, request
from .tools import reserved_words, token_to_user, now
from .schema import item_schema, item_template
import re
from uuid import uuid4
from .database import database, query
from . import storage

bp = Blueprint("item", __name__)


@bp.post("/item")
def add_new():
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

    if "name" not in request.json or not request.json["name"]:
        return jsonify({
            "status": 400,
            "error": "this field is required"
        })

    slug = re.sub('-+', '-', re.sub(
        '[^a-zA-Z0-9]', '-', request.json["name"].lower()))

    item = query({"type": "item", "slug": slug}, db=db)
    if item or slug in reserved_words:
        slug = f"{slug}-{str(uuid4().hex)[:10]}"

    item = database(item_template(
        request.json["name"],
        slug
    ))

    return jsonify({
        "status": 200,
        "item": item_schema(item, db)
    })


@bp.put("/item/<key>")
def edit_item(key):
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

    item = query({"type": "item", "key": key}, db=db)
    if not item:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = {}

    if "name" in request.json:
        if not request.json["name"]:
            error["name"] = "this field is required"
        else:
            item["name"] = request.json["name"]

            slug = re.sub('-+', '-', re.sub(
                '[^a-zA-Z0-9]', '-', request.json["name"].lower()))
            slug_in_use = query({"type": "item", "slug": slug}, db=db)
            if ((slug_in_use and slug_in_use['key'] != item["key"])
                    or slug in reserved_words):
                slug = f"{slug}-{str(uuid4().hex)[:10]}"
            item["slug"] = slug

    if "price" in request.json:
        item["price"] = None

        if request.json["price"]:
            if (
                type(request.json["price"]) not in [int, float]
                or request.json["price"] < 0
            ):
                error["price"] = "please enter a valid price"
            else:
                item["price"] = request.json["price"]

    if "old_price" in request.json:
        item["old_price"] = None

        if item["price"] and request.json["old_price"]:
            if (
                type(request.json["old_price"]) not in [int, float]
                or request.json["old_price"] < 0
            ):
                error["old_price"] = "please enter a valid price"
            elif request.json["old_price"] <= request.json["price"]:
                error["old_price"] = 'old price should be greater than price'
            else:
                item["old_price"] = request.json["old_price"]

    if "info" in request.json:
        item["info"] = request.json["info"]

    if "variation" in request.json:
        if type(request.json["variation"]) != dict:
            error["variation"] = "this field is required"
        else:
            variation = request.json["variation"]
            for key in variation:
                if type(variation[key]) != list or len(variation[key]) == 0:
                    del variation[key]
            item["variation"] = variation

    if "tags" in request.json:
        if type(request.json["tags"]) != list:
            error["tags"] = "this field is required"
        else:
            item["tags"] = request.json["tags"]

    if "status" in request.json:
        if not request.json["status"]:
            error["status"] = "this field is required"
        elif request.json["status"] == "live" and len(item["photos"]) == 0:
            error["status"] = "no photo"
        elif request.json["status"] == "live" and not item["price"]:
            error["status"] = "add price"
        else:
            item["status"] = request.json["status"]

    if error != {}:
        return jsonify({
            "status": 400,
            **error
        })

    item["date_u"] = now()
    database(item)

    return jsonify({
        "status": 200,
        "item": item_schema(item, db)
    })


# Photo #########################


@bp.post("/photo_item/<key>")
def post_item(key):
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if 'file' not in request.files or 'id' not in request.form:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    file = request.files["file"]

    ext = file.filename.split(".")[-1]
    if ext.lower() not in ['jpg', 'png', 'gif']:
        return jsonify({
            "status": 400,
            "error": "invalid file type"
        })

    item = query({"type": "item", "key": key}, db=db)
    if not item:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    photo = {
        "key": storage(file),
        "order": len(item["photos"]),
    }

    if len(item["photos"]) == 10:
        return jsonify({
            "status": 400,
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
            "status": 400,
            "error": "invalid token"
        })

    if "photos" not in request.json or not request.json["photos"]:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    item = query({"type": "item", "key": key}, db=db)
    if not item:
        return jsonify({
            "status": 400,
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
def delete_(key):
    db = database()

    if (
        "active_photo" not in request.json
        or not request.json["active_photo"]
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    item = query({"type": "item", "key": key}, db=db)
    if not item:
        return jsonify({
            "status": 400,
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

    storage.rem(active_photo)
    item["photos"] = temp
    item = database(item)

    return jsonify({
        "status": 200,
        "item": item_schema(item, db)
    })
