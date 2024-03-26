from flask import Blueprint, jsonify, request
from .tools import token_tool, token_to_user, send_mail, user_schema
from werkzeug.security import generate_password_hash, check_password_hash
# from .user_cart import cart_template, transaction
import re
from uuid import uuid4
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
        key = uuid4().hex
        cur.execute("""
                INSERT INTO "user" (key, version, name, email, password)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING *;
            """, (
            key,
            uuid4().hex,
            f"user_{key[-4:]}",
            uuid4().hex,
            generate_password_hash(uuid4().hex, method="scrypt"))
        )
        user = cur.fetchone()

        cur.execute("""
            INSERT INTO log (
                key, date, user_key, action, entity_key, entity_type
            ) VALUES (%s, %s, %s, %s, %s, %s);
        """, (
            uuid4().hex,
            datetime.now(),
            user["key"],
            "created",
            None,
            "auth"
        ))

        token = token_tool().dumps(user["key"])

    cur.execute("""
        SELECT
            CASE
                WHEN COUNT(save.*) = 0 THEN ARRAY[]::character[]
                ELSE ARRAY_AGG(save.item_key)
            END AS saves
        FROM save
        WHERE save.user_key = %s;
    """, (user["key"],))
    saves = cur.fetchone()

    cur.execute("""
        SELECT order_item.key, order_item.variation
        FROM order_item
        LEFT JOIN "order" ON order_item.order_key = "order".key
        WHERE "order".user_key = %s AND status = 'cart';
    """, (user["key"],))
    cart = cur.fetchall()
    cart = [f"{x['key']}_{json.dumps(x['variation'])}" for x in cart]

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "user": user_schema(user, saves["saves"], cart),
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

    if "name" not in request.json or not request.json["name"]:
        error["name"] = "this field is required"

    if "email" not in request.json or not request.json["email"]:
        error["email"] = "this field is required"
    elif not re.match(r"\S+@\S+\.\S+", request.json["email"]):
        error["email"] = "Please enter a valid email"
    else:
        cur.execute('SELECT * FROM "user" WHERE email = %s;', (
            request.json["email"],))
        if cur.fetchone():
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

    cur.execute("""
        INSERT INTO log (
            key, date, user_key, action, entity_key, entity_type
        ) VALUES (%s, %s, %s, %s, %s, %s);
    """, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "signed_up",
        None,
        "auth"
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

        cur.execute("""
            INSERT INTO log (
                key, date, user_key, action, entity_key, entity_type
            ) VALUES (%s, %s, %s, %s, %s, %s);
        """, (
            uuid4().hex,
            datetime.now(),
            user["key"],
            "confirmed_email",
            None,
            "auth"
        ))

    else:
        output['error'] = "email has already been confirmed"

        cur.execute("""
            INSERT INTO log (
                    key, date, user_key, action, entity_key,
                    entity_type, status, misc
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """, (
            uuid4().hex,
            datetime.now(),
            user["key"],
            "confirmed_email",
            None,
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

    in_user = None
    if out_user["email"] == request.json["email"]:
        in_user = out_user
    else:
        cur.execute('SELECT * FROM "user" WHERE email = %s;',
                    (request.json["email"],))
        in_user = cur.fetchone()

    if (
        not in_user
        or in_user["status"] == "anonymous"
        or not check_password_hash(
            in_user["password"], request.json["password"])
    ):
        return jsonify({
            "status": 400,
            "error": "your email or password is incorrect"
        })

    if in_user["status"] == "signed_up":
        send_mail(
            in_user["email"],
            "Welcome to Meji! Please Confirm Your Email to Get Started",
            request.json['email_template'].format(
                name=in_user["name"],
                token=token_tool().dumps(
                    in_user["key"]
                )
            ))

        return jsonify({
            "status": 400,
            "error": "not confirmed"
        })

    if out_user['key'] != in_user['key'] and out_user['status'] == "anonymous":
        cur.execute('SELECT * FROM save WHERE user_key = %s;',
                    (out_user["key"],))
        out_saves = cur.fetchall()
        cur.execute('SELECT * FROM save WHERE user_key = %s;',
                    (in_user["key"],))
        in_saves = cur.fetchall()
        in_saves = [x["item_key"] for x in in_saves]
        for x in out_saves:
            if x["item_key"] not in in_saves:
                cur.execute("""
                    UPDATE save
                    SET user_key = %s
                    WHERE key = %s;
                """, (
                    in_user["key"],
                    x["key"]
                ))

        out_items = []
        in_items = []

        cur.execute("""
            SELECT * FROM "order"
            WHERE "order".user_key = %s AND "order".status = 'cart';
        """, (out_user["key"],))
        out_cart = cur.fetchone()
        if out_cart:
            cur.execute("""
                SELECT * FROM order_item WHERE order_item.order_key = %s;
            """, (out_cart["key"],))
            out_items = cur.fetchall()
        cur.execute("""
            SELECT * FROM "order"
            WHERE "order".user_key = %s AND "order".status = 'cart';
        """, (in_user["key"],))
        in_cart = cur.fetchone()
        if in_cart:
            cur.execute("""
                SELECT * FROM order_item WHERE order_item.order_key = %s;
            """, (in_cart["key"],))
            in_items = cur.fetchall()

        available_items = [
            f"{x['item_key']}_{json.dumps(x['variation'])}" for x in in_items]
        for x in out_items:
            if (f"{x['item_key']}_{json.dumps(x['variation'])}"
                    in available_items):
                cur.execute("""
                    UPDATE order_item
                    SET quantity = %s
                    WHERE
                        order_item.order_key = %s
                        AND order_item.item_key = %s
                        AND order_item.variation = %s;
                """, (
                    x["quantity"],
                    in_cart["key"],
                    x["item_key"],
                    json.dumps(x["variation"])
                ))
            else:
                cur.execute("""
                    UPDATE order_item SET order_key = %s WHERE key = %s;
                """, (
                    in_cart["key"],
                    x["key"]
                ))

        # TODO: REMOVE:
        # DELETE 'FROM order_item WHERE order_key = %s' IF CASCADE WORKS
        cur.execute("""
            DELETE FROM save WHERE user_key = %s;
            DELETE FROM order_item WHERE order_key = %s;
            DELETE FROM "order" WHERE "order".key = %s
                AND "order".status = 'cart';
        """, (
            out_user["key"], out_cart["key"], out_cart["key"]
        ))

    cur.execute("""
        UPDATE "user" SET login = %s
        WHERE key = %s RETURNING *;""", (
        True, in_user["key"]
    ))

    cur.execute("""
        INSERT INTO log (
            key, date, user_key, action, entity_key, entity_type, misc
        ) VALUES (%s, %s, %s, %s, %s, %s, %s);
    """, (
        uuid4().hex, datetime.now(),
        in_user["key"],
        "logged_in",
        None,
        "auth",
        json.dumps({
            "from": out_user["key"],
            "name": out_user["name"]
        }) if in_user["key"] != out_user["key"] else None
    ))

    if in_user["key"] != out_user["key"]:
        cur.execute("""
            INSERT INTO log (
                key, date, user_key, action, entity_key, entity_type, misc
            ) VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (
            uuid4().hex,
            datetime.now(),
            out_user["key"],
            "logged_out",
            None,
            "auth",
            json.dumps({
                "to": in_user["key"],
                "name": in_user["name"]
            })
        ))

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "token": token_tool().dumps(in_user["key"])
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

    key = uuid4().hex
    cur.execute("""
        INSERT INTO "user" (
            key, version, name, email, password, setting_theme
        ) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *;
    """, (
        key, uuid4().hex, f"user_{key[-4:]}", uuid4().hex,
        generate_password_hash(uuid4().hex, method="scrypt"),
        user["setting_theme"]
    ))
    anon_user = cur.fetchone()

    cur.execute("""
        INSERT INTO log (
            key, date, user_key, action, entity_key, entity_type, misc
        ) VALUES (%s, %s, %s, %s, %s, %s, %s);
    """, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "logged_out",
        None,
        "auth",
        json.dumps({
            "to": anon_user["key"],
            "name": anon_user["name"]
        })
    ))

    cur.execute("""
        INSERT INTO log (
            key, date, user_key, action, entity_key, entity_type, misc
        ) VALUES (%s, %s, %s, %s, %s, %s, %s);
    """, (
        uuid4().hex,
        datetime.now(),
        anon_user["key"],
        "created",
        None,
        "auth",
        json.dumps({
            "from": user["key"],
            "name": user["name"]
        })
    ))

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "user": user_schema(anon_user),
        "token": token_tool().dumps(anon_user["key"])
    })


@bp.post("/forgot/password")
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

    cur.execute("""
        INSERT INTO log (
            key, date, user_key, action, entity_key, entity_type, status
        ) VALUES (%s, %s, %s, %s, %s, %s, %s);
    """, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "forgot_password",
        None,
        "auth",
        201
    ))

    db_close(con, cur)

    return jsonify({
        "status": 200
    })


@bp.post("/forgot/password/<token>")
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

    cur.execute("""
    INSERT INTO log (
        key, date, user_key, action, entity_key, entity_type
    ) VALUES (%s, %s, %s, %s, %s, %s);
""", (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "changed_password",
        None,
        "auth"
    ))

    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })
