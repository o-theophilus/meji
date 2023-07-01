from flask import Blueprint, jsonify, request
from .tools import token_to_user, now
from .database import database
from .schema import user_schema, log_template
from uuid import uuid4

bp = Blueprint("cart", __name__)


@bp.post("/cart/<key>")
def post(key):
    data = database()

    user = token_to_user(data)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    item = query("item", "key", key, data)
    if not item:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    if (
        "variation" not in request.json
        or "quantity" not in request.json
        or not request.json["quantity"]
    ):
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    def _user():
        for cart_item in user["cart"]:
            if (
                cart_item["key"] == item["key"] and
                cart_item["variation"] == request.json["variation"]
            ):
                if (
                    "operation" in request.json
                    and request.json["operation"]
                ):
                    cart_item["quantity"] += request.json["quantity"]
                else:
                    cart_item["quantity"] = request.json["quantity"]
                return

        cart = {
            "key": item["key"],
            "date": now(),
            "variation": request.json["variation"],
            "quantity": request.json["quantity"]
        }
        user["cart"].append(cart)

    _user()
    user = database(user)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "user": user_schema(user, data)
        }
    })


@bp.delete("/cart/<key>")
def delete(key):
    data = database()

    user = token_to_user(data)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    if "variation" not in request.json:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    temp = []
    for cart in user["cart"]:
        if (
            cart["key"] != key
            or cart["variation"] != request.json["variation"]
        ):
            temp.append(cart)

    user["cart"] = temp
    user = database(user)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "user": user_schema(user, data)
        }
    })


@bp.post("/order")
def cart_to_order():
    data = database()

    user = token_to_user(data)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })
    if not user["login"]:
        return jsonify({
            "status": 102,
            "message": "please login"
        })

    if user["cart"] == []:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    delivery_fee = 1500
    total_items = 0
    for cart in user["cart"]:
        item = query("item", "key", cart["key"], data)
        if not item:
            return jsonify({
                "status": 201,
                "message": "item not found"
            })
        total_items += item["price"] * cart["quantity"]

    order = {
        "key": str(uuid4().hex)[:10],
        "user_key": user["key"],
        "v": uuid4().hex,
        "type": "order",
        "pay_reference": None,

        "date_c": now(),
        "date_u": now(),

        "recipient": {
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

        "cart": user["cart"],

        "status": "pending",
        "delivery_date": f"{now(4).split('T')[0]}T10:00",

        "info": {
            "delivery_fee": delivery_fee,
            "total_items": total_items,
            "account": 0,
        },
    }

    log = log_template(
        "order",
        user["key"],
        order["key"],
        "cart_to_order",
        200
    )

    user["cart"] = []

    database([user, order, log])

    return jsonify({

        "status": 200,
        "message": "successful",
        "data": {
            "user": user_schema(user, data),
            "order_key": order["key"]
        }
    })
