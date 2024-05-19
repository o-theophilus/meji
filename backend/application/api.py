from flask import Blueprint, jsonify, request
from deta import Deta
from .tools import send_mail
import re
import os
from .postgres import db_close, db_open
# from .postgres import (
#     user_table, item_table, save_table, order_table, order_item_table,
#     feedback_table, advert_table, voucher_table, log_table, otp_table)
from uuid import uuid4
import json
from .log import log


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
from: {request.json["name"]} <{request.json["email"]}>
{phone}

{request.json["message"]}
        """
    )

    return jsonify({
        "status": 200
    })


@bp.get("/cron")
def cron():
    con, cur = db_open()

    cur.execute('SELECT * FROM "user" WHERE email = %s;',
                (os.environ["MAIL_USERNAME"],))
    admin = cur.fetchone()

    cur.execute("""
        SELECT *
        FROM voucher
        WHERE
            voucher.status = 'activated'
            AND voucher.validity < CURRENT_TIMESTAMP;
    """)
    expired = cur.fetchall()

    for x in expired:
        cur.execute("""
            UPDATE voucher
            SET status = 'expired', validity = NULL
            WHERE key = %s;
        """, (x["key"],))

        log(
            cur=cur,
            user_key=admin["key"],
            action="expired",
            entity_key=x["key"],
            entity_type="voucher",
            misc={"validity": f"{x['validity']}"}
        )

    log(
        cur=cur,
        user_key=admin["key"],
        action="ran_cron",
        entity_key=None,
        entity_type="admin",
        misc={
            "expired vouchers": [x["key"] for x in expired]
        }
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "message": "successful"
    })


# @bp.get("/fix")
def fix():
    con, cur = db_open()

    # cur.execute(f"""
    #     DROP TABLE IF EXISTS "user" CASCADE;
    #     DROP TABLE IF EXISTS item CASCADE;
    #     DROP TABLE IF EXISTS save;
    #     DROP TABLE IF EXISTS "order" CASCADE;
    #     DROP TABLE IF EXISTS order_item;
    #     DROP TABLE IF EXISTS feedback;
    #     DROP TABLE IF EXISTS advert;
    #     DROP TABLE IF EXISTS voucher;
    #     DROP TABLE IF EXISTS log;
    #     DROP TABLE IF EXISTS otp;
    #     {user_table};
    #     {item_table};
    #     {save_table};
    #     {order_table};
    #     {order_item_table};
    #     {feedback_table};
    #     {advert_table};
    #     {voucher_table};
    #     {log_table};
    #     {otp_table};
    # """)

    # cur.execute("""
    #     ALTER TABLE item
    #     RENAME COLUMN old_price
    #     TO discount_time;

    #     ALTER TABLE item
    #     ALTER COLUMN discount_time
    #     TYPE VARCHAR(32);

    #     ALTER TABLE item
    #     ALTER COLUMN discount_time
    #     SET DEFAULT 'TRUE';

    #     UPDATE item
    #     SET discount_time = 'TRUE';

    #     ALTER TABLE save
    #     DROP COLUMN date;

    # ALTER TABLE order_item
    # ADD COLUMN price FLOAT DEFAULT 0 NOT NULL;
    # """)

    # cur.execute("""
    #     ALTER TABLE order_item
    #     ADD COLUMN price FLOAT DEFAULT 0 NOT NULL;
    # """)

    # cur.execute("""
    #     UPDATE order_item
    #     SET price = (
    #         SELECT item.price
    #         FROM item
    #         WHERE item.key = order_item.item_key
    #     )
    #     WHERE order_key IN (
    #         SELECT "order".key
    #         FROM "order"
    #         WHERE "order".status != 'cart'
    #     );
    # """)

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "message": "successful",
    })


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
                    status,

                    name,
                    slug,
                    price,
                    information,
                    photos,
                    tags,
                    variation,

                    available_quantity
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (
                x["key"],
                x["status"],

                x["name"],
                x["slug"],
                x["price"],
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
                "0c0671906951411e8d450004aff4d3c2",
                "created",
                x["key"],
                "item"
            ))

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "message": "successful",
    })
