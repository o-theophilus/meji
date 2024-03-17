from flask import Blueprint, jsonify, request
from .tools import token_tool, token_to_user, send_mail, user_schema
from werkzeug.security import generate_password_hash, check_password_hash
from .log import log_template
# from .user_cart import cart_template, transaction
import re
from uuid import uuid4
import os
from datetime import datetime
from .postgres import db_close, db_open
import json


bp = Blueprint("auth", __name__)

max_age = 3600


@bp.post("/init")
def init():
    con, cur = db_open()

    token = request.headers["Authorization"]
    user = token_to_user(cur)

    if not user or user["status"] == "confirmed" and not user["login"]:

        cur.execute("""
                INSERT INTO "user" (key, version, email, password)
                VALUES (%s, %s, %s, %s)
                RETURNING *;
            """, (
            uuid4().hex,
            uuid4().hex,
            uuid4().hex,
            generate_password_hash(uuid4().hex, method="scrypt"))
        )
        user = cur.fetchone()

        cur.execute(log_template, (
            uuid4().hex,
            datetime.now(),
            user["key"],
            "created",
            user["key"],
            "auth",
            200,
            None
        ))

        token = token_tool().dumps(user["key"])

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "user": user_schema(user),
        "token": token
    })


@bp.post("/signup")
def signup():
    con, cur = db_open()

    user = token_to_user(cur)
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

    cur.execute('SELECT * FROM "user" WHERE email = %s;', (
        request.json["email"],
    ))
    email_exist = cur.fetchone()

    if "name" not in request.json or not request.json["name"]:
        error["name"] = "this field is required"

    if "email" not in request.json or not request.json["email"]:
        error["email"] = "this field is required"
    elif not re.match(r"\S+@\S+\.\S+", request.json["email"]):
        error["email"] = "Please enter a valid email"
    elif email_exist:
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
        cur.execute("""
            INSERT INTO "user" (key, version, email, password)
            VALUES (%s, %s, %s, %s)
            RETURNING *;
        """, (
            uuid4().hex, uuid4().hex, uuid4().hex,
            generate_password_hash(uuid4().hex, method="scrypt")))
        user = cur.fetchone()

    cur.execute("""
        UPDATE "user"
        SET name = %s, email = %s, password = %s, status = %s
        WHERE key = %s
        RETURNING *;""", (
        request.json["name"],
        request.json["email"],
        generate_password_hash(request.json["password"], method="scrypt"),
        "signed_up",
        user["key"]
    ))
    user = cur.fetchone()

    cur.execute(log_template, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "signed_up",
        user["key"],
        "auth", 200, None
    ))

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

    db_close(con, cur)

    return jsonify({
        "status": 200
    })


@bp.get("/confirm/<token>")
def confirm_email(token):
    con, cur = db_open()

    try:
        token = token_tool().loads(token, max_age=max_age)
    except Exception:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    cur.execute('SELECT * FROM "user" WHERE key = %s;', (token,))
    user = cur.fetchone()
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    output = {
        "status": 200,
        "user": user_schema(user)
    }

    if user["status"] != "confirmed":
        cur.execute("""
            UPDATE "user" SET status = %s
            WHERE key = %s RETURNING *;""", (
            "confirmed",
            user["key"]
        ))
        user = cur.fetchone()
        output['user'] = user_schema(user)

        cur.execute(log_template, (
            uuid4().hex,
            datetime.now(),
            user["key"],
            "confirmed_email",
            user["key"],
            "auth",
            200,
            None
        ))

    else:
        output['error'] = "email has already been confirmed"

        cur.execute(log_template, (
            uuid4().hex,
            datetime.now(),
            user["key"],
            "confirmed_email",
            user["key"],
            "auth",
            201,
            json.dumps({"error": "already confirmed"})
        ))

    db_close(con, cur)

    return jsonify(output)


@bp.post("/login")
def login():
    con, cur = db_open()

    out_user = token_to_user(cur)
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
        cur.execute('SELECT * FROM "user" WHERE email = %s;',
                    (request.json["email"],))
        user = cur.fetchone()

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

    # edited = []
    # to_delete = []

    # if out_user['key'] != user['key']:
    #     anon_saves = []
    #     saves = []
    #     anon_cart = None
    #     cart = None

    #     for x in db:
    #         if x["type"] == "save" and x["user"] == out_user['key']:
    #             anon_saves.append(x)
    #         elif x["type"] == "save" and x["user"] == user['key']:
    #             saves.append(x)
    #         elif x["type"] == "cart" and x["user"] == out_user['key']:
    #             anon_cart = x
    #         elif x["type"] == "cart" and x["user"] == user['key']:
    #             cart = x

    #     keys = [x["item"] for x in saves]
    #     for x in anon_saves:
    #         if x["item"] in keys:
    #             to_delete.append(x)
    #         else:
    #             x["user"] = user['key']
    #             edited.append(x)

    #     if anon_cart:
    #         if not cart:
    #             cart = cart_template(user)

    #         keys = [f"{x['key']}_{x['variation']}" for x in cart["items"]]
    #         for x in anon_cart["items"]:
    #             if f"{x['key']}_{x['variation']}" not in keys:
    #                 cart["items"].append(x)

    #         for x in cart["items"]:
    #             for y in anon_cart["items"]:
    #                 x_key = f"{x['key']}_{x['variation']}"
    #                 y_key = f"{y['key']}_{y['variation']}"
    #                 if x_key == y_key:
    #                     x["quantity"] = y["quantity"]
    #                     break

    #         cart = transaction(cart, db)

    #         to_delete.append(anon_cart)
    #         edited.append(cart)

    # database([*edited, user])
    # if out_user["status"] == "anonymous":
    # to_delete.append(out_user)
    # database(to_delete, True)

    cur.execute("""
        UPDATE "user" SET login = %s
        WHERE key = %s RETURNING *;""", (
        True, user["key"]
    ))

    cur.execute(log_template, (
        uuid4().hex, datetime.now(),
        user["key"],
        "logged_in",
        user["key"],
        "auth",
        200,
        json.dumps({
            "from": out_user["key"],
            "name": out_user["name"]
        })
    ))
    cur.execute(log_template, (
        uuid4().hex,
        datetime.now(),
        out_user["key"],
        "logged_out",
        out_user["key"],
        "auth", 200,
        json.dumps({
            "to": user["key"],
            "name": user["name"]
        })
    ))

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "token": token_tool().dumps(user["key"])
    })


@bp.delete("/logout")
def logout():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    cur.execute("""
        UPDATE "user" SET login = %s
        WHERE key = %s RETURNING *;""", (
        False, user["key"]
    ))

    cur.execute("""
        INSERT INTO "user" (
            key, version, email, password, setting_theme
        ) VALUES (%s, %s, %s, %s, %s) RETURNING *;
    """, (
        uuid4().hex, uuid4().hex, uuid4().hex,
        generate_password_hash(uuid4().hex, method="scrypt"),
        user["setting_theme"]
    ))
    anon_user = cur.fetchone()

    cur.execute(log_template, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "logged_out",
        user["key"],
        "auth",
        200,
        json.dumps({
            "to": anon_user["key"],
            "name": anon_user["name"]
        })
    ))

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "user": user_schema(anon_user),
        "token": token_tool().dumps(anon_user["key"])
    })


@bp.post("/forgot_password")
def forgot_password():
    con, cur = db_open()

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

    cur.execute('SELECT * FROM "user" WHERE email = %s;',
                (request.json["email"],))
    user = cur.fetchone()
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

    cur.execute(log_template, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "forgot_password",
        user["key"],
        "auth",
        201,
        None
    ))

    db_close(con, cur)

    return jsonify({
        "status": 200
    })


@bp.post("/forgot_password/<token>")
def change_password(token):
    con, cur = db_open()

    try:
        token = token_tool().loads(token, max_age=max_age)
    except Exception:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    cur.execute('SELECT * FROM "user" WHERE key = %s;', (token,))
    user = cur.fetchone()
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

    cur.execute("""
        UPDATE "user" SET password = %s
        WHERE key = %s RETURNING *;""", (
        generate_password_hash(
            request.json["password"], method="scrypt"),
        user["key"]
    ))

    cur.execute(log_template, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "changed_password",
        user["key"],
        "auth",
        200,
        None
    ))

    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })


@bp.get("/admin_init")
def admin():
    con, cur = db_open()
    email = os.environ["MAIL_USERNAME"]

    cur.execute('SELECT * FROM "user" WHERE email = %s;', (email,))
    user = cur.fetchone()
    if not user:
        cur.execute("""
                INSERT INTO "user" ( key, version, status, name, email,
                    password, roles)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """, (
            uuid4().hex, uuid4().hex,
            "confirmed", "Meji Admin", email, generate_password_hash(
                os.environ["MAIL_PASSWORD"], method="scrypt"),
            [
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
        ))

    db_close(con, cur)

    return jsonify({
        "status": 200
    })
