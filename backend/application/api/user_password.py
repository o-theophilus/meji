from flask import Blueprint, jsonify, request, current_app
from .tools import token_tool, token_to_user
from .mail import send_mail
from werkzeug.security import check_password_hash, generate_password_hash
import re
from .database import database
from .schema import user_schema

bp = Blueprint("user_password", __name__)


@bp.post("/password_forgot")
def password_forgot():
    data = database

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
        error = "This field is required"
    elif not re.match(r"\S+@\S+\.\S+", request.json["email"]):
        error = "Please enter a valid email"
    if error:
        return jsonify({
            "status": 201,
            "message": error
        })

    user = query("user", "email", request.json["email"], data)
    if not user:
        return jsonify({
            "status": 201,
            "message": "There is no user registered with this email"
        })

    token = token_tool().dumps(user["key"])
    mail = request.json['mail_content'].format(
        token=token,
        name=user["name"]
    )
    send_mail(user["email"], "Welcome!", mail)

    return jsonify({
        "status": 200,
        "message": "password change email sent",
    })


@bp.post("/password_forgot/<token>")
def password_forgot_(token):
    data = database

    try:
        token = token_tool().loads(
            token, max_age=current_app.config["EMAIL_CONFIRM_EXP"])
    except Exception:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    user = query("user", "key", token, data)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
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
            "status": 201,
            "message": error
        })

    user["password"] = generate_password_hash(
        request.json["password"], method="sha256")
    database(user)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "user": user_schema(user, data)
        }
    })


@bp.post("/password")
def password():
    data = database

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

    token = token_tool().dumps(user["key"])
    mail = request.json['mail_content'].format(token=token)
    send_mail(user["email"], "Welcome!", mail)

    return jsonify({
        "status": 200,
        "message": "password change email sent",
    })


@bp.post("/password/<token>")
def password_(token):
    data = database

    try:
        token = token_tool().loads(
            token, max_age=current_app.config["EMAIL_CONFIRM_EXP"])
    except Exception:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    user = token_to_user(data)
    token_user = query("user", "key", token, data)
    if not token_user or not user or token_user["key"] != user["key"]:
        return jsonify({
            "status": 101,
            "message": "invalid token"
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
            "status": 201,
            "message": error
        })

    user["password"] = generate_password_hash(
        request.json["password"], method="sha256")
    database(user)

    return jsonify({
        "status": 200,
        "message": "successful",
    })
