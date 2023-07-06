from flask import Blueprint, jsonify, request, current_app
from .tools import token_to_user, now, token_tool
from werkzeug.security import check_password_hash
from .schema import user_schema
from .database import database, query
from .mail import send_mail
import re
from werkzeug.security import generate_password_hash
from .storage import storage


bp = Blueprint("user", __name__)


@bp.get("/user/<key>")
def get(key):
    db = database()

    user = query({"type": "user", "key": key}, db=db)
    if not user:
        return jsonify({
            "status": 401,
            "error": "invalid request"
        })

    return jsonify({
        "status": 200,
        "user": user_schema(user, db)
    })


@ bp.put("/user_name/<key>")
def edit_name(key):
    db = database()

    me = token_to_user(db)
    if not me:
        return jsonify({
            "status": 401,
            "error": "invalid token"
        })

    user = None
    if me["key"] == key:
        user = me
    elif "admin" in me["roles"]:
        user = query({"type": "user", "key": key}, db=db)
        if not user:
            return jsonify({
                "status": 401,
                "error": "invalid request"
            })
    else:
        return jsonify({
            "status": 401,
            "error": "invalid request"
        })

    if "name" not in request.json or not request.json["name"]:
        return jsonify({
            "status": 401,
            "error": "this field is required"
        })

    user["name"] = request.json["name"]
    user["date_u"] = now(),
    user = database(user)

    return jsonify({
        "status": 200,
        "user": user_schema(user, db)
    })


@ bp.put("/user_phone")
def edit_phone():
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 401,
            "error": "invalid token"
        })

    if "phone" not in request.json or not request.json["phone"]:
        return jsonify({
            "status": 401,
            "error": "this field is required"
        })

    user["phone"] = request.json["phone"]
    user["date_u"] = now(),
    user = database(user)

    return jsonify({
        "status": 200,
        "user": user_schema(user, db)
    })


@ bp.put("/user_address")
def edit_address():
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 401,
            "error": "invalid token"
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
            "status": 401,
            **error
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
        "user": user_schema(user, db)
    })


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

    storage(user['photo'], delete=True)
    user["photo"] = storage(file)

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

        storage(user["photo"], delete=True)
        user['photo'] = None
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
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 401,
            "error": "invalid token"
        })

    if "theme" in request.json and request.json["theme"]:
        user["setting"]["theme"] = request.json["theme"]
    if "item_view" in request.json and request.json["item_view"]:
        user["setting"]["item_view"] = request.json["item_view"]

    user = database(user)

    return jsonify({
        "status": 200,
        "user": user_schema(user, db),
    })


@bp.post("/email")
def email():
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 401,
            "error": "invalid token"
        })

    if (
        "mail_content" not in request.json
        or not request.json["mail_content"]
    ):
        return jsonify({
            "status": 401,
            "error": "invalid request"
        })

    token = token_tool().dumps(user["key"])
    mail = request.json['mail_content'].format(token=token)
    send_mail(user["email"], "Welcome!", mail)

    return jsonify({
        "status": 200,
        "error": "email change email sent",
    })


@bp.post("/email/<token>")
def email_(token):
    db = database()

    try:
        token = token_tool().loads(
            token, max_age=current_app.config["EMAIL_CONFIRM_EXP"])
    except Exception:
        return jsonify({
            "status": 401,
            "error": "invalid token"
        })

    user = token_to_user(db)
    token_user = query({"type": "user", "key": token}, db=db)
    if not token_user or not user or token_user["key"] != user["key"]:
        return jsonify({
            "status": 401,
            "error": "invalid token"
        })

    error = None
    if "email" not in request.json or not request.json["email"]:
        error = "This field is required"
    elif not re.match(r"\S+@\S+\.\S+", request.json["email"]):
        error = "Please enter a valid email"
    elif user["email"] == request.json["email"]:
        error = "please use a different email form your current email"
    elif query({"type": "user", "email": request.json["email"]}, db=db):
        error = "email is already in use"
    if error:
        return jsonify({
            "status": 401,
            **error
        })

    user["email"] = request.json["email"]
    user = database(user)

    return jsonify({
        "status": 200,
        "user": user_schema(user, db)
    })


@bp.post("/password")
def password():
    db = database

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 401,
            "error": "invalid token"
        })

    if (
       "mail_content" not in request.json
        or not request.json["mail_content"]
       ):
        return jsonify({
            "status": 401,
            "error": "invalid request"
        })

    token = token_tool().dumps(user["key"])
    mail = request.json['mail_content'].format(token=token)
    send_mail(user["email"], "Welcome!", mail)

    return jsonify({
        "status": 200,
    })


@bp.post("/password/<token>")
def password_(token):
    db = database

    try:
        token = token_tool().loads(
            token, max_age=current_app.config["EMAIL_CONFIRM_EXP"])
    except Exception:
        return jsonify({
            "status": 401,
            "error": "invalid token"
        })

    user = token_to_user(db)
    token_user = query({"type": "user", "key": token}, db=db)
    if not token_user or not user or token_user["key"] != user["key"]:
        return jsonify({
            "status": 401,
            "error": "invalid token"
        })

    error = {}
    if "password" not in request.json or not request.json["password"]:
        error["password"] = "This field is required"
    elif (
        not re.search("[a-z]", request.json["password"])
        or not re.search("[A-Z]", request.json["password"])
        or not re.search("[0-9]", request.json["password"])
        or len(request.json["password"]) not in range(8, 19)
    ):
        error["password"] = """Password must include at least 1 lowercase
        letter, 1 uppercase letter, 1 number and must contain 8 - 18
        characters"""
    elif check_password_hash(user["password"], request.json["password"]):
        error["password"
              ] = "New password should be different from old password"

    if "confirm" not in request.json or not request.json["confirm"]:
        error["confirm"] = "This field is required"
    elif (
            request.json["password"]
            and "password" not in error
            and request.json["confirm"] != request.json["password"]
    ):
        error["confirm"] = 'Password and confirm password does not match'

    if error != {}:
        return jsonify({
            "status": 401,
            **error
        })

    user["password"] = generate_password_hash(
        request.json["password"], method="sha256")  # scrypt
    database(user)

    return jsonify({
        "status": 200,
    })


@ bp.delete("/user")
def delete():
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 401,
            "error": "invalid token"
        })

    if not request.json["password"]:
        return jsonify({
            "status": 401,
            "error": "this field is required"
        })

    if not check_password_hash(user["password"], request.json["password"]):
        return jsonify({
            "status": 401,
            "error": "incorrect password"
        })

    user["key"] = "deleted"
    user = database(user)

    return jsonify({
        "status": 200,
        "user": user_schema(user, db)
    })
