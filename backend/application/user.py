from flask import Blueprint, jsonify, request
from .tools import token_to_user, now, token_tool, send_mail
from werkzeug.security import check_password_hash
from .schema import user_schema, otp_template
from .auth import user_template
from .database import database, query
import re
from werkzeug.security import generate_password_hash
from .storage import storage
import random
from uuid import uuid4


bp = Blueprint("user", __name__)


@bp.post("/setting")
def post():
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if (
        "theme" in request.json
        and request.json["theme"] in ["dark", "light"]
    ):
        user["setting"]["theme"] = request.json["theme"]
    if (
        "item_view" in request.json
        and request.json["item_view"] in ["grid", "list"]
    ):
        user["setting"]["item_view"] = request.json["item_view"]

    user = database(user)

    return jsonify({
        "status": 200
    })


@ bp.put("/user/<key>")
def edit_user(key):
    db = database()

    user = token_to_user(db)
    if (
        not user
        or (
            user["key"] != key
            and "admin" not in user["roles"]
        )
    ):
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    if user["key"] != key:
        user = query({"type": "user", "key": key}, db=db)
        if not user:
            return jsonify({
                "status": 400,
                "error": "invalid request"
            })

    error = {}

    if "name" in request.json:
        if not request.json["name"]:
            error['name'] = "this field is required"
        else:
            user["name"] = request.json["name"]

    if "phone" in request.json:
        if not request.json["phone"]:
            error['phone'] = "this field is required"
        else:
            user["phone"] = request.json["phone"]

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
            user["address"]["line"] = request.json["line"]
        if not request.json["state"]:
            error["state"] = "this field is required"
        else:
            user["address"]["state"] = request.json["state"]
        if not request.json["country"]:
            error["country"] = "this field is required"
        else:
            user["address"]["country"] = request.json["country"]
        if not request.json["local_area"]:
            error["local_area"] = "this field is required"
        else:
            user["address"]["local_area"] = request.json["local_area"]
        if not request.json["postal_code"]:
            error["postal_code"] = "this field is required"
        else:
            user["address"]["postal_code"] = request.json["postal_code"]

    if error != {}:
        return jsonify({
            "status": 400,
            **error
        })

    user["date_u"] = now(),
    user = database(user)

    return jsonify({
        "status": 200,
        "user": user_schema(user, db)
    })


@bp.post("/email_otp")
def send_email_otp():
    db = database()

    user = token_to_user(db)
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

    exist = query({"type": "user", "email": request.json["email"]}, db=db)
    if exist:
        return jsonify({
            "status": 400,
            "email": "email is already in use"
        })

    otps = query({"type": "otp", "user": user['key']}, many=True, db=db)
    database(otps, delete=True)

    otp_1 = str(random.randint(1000, 9999))
    otp_2 = str(random.randint(1000, 9999))

    database([
        otp_template(
            user['key'],
            user['email'],
            otp_1
        ),
        otp_template(
            user['key'],
            request.json["email"],
            otp_2
        )
    ])

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

    return jsonify({
        "status": 200
    })


@bp.post("/email")
def email():
    db = database()

    user = token_to_user(db)

    error = {}
    if "email" not in request.json or not request.json["email"]:
        error["email"] = "this field is required"
    elif not re.match(r"\S+@\S+\.\S+", request.json["email"]):
        error["email"] = "Please enter a valid email"
    elif user["email"] == request.json["email"]:
        error["email"] = "please use a different email form your current email"
    elif query({"type": "user", "email": request.json["email"]}, db=db):
        error["email"] = "email is already in use"

    if "otp_1" not in request.json or not request.json["otp_1"]:
        error["otp_1"] = "this field is required"
    else:
        otp_1 = query(
            {"type": "otp", "user": user['key'],
                "entity": user['email'], "otp": request.json["otp_1"]},
            db=db)

        if not otp_1:
            error["otp_1"] = "invalid OTP"

    if "otp_2" not in request.json or not request.json["otp_2"]:
        error["otp_2"] = "this field is required"
    else:
        otp_2 = query(
            {"type": "otp", "user": user['key'],
                "entity": request.json["email"], "otp": request.json["otp_2"]},
            db=db)
        if not otp_2:
            error["otp_2"] = "invalid OTP"

    if error != {}:
        return jsonify({
            "status": 400,
            **error
        })

    user["email"] = request.json["email"]
    user = database(user)
    database(otp_1, delete=True)
    database(otp_2, delete=True)

    return jsonify({
        "status": 200,
        "user": user_schema(user, db)
    })


@bp.post("/password_otp")
def send_password_otp():
    db = database()

    user = token_to_user(db)
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

    otps = query({"type": "otp", "user": user['key']}, many=True, db=db)
    database(otps, delete=True)

    otp = str(random.randint(1000, 9999))

    database(otp_template(
        user['key'],
        user['email'],
        otp
    ))

    send_mail(
        user["email"],
        "Password Change Confirmation - One-Time Password (OTP)",
        request.json['email_template'].format(
            otp=otp
        )
    )

    return jsonify({
        "status": 200
    })


@bp.post("/password")
def password():
    db = database()

    user = token_to_user(db)

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
        otp = query(
            {"type": "otp", "user": user['key'],
                "entity": user['email'], "otp": request.json["otp"]},
            db=db)

        if not otp:
            error["otp"] = "invalid OTP"

    if error != {}:
        return jsonify({
            "status": 400,
            **error
        })

    user["password"] = generate_password_hash(
        request.json["password"], method="scrypt")
    user = database(user)
    database(otp, delete=True)

    return jsonify({
        "status": 200
    })


@ bp.delete("/user")
def delete():
    db = database()

    user = token_to_user(db)
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

    user["status"] = "deleted"
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


@bp.post("/user_photo")
def add_photo():
    db = database()

    user = token_to_user(db)
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
    user["photo"] = storage(file)
    database(user)

    return jsonify({
        "status": 200,
        "user": user_schema(user, db)
    })


@bp.delete("/user_photo")
def delete_photo():
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    storage(user["photo"].split("/")[-1], delete=True)
    user["photo"] = None
    database(user)

    return jsonify({
        "status": 200
    })
