from flask import Blueprint, jsonify, request
from .tools import reserved_words, token_to_user, now
from .schema import item_schema
import re
from uuid import uuid4
from .database import database, query
from .storage import storage

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

    item = database({
        "key": uuid4().hex,
        "v": uuid4().hex,
        "type": "item",
        "status": "draft",
        "date_c": now(),
        "date_u": now(),

        "name": request.json["name"],
        "slug": slug,
        "price": 0,
        "old_price": 0,
        "info": '',
        "photos": [],
        "tags": [],
        "ads": {},
        "variation": {},

        "available_quantity": 0,
        "feedbacks": [],
    })

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
        elif item["status"] == "live":
            item["status"] = "draft"

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
        if not request.json["status"] or request.json["status"] not in [
                'live', 'draft', 'delete']:
            error["status"] = "invalid request"
        elif request.json["status"] == "live" and len(item["photos"]) == 0:
            error["status"] = "add photo"
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


@bp.post("/photo/<key>")
def post_many_photo(key):
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
    if 'files' not in request.files or not item:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    files = []
    bad_files = []
    for x in request.files.getlist("files"):
        media, format = x.content_type.split("/")
        if media != "image" or format in ['svg+xml', 'x-icon']:
            bad_files.append(x)
        else:
            files.append(x)

    if files == []:
        return jsonify({
            "status": 400,
            "error": ', '.join([x.name for x in bad_files])
        })

    trim = 10 - len(item["photos"])
    bad_files += files[trim:]
    files = files[:trim]

    for x in files:
        item["photos"].append(storage(x))
    database(item)

    return jsonify({
        "status": 200,
        "item": item_schema(item, db),
        "error": ', '.join([x.name for x in bad_files])
    })


@bp.put("/photo/<key>")
def arrange_photo(key):

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
def delete_photo(key):

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

    file_name = request.json["active_photo"].split("/")[-1]
    item = query({"type": "item", "key": key}, db=db)

    if (
        not item
        or "active_photo" not in request.json
        or not request.json["active_photo"]
        or file_name not in item["photos"]
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    item["photos"].remove(file_name)
    if len(item["photos"]) == 0 and item["status"] == "live":
        item["status"] = "draft"
    storage(file_name, delete=True)
    database(item)

    return jsonify({
        "status": 200,
        "item": item_schema(item, db)
    })
