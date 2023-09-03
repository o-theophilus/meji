from flask import Blueprint, jsonify, request
from .tools import token_to_user, now
from .schema import user_schema, item_schema
from .database import database, query
from math import ceil
from uuid import uuid4

bp = Blueprint("save_cart", __name__)


@bp.get("/save")
def get_saves():
    db = database()
    user = token_to_user(db)

    page_no = 1
    size = 24

    items = []
    saves = query({"type": "save", "user": user["key"]}, True, db=db)
    saves = [x["item"] for x in saves]
    for x in db:
        if x["type"] == "item" and x["key"] in saves:
            items.append(item_schema(x, db))

    start = (page_no - 1) * size
    stop = start + size
    items = items[start: stop]

    return jsonify({
        "status": 200,
        "items": items,
        "total_page": ceil(len(items) / size)
    })


@bp.post("/save")
def save_item():
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
        or "save" not in request.json
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

    user_saved_item = query({
        "type": "save", "user": user["key"],
        "item": item["key"]}, db=db)

    if user_saved_item and not request.json["save"]:
        database(user_saved_item, True)
    elif not user_saved_item and request.json["save"]:
        database({
            "key": uuid4().hex,
            "date": now(),
            "type": "save",
            "user": user['key'],
            "item": item['key'],
        })

    return jsonify({
        "status": 200,
        "user": user_schema(user, db),
    })


@bp.get("/cart")
def get_carts():
    db = database()
    user = token_to_user(db)

    user_cart = query({"type": "cart", "user": user["key"]}, True, db=db)
    user_cart = sorted(user_cart, key=lambda d: d["date"])

    items = []
    for x in user_cart:
        item = query({"type": "item", "key": x["item"]}, db=db)
        if item:
            item = item_schema(item, db)
            item["variation"] = x["variation"]
            item["quantity"] = x["quantity"]
            items.append(item)

    return jsonify({
        "status": 200,
        "items": items
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
        or type(request.json["quantity"]) != int
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

    cart_item = query({
        "type": "cart", "user": user["key"], "item": item["key"],
        "variation": request.json["variation"]
    }, db=db)

    if cart_item:
        if request.json["quantity"] < 1:
            database(cart_item, True)
            db = [x for x in db if x["key"] != cart_item["key"]]
        elif "ops" in request.json and request.json["ops"] == "add":
            cart_item["quantity"] += request.json["quantity"]
            database(cart_item)
        else:
            cart_item["quantity"] = request.json["quantity"]
            database(cart_item)

    elif request.json["quantity"] > 0:
        cart_item = database({
            "key": uuid4().hex,
            "date": now(),
            "type": "cart",
            "user": user["key"],
            "item": item["key"],
            "variation": request.json["variation"],
            "quantity": request.json["quantity"]
        })
        db.append(cart_item)

    return jsonify({
        "status": 200,
        "user": user_schema(user, db)
    })
