from flask import Blueprint, jsonify, send_file, request
from .storage import storage, drive
from deta import Deta
from os import environ
from .database import database
from datetime import datetime, timedelta
from .tools import token_to_user
from .item_get import all_tags, shop
from .advert import adverts_placement


bp = Blueprint("api", __name__)


@bp.get("/photos/<key>")
@bp.get("/photos/<key>/<thumbnail>")
def get_photo(key, thumbnail=False):
    photo = storage(key, thumbnail=thumbnail)
    return send_file(photo, mimetype="image/jpg")


@bp.get("/photo_error")
def file_list():
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


@bp.get("/home")
def home():
    db = database()

    return jsonify({
        "status": 200,
        "tags": all_tags(db).json["tags"],
        "new_arrivals": shop(db, sort="latest", size=8).json["items"],
        "offers": shop(db, sort="discount", size=8).json["items"],
        "adverts": adverts_placement(db).json["adverts"]
    })


#################################################

@bp.post("/cron")
@bp.get("/cron")
def cron():
    temp1 = unused_anon().json

    for key in temp1["db"]["keys"]:
        pass
        # db_delete(key)

    return jsonify({
        "status": 200,
        "message": "successful"
    })


def unused_anon():
    db = database()

    keys = []
    for row in db:
        if (
            row["type"] == "user"
            and row["status"] == "anon"
            and row["saves"] == []
            and row["cart"] == []
        ):
            created = datetime.strptime(row["date_c"], '%Y-%m-%dT%H:%M:%S')
            _24hour_ago = datetime.now() - timedelta(days=1)

            if created < _24hour_ago:
                keys.append(row["key"])

    return jsonify({
        "status": 200,
        "message": "successful",
        "db": {
            "keys": keys
        }
    })


def test():
    a = {
        "a": 1,
        "b": 2,
        "d": None,
        "c": 5,
    }

    print(a.keys())
    print(a.values())
    print(list(a.values()))
    print([value for value in a.values() if value is not None])

    return jsonify({
        "status": 200,
    })


def copy_db():
    source = Deta(environ["DETA_KEY"]).Base("test")
    target = Deta(environ["DETA_KEY"]).Base("live")

    res = source.fetch()
    entities = res.items
    while res.last:
        res = source.fetch(last=res.last)
        entities += res.items

    while len(entities) > 0:
        target.put_many(entities[:25])
        entities = entities[25:]

    return jsonify({
        "status": 200,
        "message": "successful",
    })


def delete_db():
    print("deleting...")
    db = Deta(environ["DETA_KEY"]).Base("live")

    res = db.fetch()
    entities = res.items
    while res.last:
        res = db.fetch(last=res.last)
        entities += res.items

    for x in entities:
        db.delete(x["key"])

    return jsonify({
        "status": 200,
        "message": "successful",
    })


# @bp.get("/fix")
def fix():
    db = database()

    changed = []
    for x in db:
        if x["type"] == "log" and x["action"] == "deactivated":

            x["misc"] = None
            changed.append(x)

    print(len(changed))
    database(changed)

    return jsonify({
        "status": 200,
        "changed": len(changed)
    })
