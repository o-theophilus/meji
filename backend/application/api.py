from flask import Blueprint, jsonify, request
from .storage import storage, drive
from .database import database
from .tools import token_to_user
from .item_get import all_tags, shop
from .advert import adverts


bp = Blueprint("api", __name__)


@bp.get("/home")
def home():
    db = database()

    return jsonify({
        "status": 200,
        "tags": all_tags(db).json["tags"],
        "new_arrivals": shop(db, sort="latest", size=8).json["items"],
        "offers": shop(db, sort="discount", size=8).json["items"],
        "adverts": adverts("home_1", db).json["adverts"]
    })


@bp.get("/photo_error")
def photo_error():
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "admin:manage_photo" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    stored_photos = []
    paths = drive().list()["names"]
    for x in paths:
        stored_photos.append(x.split('/')[1])

    users = []
    items = []
    adverts = []
    used_photos = []
    for x in db:

        if x["type"] == "user" and x["photo"]:
            used_photos.append(x["photo"])
            if x["photo"] not in stored_photos:
                users.append({
                    "key": x["key"],
                    "name": x["name"],
                })

        elif x["type"] == "item" and x["photos"] != []:
            used_photos += x["photos"]
            if not all(y in stored_photos for y in x["photos"]):
                items.append({
                    "key": x["key"],
                    "name": x["name"],
                })

        elif x["type"] == "advert":
            x["photos"] = [y for y in x["photos"].values() if y is not None]
            if x["photos"] != []:
                used_photos += x["photos"]
                if not all(y in stored_photos for y in x["photos"]):
                    adverts.append({
                        "key": x["item"],
                        "name": x["key"],
                    })

    unused = [f"{request.host_url}photos/{x}"
              for x in stored_photos if x not in used_photos]

    return jsonify({
        "status": 200,
        "unused": unused,
        "users": users,
        "items": items,
        "adverts": adverts,
    })


@bp.delete("/photo_error")
def delete_photo():
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "admin:manage_photo" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    if (
        "photos" not in request.json
        or type(request.json["photos"]) is not list
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    for x in request.json["photos"]:
        pass
        storage(x.split("/")[-1], delete=True)

    return jsonify({
        "status": 200
    })
