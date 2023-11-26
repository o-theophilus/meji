from flask import Blueprint, jsonify, request
from .tools import token_to_user, now
from .schema import user_schema, item_schema
from .database import database, query
from uuid import uuid4
from .log import log_template

bp = Blueprint("cart", __name__)


def cart_template(user):
    return {
        "key": f"{user['key']}_cart",
        "user": user["key"],
        "v": uuid4().hex,
        "type": "cart",

        "date_c": now(),
        "date_u": now(),

        "items": [],

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
def get_cart():
    db = database()
    user = token_to_user(db)

    cart = query({
        "type": "cart",
        "key": f"{user['key']}_cart",
        "user": user["key"]}, db=db)

    if not cart:
        cart = cart_template(user)
    elif cart["transaction"]["account"] > user["acc_balance"]:
        cart["transaction"]["account"] = 0
        database(cart)

    items = []
    for x in cart["items"]:
        item = query({"type": "item", "key": x["key"]}, db=db)
        if item:
            item = item_schema(item, db)
            item["variation"] = x["variation"]
            item["quantity"] = x["quantity"]
            items.append(item)
    cart["items"] = items

    previous_receivers = []
    for x in db:
        if (
            x["type"] == "order"
            and x["user"] == user["key"]
            and x["status"] == "delivered"
        ):
            previous_receivers.append({
                "name": x["receiver"]["name"],
                "phone": x["receiver"]["phone"],
                "address": x["receiver"]["address"],
                "date": x["date_u"],
            })
    previous_receivers = sorted(previous_receivers, key=lambda d: d['date'])

    database(log_template(
        user["key"],
        "viewed",
        cart["key"],
        "cart"
    ), db_name="log")

    return jsonify({
        "status": 200,
        "cart": cart,
        "previous_receivers": previous_receivers[:5]
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

    database(log_template(
        user["key"],
        "added_to",
        cart["key"],
        "cart",
        misc={
            "key": request.json["key"],
            **request.json["variation"],
            "quantity": request.json["quantity"]
        }
    ), db_name="log")

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

    log = log_template(
        user["key"],
        "changed_quantity",
        cart["key"],
        "cart",
        misc={
            "key": request.json["key"],
            **request.json["variation"]
        }
    )

    for x in cart["items"]:
        if (
            x["key"] == request.json["key"]
            and x["variation"] == request.json["variation"]
        ):
            if (request.json["quantity"] > 0):
                log["misc"]["from"] = x["quantity"]
                log["misc"]["to"] = request.json["quantity"]
                x["quantity"] = request.json["quantity"]
                cart["date_u"] = now()
                cart = transaction(cart, db)
                db = normalize_db(cart, db)
            else:
                cart["items"].remove(x)
                cart["date_u"] = now()
                cart = transaction(cart, db)
                log["action"] = "removed_from"
            break

    database(cart, len(cart["items"]) == 0)
    if len(cart["items"]) == 0:
        cart = cart_template(user)

    database(log, db_name="log")

    return jsonify({
        "status": 200,
        "user": user_schema(user, db),
        "cart": cart
    })


@bp.put("/cart_receiver")
def cart_receiver():
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
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
            "status": 400,
            **error
        })

    cart = query({
        "type": "cart",
        "key": f"{user['key']}_cart",
        "user": user["key"]}, db=db)
    if not cart or len(cart["items"]) == 0:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    log = log_template(
        user["key"],
        "edited_receiver",
        cart["key"],
        "cart"
    )
    log["misc"]["from"] = f"""
    name: {cart["receiver"]["name"]} |
    phone: {cart["receiver"]["phone"]} |
    address: {cart["receiver"]["address"]["line"]} |
    address: {cart["receiver"]["address"]["state"]} |
    address: {cart["receiver"]["address"]["country"]} |
    address: {cart["receiver"]["address"]["local_area"]} |
    address: {cart["receiver"]["address"]["postal_code"]}
    """

    cart["receiver"]["name"] = request.json["name"]
    cart["receiver"]["phone"] = request.json["phone"]
    cart["receiver"]["address"] = {
        "line": request.json["address"]["line"],
        "state": request.json["address"]["state"],
        "country": request.json["address"]["country"],
        "local_area": request.json["address"]["local_area"],
        "postal_code": request.json["address"]["postal_code"],
    }
    cart["date_u"] = now()

    log["misc"]["to"] = f"""
    name: {cart["receiver"]["name"]} |
    phone: {cart["receiver"]["phone"]} |
    address: {cart["receiver"]["address"]["line"]} |
    address: {cart["receiver"]["address"]["state"]} |
    address: {cart["receiver"]["address"]["country"]} |
    address: {cart["receiver"]["address"]["local_area"]} |
    address: {cart["receiver"]["address"]["postal_code"]}
    """

    cart = database(cart)
    database(log, db_name="log")

    return jsonify({
        "status": 200,
        "cart": cart
    })


@bp.put("/cart_account")
def cart_account():
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
    if not cart:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = None
    if "amount" not in request.json:
        error = "invalid request"
    elif (
        type(request.json["amount"]) not in [int, float]
        or request.json["amount"] < 0
    ):
        error = "Please enter a valid amount"
    elif request.json["amount"] > user["acc_balance"]:
        error = "amount larger than available balance"
    elif request.json["amount"] > cart["transaction"][
            "total_items"] + cart["transaction"]["delivery_fee"]:
        error = "amount larger than total cost "
    if error:
        return jsonify({
            "status": 400,
            "amount": error
        })

    database(log_template(
        user["key"],
        "changed_amount",
        cart["key"],
        "cart",
        misc={
            "from": cart["transaction"]["account"],
            "to": request.json["amount"]
        }
    ), db_name="log")

    cart["transaction"]["account"] = request.json["amount"]
    cart["date_u"] = now()
    cart = database(cart)

    return jsonify({
        "status": 200,
        "cart": cart
    })
