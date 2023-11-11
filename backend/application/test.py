from flask import Blueprint, jsonify
from deta import Deta
from os import environ
from .database import database
from datetime import datetime, timedelta


bp = Blueprint("test", __name__)


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


# @bp.get("/fix")
def copy_db():
    source = Deta(environ["DETA_KEY"]).Base("test")
    target = Deta(environ["DETA_KEY"]).Base("log")

    res = source.fetch()
    entities = res.items
    while res.last:
        res = source.fetch(last=res.last)
        entities += res.items

    print(len(entities))
    entities = [x for x in entities if x["type"] == "log"]
    print(len(entities))

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


def fix():
    db = database()

    changed = []
    for x in db:
        if x["type"] == "advert":
            x["places"] = x["place"]
            del x["place"]
            changed.append(x)

    print(len(changed))
    print(changed[0])
    database(changed)

    return jsonify({
        "status": 200,
        "changed": len(changed)
    })
