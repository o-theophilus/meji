from flask import Blueprint, jsonify, request
from .tools import token_to_user, now
from uuid import uuid4
from .database import database, query
from .schema import user_schema
from .log import log_template

bp = Blueprint("voucher", __name__)


def voucher_schema(voucher):
    return {
        "key": voucher["key"],
        "value": voucher["value"],
        "status": voucher["status"],
    }


@ bp.get("/voucher/<key>")
def get(key):
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })
    if "admin" not in user["roles"]:
        return jsonify({
            "status": 102,
            "message": "unauthorised access"
        })

    voucher = query("voucher", "key", key, db)
    if not voucher:
        return jsonify({
            "status": 400,
            "message": "invalid request"
        })

    logs = []
    for row in db:
        if (
            row["type"] == "log"
            and row["for"] == "voucher"
            and row["entity"] == voucher["key"]
        ):
            logs.append(row)

    logs = sorted(logs, key=lambda d: d["date"], reverse=True)

    return jsonify({
        "status": 200,
        "message": "successful",
        "db": {
            "voucher": voucher_schema(voucher),
            "logs": logs
        }
    })


@ bp.get("/voucher")
def get_many():
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })
    if "admin" not in user["roles"]:
        return jsonify({
            "status": 102,
            "message": "unauthorised access"
        })

    vouchers = []
    for row in db:
        if "type" in row and row["type"] == "voucher":
            vouchers.append(row)

    return jsonify({
        "status": 200,
        "message": "successful",
        "db": {
            "vouchers": [voucher_schema(voucher) for voucher in vouchers]
        }
    })


@bp.post("/voucher")
def create():
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })
    if "admin" not in user["roles"]:
        return jsonify({
            "status": 102,
            "message": "unauthorised access"
        })

    error = {}

    if "value" not in request.json or not request.json["value"]:
        error["value"] = "This field is reqired"
    elif type(request.json["value"]) != int or request.json["value"] < 1:
        error["value"] = "Please enter a valid value"

    if error != {}:
        return jsonify({
            "status": 201,
            "message": error
        })

    voucher = {
        "date_c": now(),

        "key": str(uuid4().hex)[:10],
        "value": request.json["value"],

        "status": "inactive",
        "type": "voucher",
    }

    log = log_template(
        "voucher",
        user["key"],
        voucher["key"],
        "created",
        200,
    )

    database([voucher, log])

    return jsonify({
        "status": 200,
        "message": "successful",
        "db": {
            "voucher": voucher_schema(voucher),
        }
    })


@bp.post("/user_voucher")
def user_voucher():
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })
    if not user["login"]:
        return jsonify({
            "status": 201,
            "message": "please login"
        })

    if "code" not in request.json or not request.json["code"]:
        return jsonify({
            "status": 201,
            "message": "this field is required"
        })

    if len(request.json["code"]) != 10:
        return jsonify({
            "status": 201,
            "message": "invalid code"
        })

    voucher = query("voucher", "key", request.json["code"], db)
    if not voucher:
        return jsonify({
            "status": 201,
            "message": "invalid code"
        })

    if voucher["status"] == "used":
        return jsonify({
            "status": 201,
            "message": "voucher used"
        })

    user["acc_balance"] += voucher["value"]
    voucher["status"] = "used"
    voucher["value"] = 0

    log = log_template(
        "voucher",
        user["key"],
        voucher["key"],
        "used",
        200,
    )

    database([user, voucher, log])

    return jsonify({
        "status": 200,
        "message": "successful",
        "db": {
            "user": user_schema(user, db)
        }
    })


@ bp.put("/voucher/<key>")
def put(key):
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    if "admin" not in user["roles"]:
        return jsonify({
            "status": 102,
            "message": "unauthorised access"
        })

    if not user["login"]:
        return jsonify({
            "status": 201,
            "message": "please login"
        })

    if "status" not in request.json or not request.json["status"]:
        return jsonify({
            "status": 400,
            "message": "invalid request"
        })

    voucher = query("voucher", "key", key, db)
    if not voucher:
        return jsonify({
            "status": 400,
            "message": "invalid request"
        })

    log = []
    if request.json["status"] in ["active", "inactive"]:
        if voucher["status"] in ["active", "inactive"]:
            log = log_template(
                "voucher",
                user["key"],
                voucher["key"],
                "change_status",
                200,
                f"""
                from: {voucher['status']}, to: {request.json['status']}
                """
            )

            voucher["status"] = request.json["status"]

            database([voucher, log])

    logs = []
    for row in db:
        if (
            row["type"] == "log"
            and row["for"] == "voucher"
            and row["entity"] == voucher["key"]
        ):
            logs.append(row)

    if log != []:
        logs.append(log)
    logs = sorted(logs, key=lambda d: d["date"], reverse=True)

    return jsonify({
        "status": 200,
        "message": "successful",
        "db": {
            "voucher": voucher_schema(voucher),
            "logs": logs
        }
    })
