from flask import Blueprint, jsonify, request
from .tools import reserved_words, token_to_user, now
from .schema import item_schema
import re
from uuid import uuid4
from .database import database, query
from .storage import storage
from .log import log_template

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

    if "item:add" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
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
    })

    database(log_template(
        user["key"],
        "created",
        item["key"],
        "item"
    ), db_name="log")

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

    item = query({"type": "item", "key": key}, db=db)
    if not item:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = {}

    if "status" in request.json:
        if "item:edit_status" not in user["roles"]:
            error["status"] = "unauthorized access"
        elif (
            not request.json["status"]
            or request.json["status"] not in ['live', 'draft', 'delete']
        ):
            error["status"] = "invalid request"
        elif request.json["status"] == "live" and len(item["photos"]) == 0:
            error["status"] = "add photo"
        elif request.json["status"] == "live" and not item["price"]:
            error["status"] = "add price"
        else:
            item["status"] = request.json["status"]

    if "name" in request.json:
        if "item:edit_name" not in user["roles"]:
            error["name"] = "unauthorized access"
        elif not request.json["name"]:
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

    if "tags" in request.json:
        if "item:edit_tag" not in user["roles"]:
            error["tag"] = "unauthorized access"
        elif type(request.json["tags"]) is not list:
            error["tags"] = "this field is required"
        else:
            item["tags"] = request.json["tags"]

    if "price" in request.json:
        item["price"] = None

        if "item:edit_price" not in user["roles"]:
            error["price"] = "unauthorized access"
        elif request.json["price"]:
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

        if "item:edit_price" not in user["roles"]:
            error["price"] = "unauthorized access"
        elif item["price"] and request.json["old_price"]:
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
        if "item:edit_info" not in user["roles"]:
            error["info"] = "unauthorized access"
        else:
            item["info"] = request.json["info"]

    if "variation" in request.json:
        if "item:edit_variation" not in user["roles"]:
            error["variation"] = "unauthorized access"
        elif type(request.json["variation"]) is not dict:
            error["variation"] = "this field is required"
        else:
            variation = request.json["variation"]
            for key in variation:
                if (
                    type(variation[key]) is not list
                    or len(variation[key]) == 0
                ):
                    del variation[key]
            item["variation"] = variation

    if error != {}:
        return jsonify({
            "status": 400,
            **error
        })

    item["date_u"] = now()
    database(item)

    database(log_template(
        user["key"],
        "edited",
        item["key"],
        "item",
        misc=request.json
    ), db_name="log")

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

    if "item:edit_photo" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    item = query({"type": "item", "key": key}, db=db)
    if 'files' not in request.files or not item:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = ""
    files = []
    for x in request.files.getlist("files"):
        media, format = x.content_type.split("/")

        err = ""
        if media != "image" or format in ['svg+xml', 'x-icon']:
            err = f"{x.filename} => invalid file"
        elif len(files) + len(item["photos"]) >= 10:
            err = f"{x.filename} => excess file"

        if err:
            error = f"{error}, {err}" if error else err
        else:
            files.append(x)

    if files == []:
        if not error:
            error = "no file"
        return jsonify({
            "status": 400,
            "error": error
        })

    file_names = []
    for x in files:
        fn = storage(x)
        item["photos"].append(fn)
        file_names.append(fn)

    database(item)
    database(log_template(
        user["key"],
        "added_photo",
        item["key"],
        "item",
        misc={
            "added": ", ".join(file_names),
            "error": error
        }
    ), db_name="log")

    return jsonify({
        "status": 200,
        "item": item_schema(item, db),
        "error": error
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

    if "item:edit_photo" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    def fix(arr):
        return [p.split("/")[-1] for p in arr]

    item = query({"type": "item", "key": key}, db=db)
    if (
        not item
        or "photos" not in request.json
        or type(request.json["photos"]) is not list
        or set(item["photos"]) != set(fix(request.json["photos"]))
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    database(log_template(
        user["key"],
        "arranged_photo",
        item["key"],
        "item",
        misc={
            "from": item["photos"],
            "to": fix(request.json["photos"])
        }
    ), db_name="log")

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

    if "item:edit_photo" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    item = query({"type": "item", "key": key}, db=db)

    if (
        not item
        or "active_photo" not in request.json
        or not request.json["active_photo"]
        or request.json["active_photo"].split("/")[-1] not in item["photos"]
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    file_name = request.json["active_photo"].split("/")[-1]

    item["photos"].remove(file_name)
    if len(item["photos"]) == 0 and item["status"] == "live":
        item["status"] = "draft"
    storage(file_name, delete=True)
    database(item)

    database(log_template(
        user["key"],
        "deleted_photo",
        item["key"],
        "item",
        misc={
            "photo": file_name
        }
    ), db_name="log")

    return jsonify({
        "status": 200,
        "item": item_schema(item, db)
    })
