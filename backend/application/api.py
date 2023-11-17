from flask import Blueprint, jsonify
from deta import Deta
from os import environ
from .database import database, query
from datetime import datetime, timedelta


bp = Blueprint("test", __name__)


@bp.post("/cron")
@bp.get("/cron")
def cron():
    db = database()
    log_db = database(db_name="log")

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

        elif x["type"] == "user" and x["login"]:
            user_logs = query({"user": x["key"]}, many=True, db=log_db)
            user_logs = sorted(
                user_logs, key=lambda d: d["date"], reverse=True)

            last_active = datetime.strptime(
                user_logs[0]["date"], '%Y-%m-%dT%H:%M:%S')
            seven_days_ago = datetime.now() - timedelta(days=7)

            if last_active < seven_days_ago:
                x["login"] = False
                mod.append(x)

        elif x["type"] == "user" and x["status"] == "anonymous":
            cart = query({"type": "cart", "user": x["key"]}, db=db)
            save = query({"type": "save", "user": x["key"]}, db=db)

            user_logs = query({"user": x["key"]}, many=True, db=log_db)
            user_logs = sorted(
                user_logs, key=lambda d: d["date"], reverse=True)

            last_active = datetime.strptime(
                user_logs[0]["date"], '%Y-%m-%dT%H:%M:%S')

            seven_days_ago = datetime.now() - timedelta(days=7)
            if not cart and not save and last_active < seven_days_ago:
                rem.append(x)

            thirty_days_ago = datetime.now() - timedelta(days=30)
            if cart and save and last_active < thirty_days_ago:
                rem.append(x)

    print(len(mod))
    print(len(rem))
    # database(mod)
    # database(rem, True)

    return jsonify({
        "status": 200,
        "message": "successful"
    })


@bp.get("/fix")
def clean_copy_db():
    source = Deta(environ["DETA_KEY"]).Base("main")
    target = Deta(environ["DETA_KEY"]).Base("main_test")

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
