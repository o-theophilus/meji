from flask import Blueprint, jsonify, request
from .tools import token_to_user
from .database import database, query
from .schema import advert_schema
from .storage import storage
from .tools import now
from uuid import uuid4
from .log import log_template
from PIL import Image

bp = Blueprint("advert", __name__)


dimensions = ["300x300", "300x600", "600x300", "900x300"]


def advert_template(item):
    return {
        "key": uuid4().hex,
        "date_c": now(),
        "date_u": now(),
        "type": "advert",

        "item": item,
        "photos": {
                "300x300": None,
                "300x600": None,
                "600x300": None,
                "900x300": None
        },
        "placements": [],
    }


@bp.get("/advert/<item_key>")
def get_advert(item_key):
    db = database()

    item = query({"type": "item", "slug": item_key}, db=db)
    if not item:
        item = query({"type": "item", "key": item_key}, db=db)
    if not item:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    advert = query({"type": "advert", "item": item["key"]}, db=db)
    if not advert:
        advert = advert_template(item["key"])

    return jsonify({
        "status": 200,
        "advert": advert_schema(advert)
    })


@bp.post("/advert/<item_key>")
def add_advert(item_key):
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
            "error": "unauthorized access"
        })

    item = None
    advert = None
    for x in db:
        if not item and x["type"] == "item" and x["key"] == item_key:
            item = x
        elif not advert and x["type"] == "advert" and x["item"] == item_key:
            advert = x

        if item and advert:
            break

    if 'files' not in request.files or not item:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if not advert:
        for x in db:
            if not advert and x["type"] == "advert" and x["item"] == item_key:
                advert = x
                break

    available_dims = []
    if advert:
        for x in advert["photos"]:
            if advert["photos"][x]:
                available_dims.append(x)

    error = ""
    files = []
    for x in request.files.getlist("files"):
        media, format = x.content_type.split("/")
        dim = Image.open(x).size
        dim = f"{dim[0]}x{dim[1]}"

        err = ""
        if media != "image" or format in ['svg+xml', 'x-icon']:
            err = f"{x.filename} => invalid file"
        elif dim in available_dims:
            err = f"{x.filename} => already picked"
        elif dim not in dimensions:
            err = f"{x.filename} => invalid dimension"

        if err:
            error = f"{error}, {err}" if error else err
        else:
            available_dims.append(dim)
            files.append(x)

    if files == []:
        if not error:
            error = "no file"
        return jsonify({
            "status": 400,
            "error": error
        })

    action = "added_photo"
    if not advert:
        action = "created"
        advert = advert_template(item["key"])

    for x in files:
        dim = Image.open(x).size
        dim = f"{dim[0]}x{dim[1]}"
        advert["photos"][dim] = storage(x)

    log = log_template(
        user["key"],
        action,
        advert["key"],
        "advert"
    )
    database([advert, log])

    return jsonify({
        "status": 200,
        "advert": advert_schema(advert),
        "error": error
    })


@bp.delete("/advert_photo/<item_key>")
def delete_photo(item_key):
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
            "error": "unauthorized access"
        })

    item = None
    advert = None
    for x in db:
        if not item and x["type"] == "item" and x["key"] == item_key:
            item = x
        elif not advert and x["type"] == "advert" and x["item"] == item_key:
            advert = x

        if item and advert:
            break

    if (
        not item
        or "photo" not in request.json
        or not request.json["photo"]
        or "size" not in request.json
        or not request.json["size"]
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if not advert:
        for x in db:
            if not advert and x["type"] == "advert" and x["item"] == item_key:
                advert = x
                break

    if not advert:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    size = request.json["size"]

    if request.json["photo"].split("/")[-1] != advert["photos"][size]:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    storage(advert["photos"][size], delete=True)
    advert["photos"][size] = None

    has_photo = False
    for x in advert["photos"]:
        if advert["photos"][x]:
            has_photo = True
            break

    log = log_template(
        user["key"],
        "deleted",
        advert["key"],
        "advert"
    )

    if has_photo:
        log["action"] = "updated photos"
        database([advert, log])
    else:
        database(advert, True)
        database(log)
        advert = advert_template(item["key"])

    return jsonify({
        "status": 200,
        "advert": advert_schema(advert),
    })


@bp.delete("/advert/<item_key>")
def delete_advert(item_key):
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
            "error": "unauthorized access"
        })

    item = None
    advert = None
    for x in db:
        if not item and x["type"] == "item" and x["key"] == item_key:
            item = x
        elif not advert and x["type"] == "advert" and x["item"] == item_key:
            advert = x

        if item and advert:
            break

    if not item:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if not advert:
        for x in db:
            if not advert and x["type"] == "advert" and x["item"] == item_key:
                advert = x
                break

    if not advert:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    for x in advert["photos"]:
        if advert["photos"][x]:
            storage(advert["photos"][x], delete=True)

    log = log_template(
        user["key"],
        "deleted",
        advert["key"],
        "advert"
    )
    database(advert, True)
    database(log)

    return jsonify({
        "status": 200,
        "advert": advert_schema(advert_template(item["key"]))
    })
