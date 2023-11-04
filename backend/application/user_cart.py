from flask import Blueprint, jsonify, request
from .tools import token_to_user, now
from .schema import user_schema, item_schema
from .database import database, query
from uuid import uuid4

bp = Blueprint("cart", __name__)


def cart_template(user):
    return {
        "key": f"{user['key']}_cart",
        "id": str(uuid4().hex)[:10],
        "user": user["key"],
        "v": uuid4().hex,
        "type": "cart",

        "date_c": now(),
        "date_u": now(),

        "items": [],

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

        "delivery_date": f"{now(4).split('T')[0]}T10:00",

        "transaction": {
            "delivery_fee": 1500,
            "total_items": 0,
            "account": 0,
            "pay": 0,
            "pay_reference": None,
        },
    }


def transaction(cart, db):
    cart["transaction"]["total_items"] = 0
    for x in cart["items"]:
        item = query({"type": "item", "key": x["key"]}, db=db)
        if not item:
            return jsonify({
                "status": 400,
                "error": "item not found"
            })
        cart["transaction"]["total_items"] += item["price"] * x["quantity"]
    return cart


def normalize_db(cart, db):
    exist = False

    for x in db:
        if x["key"] == cart["key"]:
            x = cart
            exist = True
            break

    if not exist:
        db.append(cart)

    return db


@bp.get("/cart")
def get_carts():
    db = database()
    user = token_to_user(db)

    cart = query({
        "type": "cart",
        "key": f"{user['key']}_cart",
        "user": user["key"]}, db=db)

    if not cart:
        cart = cart_template(user)

    items = []
    for x in cart["items"]:
        item = query({"type": "item", "key": x["key"]}, db=db)
        if item:
            item = item_schema(item, db)
            item["variation"] = x["variation"]
            item["quantity"] = x["quantity"]
            items.append(item)

    cart["items"] = items
    return jsonify({
        "status": 200,
        "cart": cart
    })


@bp.post("/cart")
def add_to_cart():
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if (
        "key" not in request.json
        or not request.json["key"]
        or "variation" not in request.json
        or "quantity" not in request.json
        or type(request.json["quantity"]) is not int
        or request.json["quantity"] < 0
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    item = query({"type": "item", "key": request.json["key"]}, db=db)
    if not item:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cart_item = {
        "key": request.json["key"],
        "variation": request.json["variation"],
        "quantity": request.json["quantity"]
    }

    cart = query({
        "type": "cart",
        "key": f"{user['key']}_cart",
        "user": user["key"],
    }, db=db)
    if not cart:
        cart = cart_template(user)

    exist = False
    for x in cart["items"]:
        if (
            x["key"] == cart_item["key"]
            and x["variation"] == cart_item["variation"]
        ):
            x["quantity"] += cart_item["quantity"]
            exist = True
            break

    if not exist:
        cart["items"].append(cart_item)

    cart = transaction(cart, db)
    cart["date_u"] = now()
    database(cart)

    db = normalize_db(cart, db)
    return jsonify({
        "status": 200,
        "user": user_schema(user, db)
    })


@bp.put("/cart_item_quantity")
def cart_item_quantity():
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if (
        "key" not in request.json
        or not request.json["key"]
        or "variation" not in request.json
        or "quantity" not in request.json
        or type(request.json["quantity"]) is not int
        or request.json["quantity"] < 0
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    item = query({"type": "item", "key": request.json["key"]}, db=db)
    cart = query({
        "type": "cart",
        "key": f"{user['key']}_cart",
        "user": user["key"],
    }, db=db)
    if not item or not cart:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    for x in cart["items"]:
        if (
            x["key"] == request.json["key"]
            and x["variation"] == request.json["variation"]
        ):
            if (request.json["quantity"] > 0):
                x["quantity"] = request.json["quantity"]

                cart = transaction(cart, db)
                cart["date_u"] = now()
                db = normalize_db(cart, db)
            else:
                cart = transaction(cart, db)
                cart["date_u"] = now()
                cart["items"].remove(x)
            break

    database(cart, len(cart["items"]) == 0)

    return jsonify({
        "status": 200,
        "user": user_schema(user, db)
    })
