from flask import Blueprint, jsonify, send_file
from .storage import storage, drive
from deta import Deta
from os import environ
from .database import database  # , query
from datetime import datetime, timedelta


bp = Blueprint("api", __name__)


@bp.get("/photos/<key>")
@bp.get("/photos/<key>/<thumbnail>")
def get_photo(key, thumbnail=False):
    photo = storage(key, thumbnail=thumbnail)
    return send_file(photo, mimetype="image/jpg")


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


@bp.get("/copy_db")
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


def file_list():
    paths = drive().list()["names"]

    for x in paths:
        photo = drive().get(x)
        drive().put(f"photos/{x.split('/')[1]}", photo)
        drive().delete(x)


@bp.get("/fix")
def fix():
    db = database()

    for x in db:
        if x["type"] == "order":
            database(x, True)

    return jsonify({
        "status": 200
    })
