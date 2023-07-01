from flask import Blueprint, jsonify, request, current_app
from .tools import token_to_user, now
from .mail import notify, send_mail
from .schema import order_schema, user_schema, log_template
from .database import database
from uuid import uuid4
import requests

bp = Blueprint("order", __name__)


@bp.put("/order/<key>")
def submit_address(key):
    data = database()

    user = token_to_user(data)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    error = {}
    if "name" not in request.json or not request.json["name"]:
        error["name"] = "this field is required"
    if "phone" not in request.json or not request.json["phone"]:
        error["phone"] = "this field is required"

    if "address" not in request.json or not request.json["address"]:
        error["line"] = "this field is required"
        error["state"] = "this field is required"
        error["country"] = "this field is required"
        error["postal_code"] = "this field is required"
    else:
        if (
            "line" not in request.json["address"]
            or not request.json["address"]["line"]
        ):
            error["address"] = "this field is required"
        if (
            "state" not in request.json["address"]
            or not request.json["address"]["state"]
        ):
            error["state"] = "this field is required"
        if (
            "country" not in request.json["address"]
            or not request.json["address"]["country"]
        ):
            error["country"] = "this field is required"
        if (
            "postal_code" not in request.json["address"]
            or not request.json["address"]["postal_code"]
        ):
            error["postal_code"] = "this field is required"

    if error != {}:
        return jsonify({
            "status": 201,
            "message": error
        })

    order = query("order", "key", key, data)
    if not order:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    if order["status"] != "pending":
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    order["recipient"]["name"] = request.json["name"]
    order["recipient"]["phone"] = request.json["phone"]
    order["recipient"]["address"] = {
        "line": request.json["address"]["line"],
        "state": request.json["address"]["state"],
        "country": request.json["address"]["country"],
        "local_area": request.json["address"]["local_area"],
        "postal_code": request.json["address"]["postal_code"],
    }
    order["date_u"] = now()

    order = database(order)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "order": order_schema(order, data)
        }
    })


@bp.put("/order_/<key>")
def submit_account(key):
    data = database()

    user = token_to_user(data)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    order = query("order", "key", key, data)
    if not order:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    if order["status"] != "pending":
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    if "value" not in request.json:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    error = None
    if type(request.json["value"]) != int:
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
            "status": 201,
            "message": error
        })

    order["info"]["account"] = request.json["value"]
    order["date_u"] = now()
    order = database(order)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "order": order_schema(order, data)
        }
    })


@bp.post("/order/<key>")
def place_order(key):
    data = database()

    user = token_to_user(data)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    order = query("order", "key", key, data)
    if not order:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    if order["status"] != "pending":
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    if (
        "mail_content" not in request.json
        or not request.json["mail_content"]
        or "reference" not in request.json
    ):
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    if (
        not order["recipient"]
        or not order["recipient"]["name"]
        or not order["recipient"]["phone"]
        or not order["recipient"]["address"]
        or not order["recipient"]["address"]["line"]
        or not order["recipient"]["address"]["state"]
        or not order["recipient"]["address"]["country"]
        or not order["recipient"]["address"]["postal_code"]
    ):
        return jsonify({
            "status": 201,
            "message": "invalid delivery address"
        })

    total_pay = order["info"]["total_items"] + order["info"]["delivery_fee"]
    total_pay -= order["info"]["account"]

    if (total_pay > 0):
        ref = request.json["reference"]
        resp = requests.get(
            f'https://api.paystack.co/transaction/verify/{ref}',
            headers={
                'Content-Type': 'application/json',
                "Authorization": current_app.config["PAYSTACK_KEY"]
            }
        )
        pay_info = resp.json()

        if (
            not pay_info["status"]
            or "data" not in pay_info
            or "status" not in pay_info["data"]
            or "reference" not in pay_info["data"]
            or "amount" not in pay_info["data"]
            or "currency" not in pay_info["data"]
            or pay_info["data"]["status"] != "success"
            or pay_info["data"]["reference"] != request.json["reference"]
            or pay_info["data"]["amount"]/100 != total_pay
            or pay_info["data"]["currency"] != "NGN"

        ):
            return jsonify({
                "status": 401,
                "message": "invalid transaction"
            })

    order["status"] = "ordered"
    user["acc_balance"] -= order["info"]["account"]

    notify(
        "New Order",
        request.json["mail_content"],
        f"""
        User: {user['email']},\n
        Order Key: {order['key']},\n
        Payment Status: {order['status']}
        """
    )

    log = log_template(
        "order",
        user["key"],
        order["key"],
        "place_order",
        200,
        order['status']
    )

    order["date_u"] = now()
    database([user, order, log])

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "order": order_schema(order, data),
            "user": user_schema(user, data)
        }
    })


@bp.put("/order_status/<key>")
def status(key):
    data = database()

    user = token_to_user(data)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    if "admin" not in user["roles"]:
        return jsonify({
            "status": 102,
            "message": "unauthorised access"
        })

    order = query("order", "key", key, data)
    if not order:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    _order_user = query("user", "key", order["user_key"], data)
    if not _order_user:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    if (
        "status" not in request.json
        or not request.json["status"]
        or "mail_content" not in request.json
        or order["status"] == "pending"
    ):
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    status = ['pending', 'ordered', 'processing', 'enroute', 'delivered']
    i = status.index(order["status"])
    i = i - 1 if request.json["status"] == "previous" else i + 1

    if i < 0 or i > len(status) - 1:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    order["status"] = status[i]
    order["date_u"] = now()

    log = log_template
    log["key"] = uuid4().hex
    log["for"] = "order"
    log["user_key"] = user["key"]
    log["entity_key"] = order["key"]
    log["action"] = "change_status"
    log["result"] = "successful"
    log["note"] = request.json["status"]

    database([order, log])

    _order = order_schema(order, data)

    if (
        request.json["status"] == "next"
        and order["status"] in ["processing", "delivered"]
    ):
        subject = "New Order"
        if order["status"] == "delivered":
            subject = "Thank you"

        send_mail(_order_user["email"], subject,
                  request.json["mail_content"])

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "order": _order
        }
    })


@bp.put("/order_date/<key>")
def date(key):
    data = database()

    user = token_to_user(data)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    if "admin" not in user["roles"]:
        return jsonify({
            "status": 102,
            "message": "unauthorised access"
        })

    order = query("order", "key", key, data)
    if not order:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    error = {}

    if "date" not in request.json or not request.json["date"]:
        error["date"] = "this field is required"

    if "time" not in request.json or not request.json["time"]:
        error["time"] = "this field is required"

    if error != {}:
        return jsonify({
            "status": 201,
            "message": error
        })

    date = f"{request.json['date']}T{request.json['time']}"
    order["delivery_date"] = date

    order["date_u"] = now()

    log = log_template
    log["key"] = uuid4().hex
    log["for"] = "order"
    log["user_key"] = user["key"]
    log["entity_key"] = order["key"]
    log["action"] = "change_delivery_date"
    log["result"] = "successful"
    log["note"] = date

    database([order, log])

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "order": order_schema(order, data)
        }
    })
