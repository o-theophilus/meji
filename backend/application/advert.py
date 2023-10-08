from flask import Blueprint, jsonify, request
from .tools import token_to_user
from .database import database, query
from .schema import advert_schema
from .storage import storage
from .tools import now
from .log import log_template
from PIL import Image
from math import ceil

bp = Blueprint("advert", __name__)


dimensions = ["300x300", "300x600", "600x300", "900x300"]


def advert_template(item):
    return {
        "key": f"{item}_advert",
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
        "advert": advert_schema(advert, db)
    })


@bp.get("/adverts")
def adverts(db=None):
    if not db:
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

    page_no = int(request.args["page_no"]) if "page_no" in request.args else 1
    size = int(request.args["size"]) if "size" in request.args else 24
    status = request.args["status"] if "status" in request.args else ""

    adverts = []
    for x in db:
        if x["type"] != "advert":
            continue
        if status and status not in x["placements"]:
            continue
        adverts.append(x)

    # orders = sorted(orders, key=lambda d: d["date_u"])

    total_page = ceil(len(adverts) / size)
    start = (page_no - 1) * size
    stop = start + size
    adverts = adverts[start: stop]

    return jsonify({
        "status": 200,
        "adverts": [advert_schema(x, db) for x in adverts],
        "total_page": total_page
    })


@bp.get("/adverts_placement")
def adverts_placement(db=None):
    if not db:
        db = database()

    page_no = int(request.args["page_no"]) if "page_no" in request.args else 1
    size = int(request.args["size"]) if "size" in request.args else 24
    status = request.args["status"] if "status" in request.args else ""

    adverts = []
    for x in db:
        if x["type"] != "advert":
            continue
        if status and status not in x["placements"]:
            continue
        adverts.append(x)

    # orders = sorted(orders, key=lambda d: d["date_u"])

    total_page = ceil(len(adverts) / size)
    start = (page_no - 1) * size
    stop = start + size
    adverts = adverts[start: stop]

    return jsonify({
        "status": 200,
        "adverts": [advert_schema(x, db) for x in adverts],
        "total_page": total_page
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
        "advert": advert_schema(advert, db),
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
        log["action"] = "added_photo"
        database([advert, log])
    else:
        database(advert, True)
        database(log)
        advert = advert_template(item["key"])

    return jsonify({
        "status": 200,
        "advert": advert_schema(advert, db),
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
        "advert": advert_schema(advert_template(item["key"]), db)
    })
