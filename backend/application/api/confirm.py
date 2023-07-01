from flask import Blueprint, jsonify,  current_app
from .tools import token_tool
from .schema import user_schema
from .database import database


bp = Blueprint("user_confirm", __name__)


@bp.get("/confirm/<token>")
def confirm(token):
    data = database()

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

    if user["status"] == "confirm":
        return jsonify({
            "status": 201,
            "message": "user already confirmed",
            "data": {
                "user": user_schema(user, data)
            }
        })

    user["status"] = "confirm"
    user = database(user)

    return jsonify({
        "status": 200,
        "message": "user confirmed",
        "data": {
            "user": user_schema(user, data)
        }
    })
