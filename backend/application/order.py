from flask import Blueprint, jsonify, request
from .tools import token_to_user, now, send_mail
from .schema import order_schema, user_schema
from .log import log_template
from .database import database, query
from uuid import uuid4
import requests
import os

bp = Blueprint("order", __name__)


@bp.post("/order")
def cart_to_order():
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    cart = query({
        "type": "cart",
        "key": f"{user['key']}_cart",
        "user": user["key"]}, db=db)

    if (
        not cart
        or "email_template_admin" not in request.json
        or not request.json["email_template_admin"]
        or "email_template_user" not in request.json
        or not request.json["email_template_user"]
        or "reference" not in request.json
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if (
        not cart["receiver"]
        or not cart["receiver"]["name"]
        or not cart["receiver"]["phone"]
        or not cart["receiver"]["address"]
        or not cart["receiver"]["address"]["line"]
        or not cart["receiver"]["address"]["state"]
        or not cart["receiver"]["address"]["country"]
        or not cart["receiver"]["address"]["postal_code"]
    ):
        return jsonify({
            "status": 400,
            "error": "invalid delivery address"
        })

    total_pay = cart["transaction"]["total_items"] + cart[
        "transaction"]["delivery_fee"] - cart["transaction"]["account"]

    if total_pay > 0:
        if not request.json['reference']:
            return jsonify({
                "status": 400,
                "error": "invalid request"
            })

        for x in db:
            if (
                x["type"] == "order"
                and x["transaction"][
                    "pay_reference"] == request.json['reference']
            ):
                return jsonify({
                    "status": 400,
                    "error": "invalid request"
                })

        ref = request.json['reference']
        resp = requests.get(
            f"https://api.paystack.co/transaction/verify/{ref}",
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
            or resp["data"]["reference"] != request.json["reference"]
            or "amount" not in resp["data"]
            or resp["data"]["amount"]/100 != total_pay
            or "currency" not in resp["data"]
            or resp["data"]["currency"] != "NGN"
        ):
            return jsonify({
                "status": 400,
                "error": "invalid transaction"
            })

    cart["key"] = str(uuid4().hex)[:10]
    cart["type"] = "order"
    cart["status"] = "created"
    cart["transaction"]["pay"] = total_pay
    cart["transaction"]["pay_reference"] = request.json[
        'reference'] if request.json['reference'] else None
    cart["date_u"] = now()

    database(log_template(
        user["key"],
        "created",
        cart["key"],
        "order",
        misc={
            "value": cart["transaction"]["account"],
            "balance": user["acc_balance"],
            "new_balance": user["acc_balance"] - cart["transaction"]["account"]
        }
    ), db_name="log")

    user["acc_balance"] -= cart["transaction"]["account"]
    database(f"{user['key']}_cart", True)
    database([user, cart])

    send_mail(
        os.environ["MAIL_USERNAME"],
        "New Order",
        request.json["email_template_admin"].format(
            order_key=cart["key"]
        )
    )
    send_mail(
        user["email"],
        "Processing Order",
        request.json["email_template_user"].format(
            order_key=cart["key"]
        )
    )

    return jsonify({
        "status": 200,
        "order": order_schema(cart, db),
        "user": user_schema(user, db)
    })


@bp.put("/order_eta/<key>")
def date(key):
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "order:edit_eta" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    order = query({"type": "order", "key": key}, db=db)
    if not order:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = {}

    if "date" not in request.json or not request.json["date"]:
        error["date"] = "this field is required"

    if "time" not in request.json or not request.json["time"]:
        error["time"] = "this field is required"

    if error != {}:
        return jsonify({
            "status": 400,
            **error
        })

    database(log_template(
        user["key"],
        "changed_delivery_date",
        order["key"],
        "order",
        misc={
            "from": order["delivery_date"],
            "to": f"{request.json['date']}T{request.json['time']}"
        }
    ), db_name="log")

    order["delivery_date"] = f"{request.json['date']}T{request.json['time']}"
    order["date_u"] = now()
    database(order)

    return jsonify({
        "status": 200,
        "order": order_schema(order, db)
    })


@bp.put("/order_status/<key>")
def status(key):
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "order:status" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    status = ['created', 'processing', 'enroute', 'delivered']
    order = query({"type": "order", "key": key}, db=db)

    if order and order["user"] == user["key"]:
        order_user = user
    else:
        order_user = query({"type": "user", "key": order["user"]}, db=db)

    if (
        not order or not order_user
        or "status" not in request.json
        or not request.json["status"]
        or request.json["status"] not in status
        or "email_template" not in request.json
        or order["status"] in ["delivered", "canceled"]
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    i = status.index(order["status"])
    j = status.index(request.json["status"])
    if i + 1 != j and i - 1 != j:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if "note" not in request.json or not request.json["note"]:
        return jsonify({
            "status": 400,
            "note": "this field is required"
        })

    database(log_template(
        user["key"],
        "changed_status",
        order["key"],
        "order",
        misc={
            "from": order['status'],
            "to": request.json['status'],
            "note": request.json["note"]
        }
    ), db_name="log")

    order["status"] = request.json["status"]
    order["date_u"] = now()
    database(order)

    if request.json["status"] == "delivered":
        send_mail(
            order_user["email"],
            "Order Delivered - Thank you",
            request.json["email_template"].format(
                name=order_user["name"]
            )
        )

    return jsonify({
        "status": 200,
        "order": order_schema(order, db)
    })


@bp.put("/order_status_cancel/<key>")
def status_cancel(key):
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    order = query({"type": "order", "key": key}, db=db)
    order_user = query({"type": "user", "key": order["user"]}, db=db)

    if (
        "order:cancel" not in user["roles"]
        and user["key"] != order_user["key"]
    ):
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    if (
        not order or not order_user
        or order["status"] in ["delivered", "canceled"]
    ):
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
        return jsonify({
            "status": 400,
            "note": "this field is required"
        })

    database(log_template(
        user["key"],
        "canceled",
        order["key"],
        "order",
        misc={
            "from": order["status"],
            "to": "canceled",
            "note": request.json["note"]
        }
    ), db_name="log")

    order["status"] = "canceled"
    order["date_u"] = now()
    database(order)

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

    return jsonify({
        "status": 200,
        "order": order_schema(order, db)
    })
