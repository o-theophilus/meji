from flask import Blueprint, jsonify, request
from .tools import token_to_user, now
from werkzeug.security import check_password_hash
from .schema import user_schema
from .database import database
from datetime import timedelta, datetime


bp = Blueprint("user", __name__)


@bp.get("/user/<key>")
def get(key):
    data = database()

    user = query("user", "key", key, data)
    if not user:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "user": user_schema(user, data)
        }
    })


@ bp.put("/user_name/<key>")
def edit_name(key):
    data = database()

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

    if "name" not in request.json or not request.json["name"]:
        return jsonify({
            "status": 201,
            "message": "this field is required"
        })

    user["name"] = request.json["name"]
    user["date_u"] = now(),
    user = database(user)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "user": user_schema(user, data)
        }
    })


@ bp.put("/user_phone")
def edit_phone():
    data = database()

    user = token_to_user(data)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    if "phone" not in request.json or not request.json["phone"]:
        return jsonify({
            "status": 201,
            "message": "this field is required"
        })

    user["phone"] = request.json["phone"]
    user["date_u"] = now(),
    user = database(user)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "user": user_schema(user, data)
        }
    })


@ bp.put("/user_address")
def edit_address():
    data = database()

    user = token_to_user(data)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    error = {}
    if "address" not in request.json or not request.json["address"]:
        error["address"] = "this field is required"
    if "state" not in request.json or not request.json["state"]:
        error["state"] = "this field is required"
    if "country" not in request.json or not request.json["country"]:
        error["country"] = "this field is required"
    if "local_area" not in request.json or not request.json["local_area"]:
        error["local_area"] = "this field is required"
    if "postal_code" not in request.json or not request.json["postal_code"]:
        error["postal_code"] = "this field is required"

    if error != {}:
        return jsonify({
            "status": 201,
            "message": error
        })

    user["address"] = {
        "address": request.json["address"],
        "state": request.json["state"],
        "country": request.json["country"],
        "local_area": request.json["local_area"],
        "postal_code": request.json["postal_code"],
    }
    user["date_u"] = now(),

    user = database(user)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "user": user_schema(user, data)
        }
    })


@ bp.delete("/user")
def delete():
    data = database()

    user = token_to_user(data)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    if not request.json["password"]:
        return jsonify({
            "status": 201,
            "message": "this field is required"
        })

    if not check_password_hash(user["password"], request.json["password"]):
        return jsonify({
            "status": 201,
            "message": "incorrect password"
        })

    user["key"] = "deleted"
    user = database(user)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "user": user_schema(user, data)
        }
    })


@bp.post("/setting")
def post():
    data = database()

    user = token_to_user(data)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    if "theme" in request.json and request.json["theme"]:
        user["setting"]["theme"] = request.json["theme"]
    if "item_view" in request.json and request.json["item_view"]:
        user["setting"]["item_view"] = request.json["item_view"]

    user = database(user)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "user": user_schema(user, data),
        }
    })


def unused_anon():
    data = database()

    keys = []
    for row in data:
        if (
            row["type"] == "user"
            and row["status"] == "anon"
            and row["saves"] == []
            and row["cart"] == []
        ):
            created = datetime.strptime(row["date_c"], '%Y-%m-%dT%H:%M:%S')
            _24hour_ago = datetime.now() - timedelta(days=1)

            if created < _24hour_ago:
                keys.append(row["key"])

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "keys": keys
        }
    })
