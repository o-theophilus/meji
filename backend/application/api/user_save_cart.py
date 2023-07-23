from flask import Blueprint, jsonify, request
from .tools import token_to_user, now
from .schema import user_schema, item_schema
from .database import database, query
from math import ceil

bp = Blueprint("save_cart", __name__)


def saved_items(saves, db, page_no=1, size=24):
    items = []
    saves = [x["key"] for x in saves]
    for x in db:
        if x["type"] == "item" and x["key"] in saves:
            items.append(item_schema(x, db))

    total_page = ceil(len(items) / size)

    start = (page_no - 1) * size
    stop = start + size
    items = items[start: stop]

    return {
        "items": items,
        "total_page": total_page
    }


@bp.get("/save")
def get_saved_items():
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    return jsonify({
        "status": 200,
        **saved_items(user["saves"], db)
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

    new_saves = request.json["saves"]
    saves = []
    for item in user["saves"]:
        if item["key"] in new_saves:
            saves.append(item)
            new_saves.remove(item["key"])

    for key in new_saves:
        item = query({"type": "item", "key": key}, db=db)
        if item:
            saves.append({
                "key": key,
                "date": now()
            })

    user["saves"] = saves
    user = database(user)

    return jsonify({
        "status": 200,
        "user": user_schema(user, db),
        **saved_items(user["saves"], db)
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

    variation = request.json["variation"]
    quantity = int(request.json["quantity"])

    exist = False
    for x in user["cart"]:
        if x["key"] == item["key"] and x["variation"] == variation:
            exist = True

            if quantity < 1:
                user["cart"].remove(x)
                break
            elif "ops" in request.json and request.json["ops"] == "add":
                quantity += x["quantity"]
            x["quantity"] = quantity
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
