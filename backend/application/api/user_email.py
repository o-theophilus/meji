from flask import Blueprint, jsonify, request, current_app
from .tools import token_tool, token_to_user
from .mail import send_mail
import re
from .database import database
from .schema import user_schema

bp = Blueprint("user_email", __name__)


@bp.post("/email")
def email():
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

    token = token_tool().dumps(user["key"])
    mail = request.json['mail_content'].format(token=token)
    send_mail(user["email"], "Welcome!", mail)

    return jsonify({
        "status": 200,
        "message": "email change email sent",
    })


@bp.post("/email/<token>")
def email_(token):
    data = database()

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

    error = None
    if "email" not in request.json or not request.json["email"]:
        error = "This field is required"
    elif not re.match(r"\S+@\S+\.\S+", request.json["email"]):
        error = "Please enter a valid email"
    elif user["email"] == request.json["email"]:
        error = "please use a different email form your current email"
    elif query("user", "email", request.json["email"], data):
        error = "email is already in use"
    if error:
        return jsonify({
            "status": 201,
            "message": error
        })

    user["email"] = request.json["email"]
    user = database(user)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "user": user_schema(user, data)
        }
    })
