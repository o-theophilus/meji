from flask import Blueprint, jsonify, request
from ..tools import get_session, send_mail
from ..postgres import db_open, db_close
from ..log import log
import os
import requests
from ..cart.get import get_cart_items
from .get import order_status
from datetime import datetime, timezone, timedelta

bp = Blueprint("order", __name__)


@bp.get("/order/check")
def order_check():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute("""
        SELECT * FROM "order"
        WHERE user_key = %s AND status = 'cart';
    """, (user["key"],))
    order = cur.fetchone()
    if not order:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if (
        "name" not in order["receiver"]
        or not order["receiver"]["name"]
        or "phone" not in order["receiver"]
        or not order["receiver"]["phone"]
        or "email" not in order["receiver"]
        or not order["receiver"]["email"]
        or "address" not in order["receiver"]
        or order["receiver"]["address"] == {}
        or "address" not in order["receiver"]["address"]
        or not order["receiver"]["address"]["address"]
        or "state" not in order["receiver"]["address"]
        or not order["receiver"]["address"]["state"]
        or "country" not in order["receiver"]["address"]
        or not order["receiver"]["address"]["country"]
        or "postal_code" not in order["receiver"]["address"]
        or not order["receiver"]["address"]["postal_code"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid delivery address"
        })

    # TODO: check item availability
    cur.execute("""
        SELECT
            item.price,
            order_item.quantity
        FROM order_item
        LEFT JOIN item ON item.key = order_item.item_key
        WHERE
            order_item.order_key = %s
            -- AND item.status = 'active';
    """, (order["key"],))
    items = cur.fetchall()
    if len(items) == 0:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    total = 0
    for x in items:
        total += x["price"] * x["quantity"]

    # TODO: also check Coupons here

    pay = total + order["cost_delivery"]

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "pay": pay
    })


@bp.post("/order")
def cart_to_order():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute("""
        SELECT *
        FROM "order"
        WHERE user_key = %s AND status = 'cart';
    """, (user["key"],))
    order = cur.fetchone()

    reference = request.json.get("reference")
    email_template_admin = request.json.get("email_template_admin")
    email_template_user = request.json.get("email_template_user")

    if (
        not order
        or not reference
        or not email_template_admin
        or not email_template_user
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    # TODO: check item availability
    cur.execute("""
        SELECT
            item.price,
            order_item.quantity
        FROM order_item
        LEFT JOIN item ON item.key = order_item.item_key
        WHERE
            order_item.order_key = %s
            -- AND item.status = 'active';
    """, (order["key"],))
    items = cur.fetchall()
    if len(items) == 0:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    total = 0
    for x in items:
        total += x["price"] * x["quantity"]

    # TODO: also check Coupons here

    pay = total + order["cost_delivery"]

    cur.execute(
        """SELECT * FROM "order" WHERE pay_reference = %s;""",
        (reference,))
    if cur.fetchone():
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    resp = requests.get(
        f"https://api.paystack.co/transaction/verify/{reference}",
        headers={
            'Content-Type': 'application/json',
            "Authorization": os.environ["PAYSTACK_KEY"]
        }
    )
    resp = resp.json()

    if (
        not resp["status"]
        or "data" not in resp
        or "status" not in resp["data"]
        or resp["data"]["status"] != "success"
        or "reference" not in resp["data"]
        or resp["data"]["reference"] != reference
        or "amount" not in resp["data"]
        or resp["data"]["amount"]/100 != pay
        or "currency" not in resp["data"]
        or resp["data"]["currency"] != "NGN"
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid transaction"
        })

    # TODO: do i remove unavaolable items?
    # cur.execute("""
    #     DELETE FROM order_item
    #     WHERE order_key = %s
    #     AND item_key IN (
    #         SELECT item.key
    #         FROM item
    #         WHERE item.status != 'live'
    #     );
    # """, (order["key"],))

    cur.execute("""
        UPDATE "order"
        SET
            status = 'created',
            cost_items = %s, delivery_date = %s,
            pay_user = %s,  pay_reference = %s
        WHERE key = %s RETURNING *;
    """, (
        total, datetime.now(timezone.utc) + timedelta(days=7),
        pay, reference,
        order["key"]
    ))
    order = cur.fetchone()
    get_cart_items(cur)

    log(
        cur=cur,
        user_key=user["key"],
        action="created",
        entity_key=order["key"],
        entity_type="order"
    )

    send_mail(
        os.environ["MAIL_USERNAME"],
        "New Order",
        email_template_admin
    )
    send_mail(
        user["email"],
        "Processing Order",
        email_template_user
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "order": order,
    })


@bp.put("/order/eta/<key>")
def date(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "order:edit_eta" not in user["permissions"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute("""SELECT * FROM "order" WHERE key = %s;""", (key,))
    order = cur.fetchone()

    if not order or order["status"] != "created":
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    try:
        datetime.strptime(
            f"{request.json['delivery_date']}",
            "%Y-%m-%dT%H:%M"
        )
    except Exception:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if (
        "delivery_date" not in request.json
        or not request.json["delivery_date"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "this field is required"
        })

    log(
        cur=cur,
        user_key=user["key"],
        action="changed_date",
        entity_key=order["key"],
        entity_type="order",
        misc={
            "from": f"{order['delivery_date']}",
            "to": request.json['delivery_date']
        }
    )

    cur.execute("""
        UPDATE "order"
        SET delivery_date = %s
        WHERE key = %s
        RETURNING *;
    """, (
        request.json['delivery_date'],
        order["key"]
    ))
    order = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "order": order
    })


@bp.post("/cart/delivery_date")
def delivery_date():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute("""
        SELECT * FROM "order"
        WHERE user_key = %s AND status = 'cart';
    """, (user["key"],))
    cart = cur.fetchone()
    if not cart:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = {}
    delivery_date = request.json.get("delivery_date")

    if not delivery_date:
        error["delivery_date"] = "This field is required"

    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    log(
        cur=cur,
        user_key=user["key"],
        action="edited_delivery_date",
        entity_key=cart["key"],
        entity_type="cart",
        misc={
            "from": cart["delivery_date"],
            "to": delivery_date
        }
    )

    cur.execute("""
        UPDATE "order" SET delivery_date = %s WHERE key = %s RETURNING *;
    """, (delivery_date, cart["key"]))
    cart = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "cart": cart
    })


@bp.put("/order/status/<key>")
def status(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "order:status" not in user["permissions"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute("""SELECT * FROM "order" WHERE key = %s;""", (key,))
    order = cur.fetchone()

    if order and order["user_key"] == user["key"]:
        order_user = user
    else:
        cur.execute("""SELECT * FROM "user" WHERE key = %s;""",
                    (order["user_key"],))
        order_user = cur.fetchone()

    if (
        not order or not order_user
        or "status" not in request.json
        or not request.json["status"]
        or request.json["status"] not in order_status[:-1]
        or "email_template" not in request.json
        or order["status"] in ["delivered", "canceled"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    i = order_status.index(order["status"])
    j = order_status.index(request.json["status"])
    if i + 1 != j and i - 1 != j:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if "note" not in request.json or not request.json["note"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "note": "this field is required"
        })

    if (
        order["status"] == "created"
        and not order["delivery_date"]
    ):
        new_date = datetime.now() + timedelta(days=4)
        new_date = new_date.replace(
            hour=10, minute=0, second=0, microsecond=0)

        log(
            cur=cur,
            user_key=user["key"],
            action="changed_date",
            entity_key=order["key"],
            entity_type="order",
            misc={
                "from": order["delivery_date"],
                "to": f'{new_date}'
            }
        )
        cur.execute("""
            UPDATE "order"
            SET delivery_date = %s
            WHERE key = %s;
        """, (
            new_date,
            order["key"]
        ))

    if order["status"] == "processing" and request.json['status'] == "created":
        log(
            cur=cur,
            user_key=user["key"],
            action="changed_date",
            entity_key=order["key"],
            entity_type="order",
            misc={
                "from": f"{order['delivery_date']}",
                "to": None
            }
        )

        cur.execute("""
            UPDATE "order"
            SET delivery_date = %s
            WHERE key = %s;
        """, (
            None,
            order["key"]
        ))

    log(
        cur=cur,
        user_key=user["key"],
        action="changed_status",
        entity_key=order["key"],
        entity_type="order",
        misc={
            "from": order['status'],
            "to": request.json['status'],
            "note": request.json["note"]
        }
    )

    cur.execute("""
        UPDATE "order"
        SET status = %s
        WHERE key = %s
        RETURNING *;
    """, (
        request.json["status"],
        order["key"]
    ))
    order = cur.fetchone()

    if request.json["status"] == "delivered":
        send_mail(
            order_user["email"],
            "Order Delivered - Thank you",
            request.json["email_template"].format(
                name=order_user["name"]
            )
        )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "order": order
    })


@bp.put("/order/cancel/<key>")
def cancel(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute("""SELECT * FROM "order" WHERE key = %s;""", (key,))
    order = cur.fetchone()
    cur.execute("""SELECT * FROM "user" WHERE key = %s;""",
                (order["user_key"],))
    order_user = cur.fetchone()

    if (
        "order:cancel" not in user["permissions"]
        and user["key"] != order_user["key"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    if (
        not order or not order_user
        or order["status"] in ["delivered", "canceled"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if (
        "note" not in request.json
        or not request.json["note"]
        or "email_template_admin" not in request.json
        or not request.json["email_template_admin"]
        or "email_template_user" not in request.json
        or not request.json["email_template_user"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "note": "this field is required"
        })

    log(
        cur=cur,
        user_key=user["key"],
        action="canceled",
        entity_key=order["key"],
        entity_type="order",
        misc={
            "from": order['status'],
            "to": "canceled",
            "note": request.json["note"]
        }
    )

    cur.execute("""
        UPDATE "order"
        SET status = 'canceled'
        WHERE key = %s
        RETURNING *;
    """, (key))
    order = cur.fetchone()

    send_mail(
        os.environ["MAIL_USERNAME"],
        "Cancelled Order",
        request.json["email_template_admin"]
    )
    send_mail(
        user["email"],
        "Cancelled Order",
        request.json["email_template_user"].format(
            user_name=order_user["name"]
        )
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "order": order
    })
