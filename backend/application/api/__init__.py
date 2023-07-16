from flask import Blueprint, jsonify
# import database
# from .auth import omni
from deta import Deta
from os import environ
from .database import database, query
from datetime import datetime


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


@bp.get("/copy_db")
def copy_db():
    source = Deta(environ["DETA_KEY"]).Base("meji")
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


@bp.get("/fix")
def fix():
    db = database()

    edited = []
    for x in db:
        if x["type"] == "item":
            flag = False
            if "variation_options" in x:
                x["variation"] = x.pop("variation_options")
                flag = True
            if "alias" in x:
                x["slug"] = x.pop("alias")
                flag = True
            if "desc" in x:
                x["info"] = x.pop("desc")
                flag = True
            if "spec" in x:
                del x["spec"]
                flag = True
            if "tags" not in x:
                tags = []
                for row in db:
                    if row["type"] == "tag" and x["key"] in row["items"]:
                        tags.append(row["name"])
                x["tags"] = tags
                flag = True

            if flag:
                edited.append(x)

        elif x["type"] == "user" and x["status"] == "anon":
            x["status"] == "anonymous"
            edited.append(x)

        # elif x["type"] == "category":
        #     x["type"] = "tag"
        #     edited.append(x)

    database(edited)

    return jsonify({
        "status": 200
    })


@bp.get("/fix_photo")
def fix_photo():
    db = database()

    edited = []
    for x in db:
        if x["type"] == "item":
            x["photos"] = [y['key'] for y in x["photos"]]
            edited.append(x)

    database(edited)

    return jsonify({
        "status": 200
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
