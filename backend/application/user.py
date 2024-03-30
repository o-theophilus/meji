from flask import Blueprint, jsonify, request
from .tools import token_to_user, token_tool, send_mail, user_schema
import re
from werkzeug.security import generate_password_hash, check_password_hash
from .storage import storage
import random
from .postgres import db_close, db_open
from uuid import uuid4
from datetime import datetime, timedelta
import json


bp = Blueprint("user", __name__)


@bp.put("/user/setting")
def setting():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if (
        "theme" in request.json
        and request.json["theme"] in ["dark", "light"]
    ):
        cur.execute("""
            UPDATE "user"
            SET setting_theme = %s
            WHERE key = %s;
        """, (
            request.json["theme"],
            user["key"]
        ))

        cur.execute("""
            INSERT INTO log (
                key, date, user_key, action, entity_key, entity_type, misc
            ) VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (
            uuid4().hex,
            datetime.now(),
            user["key"],
            "changed_theme",
            None,
            "user",
            json.dumps({
                "from": user["setting_theme"],
                "to": request.json["theme"]
            })
        ))

    if (
        "item_view" in request.json
        and request.json["item_view"] in ["grid", "list"]
    ):
        cur.execute("""
            UPDATE "user"
            SET setting_item_view = %s
            WHERE key = %s;
        """, (
            request.json["item_view"],
            user["key"]
        ))

        cur.execute("""
            INSERT INTO log (
                key, date, user_key, action, entity_key, entity_type, misc
            ) VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (
            uuid4().hex,
            datetime.now(),
            user["key"],
            "changed_view",
            None,
            "user",
            json.dumps({
                "from": user["setting_item_view"],
                "to": request.json["item_view"]
            })
        ))

    db_close(con, cur)

    return jsonify({
        "status": 200
    })


@bp.put("/user/<key>")
def edit_user(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user or user["key"] != key:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    error = {}

    if "name" in request.json:
        if not request.json["name"]:
            error['name'] = "this field is required"
        else:
            cur.execute("""
                UPDATE "user"
                SET name = %s
                WHERE key = %s;
            """, (
                request.json["name"],
                user["key"]
            ))

    if "phone" in request.json:
        if not request.json["phone"]:
            error['phone'] = "this field is required"
        else:
            cur.execute("""
                UPDATE "user"
                SET phone = %s
                WHERE key = %s;
            """, (
                request.json["phone"],
                user["key"]
            ))

    if (
        "line" in request.json
        or "state" in request.json
        or "country" in request.json
        or "local_area" in request.json
        or "postal_code" in request.json
    ):
        if not request.json["line"]:
            error["line"] = "this field is required"
        else:
            cur.execute("""
                UPDATE "user"
                SET address_line = %s
                WHERE key = %s;
            """, (
                request.json["line"],
                user["key"]
            ))
        if not request.json["state"]:
            error["state"] = "this field is required"
        else:
            cur.execute("""
                UPDATE "user"
                SET address_state = %s
                WHERE key = %s;
            """, (
                request.json["state"],
                user["key"]
            ))
        if not request.json["country"]:
            error["country"] = "this field is required"
        else:
            cur.execute("""
                UPDATE "user"
                SET address_country = %s
                WHERE key = %s;
            """, (
                request.json["country"],
                user["key"]
            ))
        if not request.json["local_area"]:
            error["local_area"] = "this field is required"
        else:
            cur.execute("""
                UPDATE "user"
                SET address_local_area = %s
                WHERE key = %s;
            """, (
                request.json["local_area"],
                user["key"]
            ))
        if not request.json["postal_code"]:
            error["postal_code"] = "this field is required"
        else:
            cur.execute("""
                UPDATE "user"
                SET address_postal_code = %s
                WHERE key = %s;
            """, (
                request.json["postal_code"],
                user["key"]
            ))

    if error != {}:
        return jsonify({
            "status": 400,
            **error
        })

    cur.execute("""
        INSERT INTO log (
            key, date, user_key, action, entity_key, entity_type, misc
        ) VALUES (%s, %s, %s, %s, %s, %s, %s);
    """, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "edited",
        None,
        "user",
        request.json
    ))

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })


@bp.post("/user/email/otp")
def send_email_otp():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if (
        "email" not in request.json
        or not request.json["email"]
        or "email_template" not in request.json
        or not request.json["email_template"]
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if user["email"] == request.json["email"]:
        return jsonify({
            "status": 400,
            "email": "please use a different email form your current email"
        })

    cur.execute('SELECT * FROM "user" WHERE email = %s;',
                (request.json["email"],))
    exist = cur.fetchone()
    if exist:
        return jsonify({
            "status": 400,
            "email": "email is already in use"
        })

    cur.execute("DELETE FROM otp WHERE user_key = %s;", (user["key"],))

    otp_1 = str(random.randint(1000, 9999))
    otp_2 = str(random.randint(1000, 9999))
    key_1 = uuid4().hex
    key_2 = uuid4().hex

    cur.execute("""
            INSERT INTO otp (key, user_key, pin, email)
            VALUES (%s, %s, %s, %s), (%s, %s, %s, %s);
        """, (
        key_1,
        user["key"],
        otp_1,
        user['email'],

        key_2,
        user["key"],
        otp_2,
        request.json["email"]
    ))

    cur.execute("""
        INSERT INTO log (
            key, date, user_key, action, entity_key, entity_type, misc
        ) VALUES (%s, %s, %s, %s, %s, %s, %s), (%s, %s, %s, %s, %s, %s, %s);
    """, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "requested",
        key_1,
        "otp",
        json.dumps({"to": user['email']}),

        uuid4().hex,
        datetime.now(),
        user["key"],
        "requested",
        key_2,
        "otp",
        json.dumps({"to": request.json['email']})
    ))

    send_mail(
        user["email"],
        "Email Change Confirmation - One-Time Password (OTP)",
        request.json['email_template'].format(
            otp=otp_1
        )
    )
    send_mail(
        request.json["email"],
        "Email Change Confirmation - One-Time Password (OTP)",
        request.json['email_template'].format(
            otp=otp_2
        )
    )

    db_close(con, cur)

    return jsonify({
        "status": 200
    })


@bp.put("/user/email")
def email():
    con, cur = db_open()

    user = token_to_user(cur)

    error = {}
    cur.execute('SELECT * FROM "user" WHERE email = %s;',
                (request.json["email"],))
    email_exist = cur.fetchone()

    if "email" not in request.json or not request.json["email"]:
        error["email"] = "this field is required"
    elif not re.match(r"\S+@\S+\.\S+", request.json["email"]):
        error["email"] = "Please enter a valid email"
    elif user["email"] == request.json["email"]:
        error["email"] = "please use a different email form your current email"
    elif email_exist:
        error["email"] = "email is already in use"

    if "otp_1" not in request.json or not request.json["otp_1"]:
        error["otp_1"] = "this field is required"
    else:
        cur.execute("""
            SELECT otp.*, log.date
            FROM otp
            LEFT JOIN log ON
                otp.key = log.entity_kty,
                log.entity_type = 'otp'
                log.action = 'requested'
            WHERE
                otp.user = %s
                AND otp.pin = %s
                AND otp.email = %s;
        """, (
            user['key'],
            request.json["otp_1"],
            user['email']
        ))
        otp_1 = cur.fetchone()

        if not otp_1:
            error["otp_1"] = "invalid OTP"
        elif datetime.now() - otp_1["date"] > timedelta(minutes=15):
            cur.execute("DELETE FROM otp WHERE user_key = %s;", (user["key"],))
            error["otp_1"] = "invalid OTP"

    if "otp_2" not in request.json or not request.json["otp_2"]:
        error["otp_2"] = "this field is required"
    else:
        cur.execute("""
            SELECT otp.*, log.date
            FROM otp
            LEFT JOIN log ON
                otp.key = log.entity_kty,
                log.entity_type = 'otp'
                log.action = 'requested'
            WHERE
                otp.user = %s
                AND otp.pin = %s
                AND otp.email = %s;
        """, (
            user['key'],
            request.json["otp_2"],
            request.json["email"]
        ))
        otp_2 = cur.fetchone()

        if not otp_2:
            error["otp_2"] = "invalid OTP"
        elif datetime.now() - otp_2["date"] > timedelta(minutes=15):
            cur.execute("DELETE FROM otp WHERE user_key = %s;", (user["key"],))
            error["otp_2"] = "invalid OTP"

    if error != {}:
        return jsonify({
            "status": 400,
            **error
        })

    cur.execute("""
        INSERT INTO log (
            key, date, user_key, action, entity_key, entity_type, misc
        ) VALUES (%s, %s, %s, %s, %s, %s, %s);
    """, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "changed_email",
        None,
        "user",
        json.dumps({
            "from": user['email'],
            "to": request.json['email']
        })
    ))
    cur.execute("""
        UPDATE "user"
        SET email = %s
        WHERE key = %s
        RETURNING *;
    """, (
        request.json["email"],
        user["key"]
    ))
    user = cur.fetchone()
    cur.execute("DELETE FROM otp WHERE user_key = %s;", (user["key"],))

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })


@bp.post("/user/password/otp")
def send_password_otp():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if (
        "email_template" not in request.json
        or not request.json["email_template"]
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("DELETE FROM otp WHERE user_key = %s;", (user["key"],))

    otp = str(random.randint(1000, 9999))
    key = uuid4().hex

    cur.execute("""
            INSERT INTO otp (key, user_key, pin, email)
            VALUES (%s, %s, %s, %s);
        """, (
        key,
        user["key"],
        otp,
        user["email"]
    ))

    cur.execute("""
    INSERT INTO log (
            key, date, user_key, action, entity_key, entity_type, misc
        ) VALUES (%s, %s, %s, %s, %s, %s, %s);
    """, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "requested",
        key,
        "otp",
        json.dumps({"to": user['email']})
    ))

    send_mail(
        user["email"],
        "Password Change Confirmation - One-Time Password (OTP)",
        request.json['email_template'].format(
            otp=otp
        )
    )

    db_close(con, cur)

    return jsonify({
        "status": 200
    })


@bp.put("/user/password")
def password():
    con, cur = db_open()

    user = token_to_user(cur)

    error = {}
    if "password" not in request.json or not request.json["password"]:
        error["password"] = "this field is required"
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

    if (
        "confirm_password" not in request.json
        or not request.json["confirm_password"]
    ):
        error["confirm_password"] = "this field is required"
    elif (
            request.json["password"]
            and "password" not in error
            and request.json["confirm_password"] != request.json["password"]
    ):
        error["confirm_password"] = """Password and confirm_password password
         does not match"""

    if "otp" not in request.json or not request.json["otp"]:
        error["otp"] = "this field is required"
    else:
        cur.execute("""
            SELECT otp.*, log.date
            FROM otp
            LEFT JOIN log ON
                otp.key = log.entity_kty,
                log.entity_type = 'otp'
                log.action = 'requested'
            WHERE
                otp.user = %s
                AND otp.pin = %s
                AND otp.email = %s;
        """, (
            user['key'],
            request.json["otp"],
            user["email"]
        ))
        otp = cur.fetchone()

        if not otp:
            error["otp"] = "invalid OTP"
        elif datetime.now() - otp["date"] > timedelta(minutes=15):
            cur.execute("DELETE FROM otp WHERE user_key = %s;", (user["key"],))
            error["otp"] = "invalid OTP"

    if error != {}:
        return jsonify({
            "status": 400,
            **error
        })

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
        "user"
    ))
    cur.execute("""
        UPDATE "user"
        SET password = %s
        WHERE key = %s;
    """, (
        generate_password_hash(request.json["password"], method="scrypt"),
        user["key"]
    ))
    cur.execute("DELETE FROM otp WHERE user_key = %s;", (user["key"],))

    db_close(con, cur)

    return jsonify({
        "status": 200
    })


@ bp.delete("/user")
def delete():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if not request.json["password"]:
        return jsonify({
            "status": 400,
            "error": "this field is required"
        })

    if not check_password_hash(user["password"], request.json["password"]):
        return jsonify({
            "status": 400,
            "error": "incorrect password"
        })

    cur.execute("""
        UPDATE "user"
        SET status = %s, login = %s
        WHERE key = %s;
    """, (
        "deleted",
        False,
        user["key"]
    ))

    cur.execute("""
        INSERT INTO "user" (key, version, email, password, setting_theme)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING *;
    """, (
        uuid4().hex, uuid4().hex, uuid4().hex,
        generate_password_hash(uuid4().hex, method="scrypt"),
        user["setting_theme"]
    ))
    anon_user = cur.fetchone()

    cur.execute("""
        INSERT INTO log (
            key, date, user_key, action, entity_key, entity_type
        ) VALUES (%s, %s, %s, %s, %s, %s);
    """, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "deleted_account",
        None,
        "user"
    ))

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "user": user_schema(anon_user),
        "token": token_tool().dumps(anon_user["key"])
    })


@bp.put("/user/photo")
def add_photo():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if 'file' not in request.files:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    file = request.files["file"]
    media, format = file.content_type.split("/")
    if media != "image" or format in ['svg+xml', 'x-icon']:
        return jsonify({
            "status": 400,
            "error": "invalid file"
        })

    if user["photo"]:
        storage(user["photo"], delete=True)

    cur.execute("""
        UPDATE "user"
        SET photo = %s
        WHERE key = %s
        RETURNING *;
    """, (
        storage(file),
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
        "updated_photo",
        None,
        "user"
    ))

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })


@bp.delete("/user/photo")
def delete_photo():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    storage(user["photo"].split("/")[-1], delete=True)

    cur.execute("""
        UPDATE "user"
        SET photo = %s
        WHERE key = %s;
    """, (
        None,
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
        "deleted_photo",
        None,
        "user"
    ))

    db_close(con, cur)

    return jsonify({
        "status": 200
    })
