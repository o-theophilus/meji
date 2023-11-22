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
ad_space = ['home_1', 'home_2', 'home_3', 'shop', 'save']


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
        "places": [],
    }


@bp.get("/advert/<key>")
def get_advert(key):
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "item:advert" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    item = query({"type": "item", "key": key.split("_")[0]}, db=db)
    if not item:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    advert = query({"type": "advert", "key": key}, db=db)
    if not advert:
        advert = advert_template(item["key"])

    database(log_template(
        user["key"],
        "viewed",
        advert["key"],
        "advert",
    ), db_name="log")

    return jsonify({
        "status": 200,
        "advert": advert_schema(advert, db),
        "ad_space": ad_space
    })


@bp.get("/advert")
def adverts(status="", db=None):
    if not db:
        db = database()

    page_no = int(request.args["page_no"]) if "page_no" in request.args else 1
    size = int(request.args["size"]) if "size" in request.args else 24
    status = request.args["status"] if "status" in request.args else status

    adverts = []
    for x in db:
        if x["type"] != "advert":
            continue
        if status and status not in x["places"]:
            continue
        adverts.append(x)

    total_page = ceil(len(adverts) / size)
    start = (page_no - 1) * size
    stop = start + size
    adverts = adverts[start: stop]

    return jsonify({
        "status": 200,
        "adverts": [advert_schema(x, db) for x in adverts],
        "total_page": total_page,
        "ad_space": ad_space
    })


@bp.post("/advert/<item_key>")
def add_photo(item_key):
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "item:advert" not in user["roles"]:
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

    if not item or 'files' not in request.files:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if not advert:
        advert = advert_template(item["key"])

    available_dims = []
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

    misc = {}
    for x in files:
        dim = Image.open(x).size
        dim = f"{dim[0]}x{dim[1]}"
        advert["photos"][dim] = storage(x)
        misc[dim] = advert["photos"][dim]

    database(advert)
    database(log_template(
        user["key"],
        "added_photo",
        advert["key"],
        "advert",
        misc=misc
    ), db_name="log")

    return jsonify({
        "status": 200,
        "advert": advert_schema(advert, db),
        "error": error
    })


@bp.delete("/advert/<item_key>")
def delete_photo(item_key):
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "item:advert" not in user["roles"]:
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
        or not advert
        or "photo" not in request.json
        or not request.json["photo"]
        or "size" not in request.json
        or not request.json["size"]
    ):
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

    misc = {}
    misc[size] = advert["photos"][size]
    storage(advert["photos"][size], delete=True)
    advert["photos"][size] = None

    has_photo = False
    for x in advert["photos"]:
        if advert["photos"][x]:
            has_photo = True
            break
    if has_photo:
        database(advert)
    else:
        database(advert, True)
        advert = advert_template(item["key"])

    database(log_template(
        user["key"],
        "deleted_photo",
        advert["key"],
        "advert",
        misc=misc
    ), db_name="log")

    return jsonify({
        "status": 200,
        "advert": advert_schema(advert, db),
    })


@bp.delete("/advert_all/<item_key>")
def delete_all_photo(item_key):
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "item:advert" not in user["roles"]:
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

    if not item or not advert:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    misc = {}
    for x in advert["photos"]:
        if advert["photos"][x]:
            storage(advert["photos"][x], delete=True)
            misc[x] = advert["photos"][x]

    database(advert, True)
    database(log_template(
        user["key"],
        "deleted_photo",
        advert["key"],
        "advert",
        misc=misc
    ), db_name="log")

    return jsonify({
        "status": 200,
        "advert": advert_schema(advert_template(item["key"]), db)
    })


@bp.put("/advert/<item_key>")
def adverts_placement(item_key):
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "item:advert" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    advert = query({"type": "advert", "key": item_key}, db=db)
    if (
        not advert
        or "places" not in request.json
        or type(request.json["places"]) is not list
        or not all(y in ad_space for y in request.json["places"])
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    for x in advert["photos"]:
        if not advert["photos"][x]:
            return jsonify({
                "status": 400,
                "error": "invalid request"
            })

    database(log_template(
        user["key"],
        "changed_placement",
        advert["key"],
        "advert",
        misc={
            "from": advert["places"],
            "to": request.json["places"]
        }
    ), db_name="log")

    advert["places"] = request.json["places"]
    advert["date_u"] = now()
    advert = database(advert)

    return jsonify({
        "status": 200,
        "advert": advert_schema(advert, db)
    })
