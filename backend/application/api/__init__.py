from flask import Blueprint, jsonify
# import database
# from .auth import omni
from deta import Deta
from os import environ
from .database import database


bp = Blueprint("api", __name__)


@bp.post("/cron")
@bp.get("/cron")
def cron():
    temp1 = unused_anon().json

    for key in temp1["data"]["keys"]:
        pass
        # db_delete(key)

    return jsonify({
        "status": 200,
        "message": "successful"
    })


@bp.post("/copy_db")
def copy_db():
    from_ = Deta(environ["DETA_KEY"]).Base("dev")
    to_ = Deta(environ["DETA_KEY"]).Base("dev")

    while len(from_) != 0:
        to_.put_many(from_[:25])
        from_ = from_[25:]

    return jsonify({
        "status": 200,
        "message": "successful",
    })


@bp.get("/fix")
def fix():
    db = database()

    items = []
    for item in db:
        if item["type"] == "item":
            item["variations"] = item.pop("variation_options")
            items.append(item)

    database(items)

    return jsonify({
        "status": 200,
        "error": "successful"
    })


def unused_anon():
    data = database()

    keys = []
    for row in data:
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
        "data": {
            "keys": keys
        }
    })


def file_list():
    paths = drive().list()["names"]

    for x in paths:
        photo = drive().get(x)
        drive().put(f"photos/{x.split('/')[1]}", photo)
        drive().delete(x)
