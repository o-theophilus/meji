from flask import Blueprint, jsonify, request
from deta import Deta
from .tools import send_mail
from .database import database, query
from datetime import datetime, timedelta
import re
import os
from .log import log_template


bp = Blueprint("test", __name__)


@bp.post("/contact")
def contact():
    error = {}

    if "name" not in request.json or not request.json["name"]:
        error["name"] = "this field is required"

    if "email" not in request.json or not request.json["email"]:
        error["email"] = "this field is required"
    elif not re.match(r"\S+@\S+\.\S+", request.json["email"]):
        error["email"] = "Please enter a valid email"

    if "message" not in request.json or not request.json["message"]:
        error["message"] = "this field is required"

    if error != {}:
        return jsonify({
            "status": 400,
            **error
        })

    phone = ""
    if "phone" in request.json and request.json["name"]:
        phone = request.json["phone"]

    send_mail(
        os.environ["MAIL_USERNAME"],
        "Contact Form",
        f"""
from: {request.json["name"]} <{request.json["name"]}>
{phone}

{request.json["message"]}
        """
    )

    return jsonify({
        "status": 200
    })


@bp.get("/cron")
def cron():
    db = database()
    log_db = database(db_name="log")
    log_db = sorted(log_db, key=lambda d: d["date"], reverse=True)

    picked = []
    users_last_active = []
    for x in log_db:
        if x["user"] not in picked:
            picked.append(x["user"])
            users_last_active.append({
                "key": x["user"],
                "date":  datetime.strptime(
                    x["date"], '%Y-%m-%dT%H:%M:%S'
                )
            })

    seven_days_ago = datetime.now() - timedelta(days=7)
    thirty_days_ago = datetime.now() - timedelta(days=30)

    mod = []
    rem = []

    for x in db:
        if (
            x["type"] == "voucher"
            and x["status"] == "active"
            and datetime.strptime(
                x["validity"], '%Y-%m-%d'
            ) < datetime.now()
        ):
            x["status"] = "expired"
            mod.append(x)

        elif x["type"] == "user":

            last_active = None
            for y in users_last_active:
                if x["key"] == y["key"]:
                    last_active = y["date"]
                    break

            if not last_active:
                rem.append(x)

            elif x["login"] and last_active < seven_days_ago:
                x["login"] = False
                mod.append(x)

            elif x["status"] == "anonymous":
                cart = query({"type": "cart", "user": x["key"]}, db=db)
                save = query({"type": "save", "user": x["key"]}, db=db)

                if not cart and not save and last_active < seven_days_ago:
                    rem.append(x)

                elif last_active < thirty_days_ago:
                    rem.append(x)

    database(mod)
    rem = rem[:10]
    database(rem, True)

    database(log_template(
        "Meji",
        "ran cron",
        None,
        "auth"
    ), db_name="log")

    return jsonify({
        "status": 200,
        "message": "successful"
    })


def clean_copy_db():
    source = Deta(os.environ["DETA_KEY"]).Base("log_test")
    target = Deta(os.environ["DETA_KEY"]).Base("log")

    def delete_target():
        res = target.fetch()
        entities = res.items
        while res.last:
            res = target.fetch(last=res.last)
            entities += res.items

        for x in entities:
            target.delete(x["key"])

    def copy_source():
        res = source.fetch()
        entities = res.items
        while res.last:
            res = source.fetch(last=res.last)
            entities += res.items

        while len(entities) > 0:
            target.put_many(entities[:25])
            entities = entities[25:]

    delete_target()
    copy_source()

    return jsonify({
        "status": 200,
        "message": "successful",
    })


# @bp.get("/fix")
def migration():
    data_base = Deta(os.environ["DETA_KEY"]).Base("main")

    res = data_base.fetch()
    entities = res.items
    while res.last:
        res = data_base.fetch(last=res.last)
        entities += res.items

    changed = []
    for x in entities:
        if (
            x["type"] == "item"
            and x["tags"].count("male") > 1
        ):

            x["tags"].remove("male")
            changed.append(x)

    # print(changed[0])
    print(len(changed))

    # while len(changed) > 0:
    #     data_base.put_many(changed[:25])
    #     changed = changed[25:]

    return jsonify({
        "status": 200,
        "changed": len(changed)
    })
