from flask import Blueprint, jsonify, request, current_app
from .tools import (
    token_tool, token_to_user, now)
from .mail import send_mail
from .schema import user_schema, user_template
from werkzeug.security import generate_password_hash, check_password_hash
from .database import database
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
    data = database()

    user = token_to_user(data)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    if (
        "mail_content" not in request.json
        or not request.json["mail_content"]
    ):
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    if user["login"]:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    error = {}

    if "name" not in request.json or not request.json["name"]:
        error["name"] = "this field is required"

    if "email" not in request.json or not request.json["email"]:
        error["email"] = "this field is required"
    elif not re.match(r"\S+@\S+\.\S+", request.json["email"]):
        error["email"] = "Please enter a valid email"

    elif query("user", "email", request.json["email"], data):
        error["email"] = "email taken"

    if "password" not in request.json or not request.json["password"]:
        error["password"] = "this field is required"
    elif (
        not re.search("[a-z]", request.json["password"]) or
        not re.search("[A-Z]", request.json["password"]) or
        not re.search("[0-9]", request.json["password"]) or
        len(request.json["password"]) not in range(8, 19)
    ):
        error["password"] = """Password must include at least 1 lowercase
        letter, 1 uppercase letter, 1 number and must contain 8 - 18
        characters"""

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
            "status": 201,
            "message": error
        })

    if user["status"] != "anon":
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })
        # user = default_user
        # user["key"] = uuid4().hex

    user["name"] = request.json["name"]
    user["email"] = request.json["email"]
    user["password"] = generate_password_hash(
        request.json["password"], method="sha256")
    user["status"] = "not_confirm"
    user["date_u"] = now(),
    user["v"]: uuid4().hex

    user = database(user)
    token = token_tool().dumps(user["key"])
    mail = request.json['mail_content'].format(token=token)
    send_mail(user["email"], "Welcome!", mail)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "user": user_schema(user, data)
        }
    })


@bp.post("/login")
def login():
    data = database()

    anon_user = token_to_user(data)
    if not anon_user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    message = {}
    if "email" not in request.json or not request.json["email"]:
        message["email"] = "This field is required"
    if "password" not in request.json or not request.json["password"]:
        message["password"] = "This field is required"

    if message != {}:
        return jsonify({
            "status": 201,
            "message": message
        })

    user = query("user", "email", request.json["email"], data)

    if (
        user
        and check_password_hash(user["password"], request.json["password"])
    ):

        if user["status"] != "confirm":
            if (
                "mail_content" not in request.json
                or not request.json["mail_content"]
            ):
                return jsonify({
                    "status": 401,
                    "message": "invalid request"
                })

            token = token_tool().dumps(user["key"])
            mail = request.json['mail_content'].format(
                name=user["name"],
                token=token
            )
            send_mail(user["email"], "Welcome!", mail)

            return jsonify({
                "status": 201,
                "message": "not confirmed",
                "data": {
                    "user": user_schema(user, data)
                }
            })

        user_cart = [cart["key"] for cart in user["cart"]]
        user_saves = [save["key"] for save in user["saves"]]

        if anon_user["status"] == "anon":
            for cart in anon_user["cart"]:
                if cart["key"] not in user_cart:
                    user["cart"].append(cart)

            for save in anon_user["saves"]:
                if save["key"] not in user_saves:
                    user["saves"].append(save)

            db.delete(anon_user["key"])

        user["login"] = True
        user = database(user)

        return jsonify({
            "status": 200,
            "message": "successful",
            "data": {
                "user": user_schema(user, data),
                "token": token_tool().dumps(user["key"])
            }
        })

    return jsonify({
        "status": 201,
        "message": "Your email or password is incorrect"
    })


@bp.delete("/logout")
def logout():
    data = database()

    user = token_to_user(data)
    if user:
        user["login"] = False

    temp = uuid4().hex
    user = database(user_template(temp, temp, temp))

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "user": user_schema(user, data),
            "token": token_tool().dumps(user["key"])
        }
    })


def omni():
    data = database()
    email = current_app.config["MAIL_DEFAULT_SENDER"][1]

    user = query("user", "email", email, data)
    if not user:
        password = generate_password_hash(
            "1234",
            method="sha256"
        )
        # user["roles"] = ["admin", "dashboard", "omni"]
        database(user_template(
            "Meji Admin", email, password
        ))
