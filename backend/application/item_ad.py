from flask import Blueprint, jsonify, request
from .tools import token_to_user
from math import ceil
from .database import database, query
from .schema import item_schema
# from .photo import photo_url
import re

bp = Blueprint("item_ad", __name__)


def ads_schema(item):
    photos = sorted(item["photos"], key=lambda d: d["order"])
    photos = [
        f"{'xxx'}/{photo['key']}" for photo in photos]

    return {
        "key": item["key"],
        "slug": item["slug"],
        "name": item["name"],

        "photos": photos,
        "300x300": item["ads"]["300x300"],
        "300x600": item["ads"]["300x600"],
        "600x300": item["ads"]["600x300"],
        "900x300": item["ads"]["900x300"],
        "placement": item["ads"]["placement"],
    }


@bp.get("/ads")
def ad():
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

    search = request.args["search"] if "search" in request.args else ""
    page_no = int(request.args["page_no"]) if "page_no" in request.args else 1
    size = int(request.args["size"]) if "size" in request.args else 24

    items = []
    for row in db:
        if (
            row["type"] == "item"
            and row["status"] == "live"
            and row["ads"] != {}
        ):
            if search:
                if re.search(search, row["name"], re.IGNORECASE):
                    items.append(row)
            else:
                items.append(row)

    items = sorted(items, key=lambda d: d["name"])

    total_page = ceil(len(items) / size)

    start = (page_no - 1) * size
    stop = start + size
    items = items[start: stop]

    return jsonify({
        "status": 400,
        "error": "successful",
        "db": {
            "items": [ads_schema(item) for item in items],
            "total_page": total_page
        }
    })


@ bp.get("/ads")
def ads():
    db = database()

    ads = []
    for x in db:
        if (
            x["type"] == "item"
            and "ads" in x
            and x["ads"] != {}
            and "home" in x["ads"]["placement"]
        ):
            ads.append({
                "name": x["name"],
                "slug": x["slug"],
                "ads": {
                    f'{"xxx"}/{x["ads"]["300x300"]}',
                    f'{"xxx"}/{x["ads"]["300x600"]}',
                    f'{"xxx"}/{x["ads"]["600x300"]}',
                    f'{"xxx"}/{x["ads"]["900x300"]}'
                }
            })

    return jsonify({
        "status": 400,
        "ads": ads,
    })


@bp.post("/ads/<item_key>")
def add(item_key):
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

    item = query({"type": "item", "key": item_key}, db=db)
    if not item:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    def validate(size):
        if size not in request.files:
            return None

        file = request.files[size]

        ext = file.filename.split(".")[-1]
        if ext.lower() not in ['jpg', 'png', 'gif']:
            return None

        # check dimension too
        return file

    error = {}

    sizes = ["300x300", "300x600", "600x300", "900x300"]
    files = {}
    for x in sizes:
        file_ = validate(x)
        if file_:
            files[x] = file_
        else:
            error[x] = "invalid request, file or type"

    if error != {}:
        return jsonify({
            "status": 400,
            "error": error
        })

    ads = {
        # "300x300": upload(file_300x300, "ads", 300, 300),
        # "300x600": upload(file_300x600, "ads", 300, 600),
        # "600x300": upload(file_600x300, "ads", 600, 300),
        # "900x300": upload(file_900x300, "ads", 900, 300),
        "placement": []
    }

    item["ads"] = ads
    item = database(item)

    return jsonify({
        "status": 200,
        "error": "successful",
        "db": {
            "item": item_schema(item, db)
        }
    })


@bp.put("/ads/<key>")
def placement(key):
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

    if "placement" not in request.json or not request.json["placement"]:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    item = query("item", "key", key, db)
    if not item:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    item["ads"]["placement"] = request.json["placement"]
    item = database(item)

    return jsonify({
        "status": 200,
        "error": "successful",
        "db": {
            "item": ads_schema(item)
        }
    })


@bp.delete("/photo_ads/<key>")
def photo_remove_ads(key):
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

    item = query("item", "key", key, db)
    if not item:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if "ads" in item:
        pass
        # remove(item["ads"]["300x300"], "ads")
        # remove(item["ads"]["300x600"], "ads")
        # remove(item["ads"]["600x300"], "ads")
        # remove(item["ads"]["900x300"], "ads")

    item["ads"] = {}
    item = database(item)

    return jsonify({
        "status": 200,
        "error": "successful",
        "db": {
            "item": item_schema(item, db),
            "ads": item["ads"]
        }
    })
