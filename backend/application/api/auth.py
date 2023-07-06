from flask import Blueprint, jsonify, request, current_app
from .tools import (
    token_tool, token_to_user, now)
from .mail import send_mail
from .schema import user_schema, user_template
from werkzeug.security import generate_password_hash, check_password_hash
from .database import database, query
import re
from uuid import uuid4


bp = Blueprint("auth", __name__)


@bp.post("/init")
def init():
    db = database()

    token = request.headers["Authorization"]
    user = token_to_user(db)

    if not user:
        temp = uuid4().hex
        user = database(user_template(temp, temp, temp))
        token = token_tool().dumps(user["key"])

    return jsonify({
        "status": 200,
        "user": user_schema(user, db),
        "token": token
    })


@bp.post("/user")
def signup():
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 401,
            "error": "invalid token"
        })

    if (
        user["login"]
        or user["status"] != "anon"
        or "mail_content" not in request.json
        or not request.json["mail_content"]
    ):
        return jsonify({
            "status": 401,
            "error": "invalid request"
        })

    error = {}

    if "name" not in request.json or not request.json["name"]:
        error["name"] = "this field is required"

    if "email" not in request.json or not request.json["email"]:
        error["email"] = "this field is required"
    elif not re.match(r"\S+@\S+\.\S+", request.json["email"]):
        error["email"] = "Please enter a valid email"
    elif query({"type": "user", "email": request.json["email"]}, db=db):
        error["email"] = "email taken"

    if "password" not in request.json or not request.json["password"]:
        error["password"] = "this field is required"
    elif (
        not re.search("[a-z]", request.json["password"])
        or not re.search("[A-Z]", request.json["password"])
        or not re.search("[0-9]", request.json["password"])
        or len(request.json["password"]) not in range(8, 19)
    ):
        error["password"] = """password must include at least 1 lowercase
        letter, 1 uppercase letter, 1 number and must contain 8 - 18
        characters"""

    if "confirm" not in request.json or not request.json["confirm"]:
        error["confirm"] = "This field is required"
    elif (
            request.json["password"]
            and "password" not in error
            and request.json["confirm"] != request.json["password"]
    ):
        error["confirm"] = 'password and confirm password does not match'

    if error != {}:
        return jsonify({
            "status": 401,
            **error
        })

    user["name"] = request.json["name"]
    user["email"] = request.json["email"]
    user["password"] = generate_password_hash(
        request.json["password"], method="sha256")  # scrypt
    user["status"] = "not_confirm"
    user["date_u"] = now(),

    user = database(user)

    send_mail(
        user["email"],
        "Welcome!",
        request.json['mail_content'].format(
            token=token_tool().dumps(
                user["key"]
            )
        )
    )

    return jsonify({
        "status": 200,
        "user": user_schema(user, db)
    })


@bp.post("/login")
def login():
    db = database()

    anon_user = token_to_user(db)
    if not anon_user:
        return jsonify({
            "status": 401,
            "error": "invalid token"
        })

    if (
        anon_user["status"] != "anon"
        or "mail_content" not in request.json
        or not request.json["mail_content"]
    ):
        return jsonify({
            "status": 401,
            "error": "invalid request"
        })

    error = {}
    if "email" not in request.json or not request.json["email"]:
        error["email"] = "This field is required"
    if "password" not in request.json or not request.json["password"]:
        error["password"] = "This field is required"

    if error != {}:
        return jsonify({
            "status": 401,
            **error
        })

    user = query("user", "email", request.json["email"], db)

    if (
        not user
        or not check_password_hash(user["password"], request.json["password"])
    ):
        return jsonify({
            "status": 401,
            "error": "your email or password is incorrect"
        })

    if user["status"] != "confirm":
        send_mail(
            user["email"],
            "Welcome!",
            request.json['mail_content'].format(
                name=user["name"],
                token=token_tool().dumps(
                    user["key"]
                )
            ))

        return jsonify({
            "status": 401,
            "user": user_schema(user, db)
        })

    def copy(y):
        keys = [x["key"] for x in user[y]]
        for x in anon_user[y]:
            if x["key"] not in keys:
                user[y].append(x)
    copy("cart")
    copy("saves")

    user["login"] = True
    user = database(user)
    database(anon_user, True)

    return jsonify({
        "status": 200,
        "user": user_schema(user, db),
        "token": token_tool().dumps(user["key"])
    })


@bp.delete("/logout")
def logout():
    db = database()

    user = token_to_user(db)
    if user:
        user["login"] = False
        database(user)

    temp = uuid4().hex
    user = database(user_template(temp, temp, temp))

    return jsonify({
        "status": 200,
        "user": user_schema(user, db),
        "token": token_tool().dumps(user["key"])
    })


@bp.post("/forgot_password")
def forgot_password():
    db = database()

    if (
       "mail_content" not in request.json
        or not request.json["mail_content"]
       ):
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    error = None
    if "email" not in request.json or not request.json["email"]:
        error = "this field is required"
    elif not re.match(r"\S+@\S+\.\S+", request.json["email"]):
        error = "please enter a valid email"
    if error:
        return jsonify({
            "status": 401,
            "error": error
        })

    user = query("user", "email", request.json["email"], db)
    if not user:
        return jsonify({
            "status": 401,
            "error": "there is no user registered with this email"
        })

    send_mail(
        user["email"],
        "Welcome!",
        request.json['mail_content'].format(
            token=token_tool().dumps(
                user["key"]
            ),
            name=user["name"]
        ))

    return jsonify({
        "status": 200
    })


@bp.post("/forgot_password/<token>")
def change_password(token):
    db = database()

    try:
        token = token_tool().loads(
            token, max_age=current_app.config["EMAIL_CONFIRM_EXP"])
    except Exception:
        return jsonify({
            "status": 401,
            "error": "invalid token"
        })

    user = query({"type": "user", "key": token}, db=db)
    if not user:
        return jsonify({
            "status": 401,
            "error": "invalid token"
        })

    error = {}
    if "password" not in request.json or not request.json["password"]:
        error["password"] = "this field is required"
    elif (
        not re.search("[a-z]", request.json["password"])
        or not re.search("[A-Z]", request.json["password"])
        or not re.search("[0-9]", request.json["password"])
        or len(request.json["password"]) not in range(8, 19)
    ):
        error["password"] = """password must include at least 1 lowercase
        letter, 1 uppercase letter, 1 number and must contain 8 - 18
        characters"""
    elif check_password_hash(user["password"], request.json["password"]):
        error["password"
              ] = "new password should be different from old password"

    if "confirm" not in request.json or not request.json["confirm"]:
        error["confirm"] = "this field is required"
    elif (
            request.json["password"]
            and "password" not in error
            and request.json["confirm"] != request.json["password"]
    ):
        error["confirm"] = 'password and confirm password does not match'

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
        "user": user_schema(user, db)
    })


def omni():
    db = database()
    email = current_app.config["MAIL_DEFAULT_SENDER"][1]

    user = query({"type": "user", "email": email}, db=db)
    if not user:
        password = generate_password_hash(
            "1234",
            method="sha256"
        )
        # user["roles"] = ["admin", "dashboard", "omni"]
        database(user_template(
            "Meji Admin", email, password
        ))
