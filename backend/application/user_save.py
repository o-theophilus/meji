from flask import Blueprint, jsonify, request
from .tools import token_to_user, now
from .schema import user_schema, item_schema
from .database import database, query
from math import ceil
from uuid import uuid4

bp = Blueprint("save", __name__)


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

    total_page = ceil(len(items) / size)

    start = (page_no - 1) * size
    stop = start + size
    items = items[start: stop]

    return jsonify({
        "status": 200,
        "items": items,
        "total_page": total_page
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

    saved_item = query({
        "type": "save", "user": user["key"],
        "item": item["key"]}, db=db)

    if saved_item and not request.json["save"]:
        database(saved_item, True)
        db = [x for x in db if x["key"] != saved_item["key"]]

    elif not saved_item and request.json["save"]:
        save = database({
            "key": uuid4().hex,
            "date": now(),
            "type": "save",
            "user": user['key'],
            "item": item['key'],
        })
        db.append(save)

    return jsonify({
        "status": 200,
        "user": user_schema(user, db),
    })
