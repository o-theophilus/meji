from flask import Blueprint, jsonify, request
from .tools import token_to_user, now
from .database import database, query
from .schema import user_schema, log_template
from uuid import uuid4

bp = Blueprint("cart", __name__)


@bp.post("/cart")
def add_to_cart():
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 401,
            "error": "invalid token"
        })

    if (
        "key" not in request.json
        or not request.json["key"]
        or "variation" not in request.json
        or "quantity" not in request.json
    ):
        return jsonify({
            "status": 401,
            "error": "invalid request"
        })

    item = query({"type": "item", "key": request.json["key"]}, db=db)
    if not item:
        return jsonify({
            "status": 401,
            "error": "invalid request"
        })

    variation = request.json["variation"]
    quantity = int(request.json["quantity"])

    exist = False
    for ci in user["cart"]:
        if ci["key"] == item["key"] and ci["variation"] == variation:
            exist = True

            if quantity < 1:
                user["cart"].remove(ci)
                break
            elif "ops" in request.json and request.json["ops"] == "add":
                quantity += ci["quantity"]
            ci["quantity"] = quantity
            break

    if not exist:
        user["cart"].append({
            "key": item["key"],
            "date": now(),
            "variation": variation,
            "quantity": quantity
        })

    user = database(user)

    return jsonify({
        "status": 200,
        "user": user_schema(user, db)
    })


@bp.post("/order")
def cart_to_order():
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 401,
            "error": "invalid token"
        })
    if not user["login"]:
        return jsonify({
            "status": 401,
            "error": "please login"
        })

    if user["cart"] == []:
        return jsonify({
            "status": 401,
            "error": "invalid request"
        })

    delivery_fee = 1500
    total_items = 0
    for cart in user["cart"]:
        item = query("item", "key", cart["key"], db)
        if not item:
            return jsonify({
                "status": 401,
                "error": "item not found"
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
        "user": user_schema(user, db),
        "order_key": order["key"]
    })
