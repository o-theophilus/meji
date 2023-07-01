from flask import Blueprint, jsonify
from .tools import token_to_user, now
from .schema import user_schema
from .database import database

bp = Blueprint("save", __name__)


@bp.put("/save/<key>")
def put(key):
    data = database()

    user = token_to_user(data)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    wasSaved = False
    saves = []
    for save in user["saves"]:
        if save["key"] == key:
            wasSaved = True
        else:
            saves.append(save)

    if wasSaved:
        user["saves"] = saves
    else:
        item = query("item", "key", key, data)
        save = {
            "key": item["key"],
            "date": now()
        }
        user["saves"].append(save)

    user = database(user)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "user": user_schema(user, data)
        }
    })
