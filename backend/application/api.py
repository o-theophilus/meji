from flask import Blueprint, jsonify, request
from deta import Deta
from .tools import send_mail
from .database import database, query
from datetime import datetime, timedelta
import re
import os
from .postgres import db_close, db_open
from uuid import uuid4
import json


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

    expired = []
    logged_out = []
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
            expired.append(x)

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
                logged_out.append(x)

            elif x["status"] == "anonymous":
                cart = query({"type": "cart", "user": x["key"]}, db=db)
                save = query({"type": "save", "user": x["key"]}, db=db)

                if not cart and not save and last_active < seven_days_ago:
                    rem.append(x)

                elif last_active < thirty_days_ago:
                    rem.append(x)

    database(expired+logged_out)
    rem = rem[:10]
    database(rem, True)

    query("""
        INSERT INTO log (
            key, date, user_key, action, entity_key, entity_type, status, misc
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """(
        "meji",
        "ran_cron",
        None,
        "auth",
        misc={
            "expired_voucher": ", ".join([x["key"] for x in expired]),
            "users_logged_out": ", ".join([x["email"] for x in logged_out]),
            "anonymous_deleted": ", ".join([x["key"] for x in rem])
        }
    ))

    return jsonify({
        "status": 200,
        "message": "successful"
    })


# @bp.get("/fix")
def deta_to_postgres():
    con, cur = db_open()

    source = Deta(os.environ["DETA_KEY"]).Base("main")

    res = source.fetch()
    entities = res.items
    while res.last:
        res = source.fetch(last=res.last)
        entities += res.items

    for x in entities:
        if x["type"] == "item":
            cur.execute("""
                INSERT INTO item (
                    key,
                    version,
                    status,

                    name,
                    slug,
                    price,
                    old_price,
                    information,
                    photos,
                    tags,
                    variation,

                    available_quantity
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (
                x["key"],
                x["v"],
                x["status"],

                x["name"],
                x["slug"],
                x["price"],
                x["old_price"],
                x["info"],
                x["photos"],
                x["tags"],
                json.dumps(x["variation"]),

                x["available_quantity"]
            ))

            cur.execute("""
                INSERT INTO log (
                    key, date, user_key, action, entity_key, entity_type
                ) VALUES (%s, %s, %s, %s, %s, %s);
            """, (
                uuid4().hex,
                x["date_c"],
                "46a28cf075b048a581615c8cb508d0c3",
                "created",
                x["key"],
                "item"
            ))

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "message": "successful",
    })
