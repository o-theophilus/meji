from flask import Blueprint, jsonify, request
from .tools import token_tool, token_to_user, now, send_mail
from .schema import user_schema
from werkzeug.security import generate_password_hash, check_password_hash
from .database import database, query
from .log import log_template
from .user_cart import cart_template, transaction
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
        "status": "anonymous",  # signedup, confirmed

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
        "roles": [],
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

    if user["status"] != "anonymous":
        user = user_template("anon", "anon", "anon")

    user["name"] = request.json["name"]
    user["email"] = request.json["email"]
    user["password"] = generate_password_hash(
        request.json["password"], method="scrypt")
    user["date_u"] = now()
    user["status"] = "signedup"

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
        "status": 200
    })


max_age = 3600


@bp.get("/confirm/<token>")
def confirm_email(token):
    db = database()

    try:
        token = token_tool().loads(token, max_age=max_age)
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

    if user["status"] == "confirmed":
        output['error'] = "email has already been confirmed"
    else:
        user["status"] = "confirmed"
        user = database(user)

    return jsonify(output)


@bp.post("/login")
def login():
    db = database()

    out_user = token_to_user(db)
    if not out_user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if (
        out_user["login"]
        or "email_template" not in request.json
        or not request.json["email_template"]
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = {}
    if "email" not in request.json or not request.json["email"]:
        error["email"] = "this field is required"
    if "password" not in request.json or not request.json["password"]:
        error["password"] = "this field is required"

    if error != {}:
        return jsonify({
            "status": 400,
            **error
        })

    user = None
    if out_user["email"] == request.json["email"]:
        user = out_user
    else:
        user = query({'type': "user", "email": request.json["email"]}, db=db)

    if (
        not user
        or not check_password_hash(user["password"], request.json["password"])
        or user["status"] == "anonymous"
    ):
        return jsonify({
            "status": 400,
            "error": "your email or password is incorrect"
        })

    if user["status"] != "confirmed":
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

    edited = []
    to_delete = []

    if out_user['key'] != user['key']:
        anon_saves = []
        saves = []
        anon_cart = None
        cart = None

        for x in db:
            if x["type"] == "save" and x["user"] == out_user['key']:
                anon_saves.append(x)
            elif x["type"] == "save" and x["user"] == user['key']:
                saves.append(x)
            elif x["type"] == "cart" and x["user"] == out_user['key']:
                anon_cart = x
            elif x["type"] == "cart" and x["user"] == user['key']:
                cart = x

        keys = [x["item"] for x in saves]
        for x in anon_saves:
            if x["item"] in keys:
                to_delete.append(x)
            else:
                x["user"] = user['key']
                edited.append(x)

        if anon_cart:
            if not cart:
                cart = cart_template(user)

            keys = [f"{x['key']}_{x['variation']}" for x in cart["items"]]
            for x in anon_cart["items"]:
                if f"{x['key']}_{x['variation']}" not in keys:
                    cart["items"].append(x)

            for x in cart["items"]:
                for y in anon_cart["items"]:
                    x_key = f"{x['key']}_{x['variation']}"
                    y_key = f"{y['key']}_{y['variation']}"
                    if x_key == y_key:
                        x["quantity"] = y["quantity"]
                        break

            cart = transaction(cart, db)

            to_delete.append(anon_cart)
            edited.append(cart)

    user["login"] = True
    database([*edited, user])
    if out_user["status"] == "anonymous":
        to_delete.append(out_user)
    database(to_delete, True)

    database(log_template(
        user["key"],
        "logged_in",
        None,
        "auth"
    ), db_name="log")

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
        token = token_tool().loads(token, max_age=max_age)
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
        user["status"] = "confirmed"
        user["roles"] = [
            "admin:manage_photo",
            "user:view",
            "user:view_balance",
            "user:set_role",
            "item:add",
            "item:edit_photo",
            "item:advert",
            "item:edit_status",
            "item:edit_name",
            "item:edit_tag",
            "item:edit_price",
            "item:edit_info",
            "item:edit_variation",
            "voucher:view",
            "voucher:add",
            "voucher:view_code",
            "voucher:status",
            "log:view",
            "order:view",
            "order:edit_eta",
            "order:status",
            "order:cancel"
        ]
        database(user)

    return jsonify({
        "status": 200
    })
