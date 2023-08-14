from flask import Blueprint, jsonify, send_file, request
from .storage import storage, drive
from deta import Deta
from os import environ
from .database import database
from datetime import datetime, timedelta
from .tools import token_to_user


bp = Blueprint("api", __name__)


@bp.get("/photos/<key>")
@bp.get("/photos/<key>/<thumbnail>")
def get_photo(key, thumbnail=False):
    photo = storage(key, thumbnail=thumbnail)
    return send_file(photo, mimetype="image/jpg")


@bp.get("/admin/photos")
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
            "error": "unauthorised access"
        })

    items_photos = []
    items = []
    for x in db:
        if x["type"] == "item":
            items_photos += x["photos"]
            items.append({
                "name": x["name"],
                "slug": x["slug"],
                "photos": x["photos"]
            })

    stored_photos = []
    paths = drive().list()["names"]
    for x in paths:
        stored_photos.append(x.split('/')[1])

    missing = [x for x in items_photos if x not in stored_photos]
    unused = [f"{request.host_url}photos/{x}"
              for x in stored_photos if x not in items_photos]

    missing_slug = []
    for x in items:
        for y in missing:
            if y in x["photos"] and x["slug"] not in missing_slug:
                missing_slug.append({
                    "name": x["name"],
                    "slug": x["slug"]
                })
                continue

    return jsonify({
        "status": 200,
        "missing": missing_slug,
        "unused": unused
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


@bp.get("/fix")
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


@bp.get("/fixx")
def fix():
    db = database()

    for x in db:
        if x["type"] == "order":
            database(x, True)

    return jsonify({
        "status": 200
    })
