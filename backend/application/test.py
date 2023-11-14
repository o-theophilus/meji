from flask import Blueprint, jsonify
from deta import Deta
from os import environ
from .database import database
from datetime import datetime, timedelta


bp = Blueprint("test", __name__)


@bp.post("/cron")
@bp.get("/cron")
def cron():

    # expire voucher
    # signout inactive users after 7 days
    # delete anonymous users without cart and like after 7 days
    # delete anonymous users with cart or like after 30 days

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


def clean_copy_db():
    source = Deta(environ["DETA_KEY"]).Base("main")
    target = Deta(environ["DETA_KEY"]).Base("main_test")

    res = target.fetch()
    entities = res.items
    while res.last:
        res = target.fetch(last=res.last)
        entities += res.items

    for x in entities:
        target.delete(x["key"])

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


@bp.get("/fix")
def copy_db():
    source = Deta(environ["DETA_KEY"]).Base("main_test")
    target = Deta(environ["DETA_KEY"]).Base("main")

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


def fix():
    db = database()

    changed = []
    for x in db:
        if x["type"] == "user" and x["status"] == "confirmed":
            # x["status"] = "confirmed"
            changed.append(x)

    print(len(changed))
    # print(changed[0])
    # database(changed)

    return jsonify({
        "status": 200,
        "changed": len(changed)
    })
