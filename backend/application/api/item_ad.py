from flask import Blueprint, jsonify, request
from .tools import token_to_user
from math import ceil
from .database import database
# from .photo import photo_url
import re

bp = Blueprint("item_ad", __name__)


def ads_schema(item):
    photos = sorted(item["photos"], key=lambda d: d["order"])
    photos = [
        f"{'xxx'}/{photo['key']}" for photo in photos]

    return {
        "key": item["key"],
        "alias": item["alias"],
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

    search = request.args.get("search")
    page_no = int(request.args.get("page_no"))
    size = 24

    items = []
    for row in data:
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
        "status": 200,
        "message": "successful",
        "data": {
            "items": [ads_schema(item) for item in items],
            "total_page": total_page
        }
    })


@bp.put("/ads/<key>")
def placement(key):
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

    if "placement" not in request.json or not request.json["placement"]:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    item = query("item", "key", key, data)
    if not item:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    item["ads"]["placement"] = request.json["placement"]
    item = database(item)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "item": ads_schema(item)
        }
    })
