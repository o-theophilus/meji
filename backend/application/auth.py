from flask import Blueprint, jsonify, request, current_app
from .tools import token_tool, token_to_user, now, send_mail
from .schema import user_schema
from werkzeug.security import generate_password_hash, check_password_hash
from .database import database, query
import re
from uuid import uuid4
import os


bp = Blueprint("auth", __name__)


def user_template(
        name,
        email,
        password
):
    return {
        "key": uuid4().hex,
        "v": uuid4().hex,
        "type": "user",
        "date_c": now(),
        "date_u": now(),
        "status": "anonymous",

        "name": name,
        "email": email,
        "phone": None,
        "password": generate_password_hash(
            password,
            method="scrypt"
        ),
        "address": {
            "line": None,
            "country": None,
            "state": None,
            "local_area": None,
            "postal_code": None,
        },
        "photo": None,
        "acc_balance": 0,
        "saves": [],
        "cart": [],
        "roles": [],  # admin, supplier,
        "login": False,
        "setting": {
            "item_view": "grid",
            "theme": "light"
        },
    }


@bp.post("/init")
def init():
    db = database()

    token = request.headers["Authorization"]
    user = token_to_user(db)

    if not user:
        temp = uuid4().hex
        user = database(user_template("anonymous", temp, temp))
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
            "status": 400,
            "error": "invalid token"
        })

    if (
        user["login"]
        or user["status"] != "anonymous"
        or "email_template" not in request.json
        or not request.json["email_template"]
    ):
        return jsonify({
            "status": 400,
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

    if "confirm_password" not in request.json or not request.json[
            "confirm_password"]:
        error["confirm_password"] = "This field is required"
    elif (
            request.json["password"]
            and "password" not in error
            and request.json["confirm_password"] != request.json["password"]
    ):
        error["confirm_password"] = """password and confirm password does not
        match"""

    if error != {}:
        return jsonify({
            "status": 400,
            **error
        })

    user["name"] = request.json["name"]
    user["email"] = request.json["email"]
    user["password"] = generate_password_hash(
        request.json["password"], method="scrypt")
    user["date_u"] = now(),

    user = database(user)

    send_mail(
        user["email"],
        "Welcome to Meji! Please Confirm Your Email to Get Started",
        request.json['email_template'].format(
            name=user["name"],
            token=token_tool().dumps(
                user["key"]
            )
        )
    )

    return jsonify({
        "status": 200,
        # "user": user_schema(user, db)
    })


@bp.get("/confirm/<token>")
def confirm_email(token):
    db = database()

    try:
        token = token_tool().loads(
            token, max_age=current_app.config["EMAIL_CONFIRM_EXP"])
    except Exception:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    user = query({"type": "user", "key": token}, db=db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    output = {
        "status": 200,
        "user": user_schema(user, db)
    }

    if user["status"] == "confirm":
        output['error'] = "email has already been confirmed"
    else:
        user["status"] = "confirm"
        user = database(user)

    return jsonify(output)


@bp.post("/login")
def login():
    db = database()

    anon_user = token_to_user(db)
    if not anon_user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if (
        anon_user["login"]
        or "email_template" not in request.json
        or not request.json["email_template"]
    ):
        print(anon_user["status"])
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = {}
    if "email" not in request.json or not request.json["email"]:
        error["email"] = "This field is required"
    if "password" not in request.json or not request.json["password"]:
        error["password"] = "This field is required"

    if error != {}:
        return jsonify({
            "status": 400,
            **error
        })

    user = query({'type': "user", "email": request.json["email"]}, db=db)

    if (
        not user
        or not check_password_hash(user["password"], request.json["password"])
    ):
        return jsonify({
            "status": 400,
            "error": "your email or password is incorrect"
        })

    if user["status"] != "confirm":
        send_mail(
            user["email"],
            "Welcome to Meji! Please Confirm Your Email to Get Started",
            request.json['email_template'].format(
                name=user["name"],
                token=token_tool().dumps(
                    user["key"]
                )
            ))

        return jsonify({
            "status": 400,
            "error": "not confirmed"
        })

    if anon_user['key'] != user['key']:
        def copy(y):
            keys = [x["key"] for x in user[y]]
            for x in anon_user[y]:
                if x["key"] not in keys:
                    user[y].append(x)
        copy("cart")
        copy("saves")
        database(anon_user, True)

    user["login"] = True
    user = database(user)

    return jsonify({
        "status": 200,
        "token": token_tool().dumps(user["key"])
    })


@bp.delete("/logout")
def logout():
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    user["login"] = False
    temp = uuid4().hex
    anon_user = user_template("anonymous", temp, temp)
    anon_user["setting"]["theme"] = user["setting"]["theme"]
    database([user, anon_user])

    return jsonify({
        "status": 200,
        "user": user_schema(anon_user, db),
        "token": token_tool().dumps(anon_user["key"])
    })


@bp.post("/forgot_password")
def forgot_password():
    db = database()

    if (
       "email_template" not in request.json
        or not request.json["email_template"]
       ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = None
    if "email" not in request.json or not request.json["email"]:
        error = "this field is required"
    elif not re.match(r"\S+@\S+\.\S+", request.json["email"]):
        error = "please enter a valid email"
    if error:
        return jsonify({
            "status": 400,
            "error": error
        })

    user = query({"type": "user", "email": request.json["email"]}, db=db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "there is no user registered with this email"
        })

    send_mail(
        user["email"],
        "Welcome!",
        request.json['email_template'].format(
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
            "status": 400,
            "error": "invalid token"
        })

    user = query({"type": "user", "key": token}, db=db)
    if not user:
        return jsonify({
            "status": 400,
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

    if "confirm_password" not in request.json or not request.json[
            "confirm_password"]:
        error["confirm_password"] = "this field is required"
    elif (
            request.json["password"]
            and "password" not in error
            and request.json["confirm_password"] != request.json["password"]
    ):
        error["confirm_password"] = """password and confirm password does not
         match"""

    if error != {}:
        return jsonify({
            "status": 400,
            **error
        })

    user["password"] = generate_password_hash(
        request.json["password"], method="scrypt")
    database(user)

    return jsonify({
        "status": 200,
        "user": user_schema(user, db)
    })


@bp.get("/admin_init")
def admin():
    db = database()
    email = os.environ["MAIL_USERNAME"]

    user = query({"type": "user", "email": email}, db=db)
    if not user:
        user = user_template(
            "Meji Admin",
            email,
            os.environ["MAIL_PASSWORD"]
        )
        user["status"] = "confirm"
        user["roles"] = ["admin", "dashboard", "omni"]
        database(user)

    return jsonify({
        "status": 200
    })
