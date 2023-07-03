from flask import Blueprint, jsonify
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
            "status": 401,
            "error": "invalid token"
        })

    return jsonify({
        "status": 200,
        "items": saved_items(user["saves"], db)
    })


@bp.post("/save/<key>")
def save_item(key):
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 401,
            "error": "invalid token"
        })

    item = query({"type": "item", "key": key}, db=db)
    if not item:
        return jsonify({
            "status": 401,
            "error": "invalid request"
        })

    item_removed = False
    for save in user["saves"]:
        if save["key"] == key:
            item_removed = True
            user["saves"].remove(save)
            break

    if not item_removed:
        user["saves"].append({
            "key": key,
            "date": now()
        })

    user = database(user)

    return jsonify({
        "status": 200,
        "user": user_schema(user, db),
        "items": saved_items(user["saves"], db)
    })
