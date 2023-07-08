from flask import Blueprint, jsonify, request
from .tools import token_to_user, now
from .schema import user_schema, item_schema
from .database import database, query

bp = Blueprint("save", __name__)


def saved_items(saves, db):
    items = []
    for save in saves:
        item = query({"type": "item", "key": save["key"]}, db=db)
        if item:
            items.append(item_schema(item, db))

    return items


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
        "items": saved_items(user["saves"], db)
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
        "items": saved_items(user["saves"], db)
    })
