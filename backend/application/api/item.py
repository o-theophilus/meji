from flask import Blueprint, jsonify, request
from .tools import reserved_words, token_to_user, now
from .schema import item_schema, item_template
import re
from uuid import uuid4
from .database import database, query
from . import storage

bp = Blueprint("item", __name__)


@bp.post("/item")
def post():
    data = database()

    user = token_to_user(data)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    if "admin" not in user["roles"]:
        return jsonify({
            "status": 102,
            "message": "unauthorised access"
        })

    error = {}
    if "name" not in request.json or not request.json["name"]:
        error["name"] = "This field is required"

    if "price" not in request.json or not request.json["price"]:
        error["price"] = "This field is required"
    elif type(request.json["price"]) != int or request.json["price"] < 1:
        error["price"] = "Please enter a valid price"

    if "old_price" in request.json and request.json["old_price"]:
        if (type(request.json["old_price"]) != int or
           request.json["old_price"] < 0):
            error["old_price"] = "Please enter a valid price"
        if (request.json["price"] >= request.json["old_price"]):
            error["old_price"] = 'Old price should be greater than Price'

    if error != {}:
        return jsonify({
            "status": 201,
            "message": error
        })

    alias = re.sub('-+', '-', re.sub(
        '[^a-zA-Z0-9]', '-', request.json["name"].lower()))

    item = query("item", "alias", alias, data)
    if item or alias in reserved_words:
        alias = f"{alias}-{str(uuid4().hex)[:10]}"

    old_price = None
    if "old_price" in request.json and request.json["old_price"]:
        old_price = request.json["old_price"]
    desc = None
    if "desc" in request.json and request.json["desc"]:
        desc = request.json["desc"]
    spec = None
    if "spec" in request.json and request.json["spec"]:
        spec = request.json["spec"]

    database(item_template(
        request.json["name"],
        alias,
        request.json["price"],
        old_price,
        desc,
        spec
    ))

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "item": item_schema(item, data)
        }
    })


@bp.put("/item/<key>")
def put(key):
    data = database()

    user = token_to_user(data)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    if "admin" not in user["roles"]:
        return jsonify({
            "status": 102,
            "message": "unauthorised access"
        })

    item = query("item", "key", key, data)
    if not item:
        return jsonify({
            "status": 400,
            "message": "invalid request"
        })

    error = {}

    if "name" not in request.json or not request.json["name"]:
        error["name"] = "This field is required"

    if "price" not in request.json or not request.json["price"]:
        error["price"] = "This field is required"
    elif type(request.json["price"]) != int or request.json["price"] < 1:
        error["price"] = "Please enter a valid price"

    if "old_price" in request.json and request.json["old_price"]:
        if (type(request.json["old_price"]) != int or
           request.json["old_price"] < 0):
            error["old_price"] = "Please enter a valid price"
        if (request.json["price"] >= request.json["old_price"]):
            error["old_price"] = 'Old price should be greater than Price'

    if error != {}:
        return jsonify({
            "status": 201,
            "message": error
        })

    alias = re.sub('-+', '-', re.sub(
        '[^a-zA-Z0-9]', '-', request.json["name"].lower()))

    alias_in_use = query("item", "alias", alias, data)

    if (
        (alias_in_use and alias_in_use['key'] != item["key"])
        or alias in reserved_words
    ):
        alias = f"{alias}-{str(uuid4().hex)[:10]}"

    item["alias"] = alias
    item["name"] = request.json["name"]
    item["price"] = request.json["price"]
    item["date_u"] = now()

    if "old_price" in request.json and request.json["old_price"]:
        item["old_price"] = request.json["old_price"]
    if "desc" in request.json and request.json["desc"]:
        item["desc"] = request.json["desc"]
    if "spec" in request.json and request.json["spec"]:
        item["spec"] = request.json["spec"]

    database(item)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "item": item_schema(item, data)
        }
    })


@bp.put("/item_variation/<key>")
def variation(key):
    data = database()

    user = token_to_user(data)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    if "admin" not in user["roles"]:
        return jsonify({
            "status": 102,
            "message": "unauthorised access"
        })

    item = query("item", "key", key, data)
    if not item:
        return jsonify({
            "status": 400,
            "message": "invalid request"
        })

    if "variation_options" not in request.json:
        return jsonify({
            "status": 201,
            "message": "This field is required"
        })

    variation = request.json["variation_options"]
    if variation != {}:
        for key in variation:
            if len(variation[key]) < 1:
                return jsonify({
                    "status": 201,
                    "message":  'Empty property value'
                })

    item["variation_options"] = variation
    database(item)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "item": item_schema(item, data)
        }
    })


@bp.put("/item_/<key>")
def change_status(key):
    data = database()

    user = token_to_user(data)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    if "admin" not in user["roles"]:
        return jsonify({
            "status": 102,
            "message": "unauthorised access"
        })

    if "status" not in request.json or not request.json["status"]:
        return jsonify({
            "status": 400,
            "message": "invalid request"
        })

    item = query("item", "key", key, data)
    if not item:
        return jsonify({
            "status": 400,
            "message": "invalid request"
        })

    if request.json["status"] == "live" and item["photos"] == []:
        return jsonify({
            "status": 201,
            "message": "no photo"
        })

    item["status"] = request.json["status"]
    item["date_u"] = now()

    item = database(item)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "item": item_schema(item, data)
        }
    })


@bp.delete("/item/<key>")
def delete(key):
    data = database()

    user = token_to_user(data)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    if "admin" not in user["roles"]:
        return jsonify({
            "status": 102,
            "message": "unauthorised access"
        })

    item = query("item", "key", key, data)
    if not item:
        return jsonify({
            "status": 400,
            "message": "invalid request"
        })

    database.rem(key)

    return jsonify({
        "status": 200,
        "message": "successful"
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
