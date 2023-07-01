from flask import Blueprint, jsonify, request
from .tools import token_to_user
from . import dd
from .database import database
from .schema import user_schema

bp = Blueprint("user_photo", __name__)


@bp.post("/photo_user/<key>")
def post_user(key):
    data = database

    user = token_to_user(data)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    if user["key"] != key:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    if 'file' not in request.files:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    file = request.files["file"]

    ext = file.filename.split(".")[-1]
    if ext.lower() not in ['jpg', 'png', 'gif']:
        return jsonify({
            "status": 201,
            "message": "invalid file type"
        })

    dd.rem(user['photo'])
    user["photo"] = dd.add(file)

    user = database(user)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "user": user_schema(user, data)
        }
    })


@bp.delete("/photo_user/<key>")
def delete_user(key):
    data = database

    me = token_to_user(data)
    if not me:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    user = None
    if me["key"] == key:
        user = me
    elif "admin" in me["roles"]:
        user = query("user", "key", key, data)
        if not user:
            return jsonify({
                "status": 401,
                "message": "invalid request"
            })
    else:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    if user["photo"]:

        dd.rem(user["photo"])
        user['photo'] = None
        user = database(user)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "user": user_schema(user, data)
        }
    })
