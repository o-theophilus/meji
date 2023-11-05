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
    if not user["login"]:
        return jsonify({
            "status": 400,
            "error": "please login"
        })

    c_items = query({"type": "cart", "user": user["key"]}, True, db=db)
    if c_items == []:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    total_items = 0
    for x in c_items:
        item = query({"type": "item", "key": x["item"]}, db=db)
        if not item:
            return jsonify({
                "status": 400,
                "error": "item not found"
            })
        total_items += item["price"] * x["quantity"]

    order = {
        "key": str(uuid4().hex)[:10],
        "user": user["key"],
        "v": uuid4().hex,
        "type": "order",

        "date_c": now(),
        "date_u": now(),

        "receiver": {
            "name": user["name"],
            "phone": user["phone"],
            "address": {
                "line": None,
                "country": None,
                "state": None,
                "local_area": None,
                "postal_code": None,
            },
        },

        "items": c_items,

        # ordered, processing, enroute, delivered, canceled
        "status": "pending",
        "delivery_date": f"{now(4).split('T')[0]}T10:00",

        "info": {
            "delivery_fee": 1500,
            "total_items": total_items,
            "account": 0,
            "pay": 0,
            "pay_reference": None,
        },
    }

    log = log_template(
        user["key"],
        "created",
        order["key"],
        "order",
        200
    )

    database(c_items, True)
    database([order, log])

    return jsonify({
        "status": 200,
        "order_key": order["key"]
    })


@bp.post("/order/<key>")
def place_order(key):
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    order = query({"type": "order", "key": key}, db=db)
    if not order:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if order["status"] != "pending":
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if (
        "email_template" not in request.json
        or not request.json["email_template"]
        or "reference" not in request.json
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if (
        not order["receiver"]
        or not order["receiver"]["name"]
        or not order["receiver"]["phone"]
        or not order["receiver"]["address"]
        or not order["receiver"]["address"]["line"]
        or not order["receiver"]["address"]["state"]
        or not order["receiver"]["address"]["country"]
        or not order["receiver"]["address"]["postal_code"]
    ):
        return jsonify({
            "status": 400,
            "error": "invalid delivery address"
        })

    total_pay = order["info"]["total_items"] + order[
        "info"]["delivery_fee"] - order["info"]["account"]

    if total_pay > 0:
        if not request.json['reference']:
            return jsonify({
                "status": 400,
                "error": "invalid request"
            })

        for x in db:
            if (
                x["type"] == "order"
                and request.json['reference'] == x["info"]["pay_reference"]
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

    order["status"] = "ordered"
    order["info"]["pay"] = total_pay
    order["info"]["pay_reference"] = request.json['reference'] if request.json[
        'reference'] else None
    order["date_u"] = now()
    user["acc_balance"] -= order["info"]["account"]
    log = log_template(
        user["key"],
        "ordered",
        order["key"],
        "order",
    )

    database([user, order, log])

    send_mail(
        os.environ["MAIL_USERNAME"],
        "New Order",
        request.json["email_template"]
    )

    return jsonify({
        "status": 200,
        "order": order_schema(order, db),
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

    if "admin" not in user["roles"]:
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

    order["delivery_date"] = f"{request.json['date']}T{request.json['time']}"
    order["date_u"] = now()
    log = log_template(
        user["key"],
        "changed_delivery_date",
        order["key"],
        "order"
    )

    database([order, log])

    return jsonify({
        "status": 200,
        "order": order_schema(order, db)
    })


@bp.put("/order_account/<key>")
def submit_account(key):
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    order = query({"type": "order", "key": key}, db=db)
    if not order:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if order["status"] != "pending":
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if "value" not in request.json:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = None
    if type(request.json["value"]) is not int:
        error = "Please enter a valid value"
    elif request.json["value"] > user["acc_balance"]:
        error = "amount larger than available balance"
    elif request.json["value"] > order["info"][
            "total_items"] + order["info"]["delivery_fee"]:
        error = "amount larger than total cost "
    elif request.json["value"] < 0:
        error = "negative amount not allowed"
    if error:
        return jsonify({
            "status": 400,
            **error
        })

    order["info"]["account"] = request.json["value"]
    order["date_u"] = now()
    order = database(order)

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

    status = ['ordered', 'processing', 'enroute', 'delivered']
    order = query({"type": "order", "key": key}, db=db)
    order_user = query({"type": "user", "key": order["user"]}, db=db)

    if "admin" not in user["roles"] and user["key"] != order_user["key"]:
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    if (
        not order or not order_user
        or "status" not in request.json
        or not request.json["status"]
        or request.json["status"] not in status
        or "email_template" not in request.json
        or order["status"] in ["pending", "delivered", "canceled"]
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

    log = log_template(
        user["key"],
        "changed_status",
        order["key"],
        "order",
        misc={
            "change": f"from: {order['status']} to: {request.json['status']}",
            "note": request.json["note"]
        }
    )
    order["status"] = request.json["status"]
    order["date_u"] = now()

    database([order, log])

    if request.json["status"] in ["processing", "delivered"]:
        send_mail(
            order_user["email"],
            "New Order" if order["status"] == "delivered" else "Thank you",
            request.json["email_template"]
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

    if "admin" not in user["roles"] and user["key"] != order_user["key"]:
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

    if "note" not in request.json or not request.json["note"]:
        return jsonify({
            "status": 400,
            "note": "this field is required"
        })

    log = log_template(
        user["key"],
        "canceled",
        order["key"],
        "order",
        misc={
            "from": order["status"],
            "to": "canceled",
            "note": request.json["note"]
        }
    )
    order["status"] = "canceled"
    order["date_u"] = now()

    database([order, log])

    return jsonify({
        "status": 200,
        "order": order_schema(order, db)
    })
