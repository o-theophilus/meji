from flask import Blueprint, jsonify, request
from .tools import token_to_user, now
from uuid import uuid4
from .database import database, query
from .schema import user_schema, log_schema
from .log import log_template
from math import ceil

bp = Blueprint("voucher", __name__)


def voucher_schema(voucher):
    return {
        "key": voucher["key"],
        "date": voucher["date_c"],
        "value": voucher["value"],
        "status": voucher["status"],
    }


@ bp.get("/voucher/<key>")
def get(key):
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })
    if "admin" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorised access"
        })

    voucher = query({"type": "voucher", "key": key}, db=db)
    if not voucher:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    logs = []
    for x in db:
        if x["type"] == "log" and x["entity"] == voucher["key"]:
            logs.append(x)

    logs = sorted(logs, key=lambda d: d["date"], reverse=True)

    return jsonify({
        "status": 200,
        "voucher": voucher_schema(voucher),
        "logs": [log_schema(x, db) for x in logs]
    })


def get_vouchers(db=[]):
    page_no = 1
    if "page_no" in request.args:
        page_no = int(request.args.get("page_no"))
    size = 24
    status = None
    if "status" in request.args:
        status = request.args.get("status")

    vouchers = []
    for x in db:
        if x["type"] != "voucher":
            continue
        if status and x["status"] != status:
            continue
        vouchers.append(x)

    # vouchers = sorted(logs, key=lambda d: d["date_u"])

    start = (page_no - 1) * size
    stop = start + size
    vouchers = vouchers[start: stop]

    return {
        "vouchers": [voucher_schema(x) for x in vouchers],
        "total_page": ceil(len(vouchers) / size)
    }


@ bp.get("/voucher")
def get_many():
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "admin" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorised access"
        })

    return jsonify({
        "status": 200,
        **get_vouchers(db)
    })


@bp.post("/voucher")
def create():
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })
    if "admin" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorised access"
        })

    error = {}

    if "value" not in request.json or not request.json["value"]:
        error["value"] = "this field is reqired"
    elif (
        type(request.json["value"]) not in [int, float]
        or request.json["value"] <= 0
    ):
        error["value"] = "please enter a valid value"

    if "quantity" not in request.json or not request.json["quantity"]:
        error["quantity"] = "this field is reqired"
    elif (
        type(request.json["quantity"]) != int
        or request.json["quantity"] < 1
    ):
        error["quantity"] = "please enter a valid quantity"

    if error != {}:
        return jsonify({
            "status": 400,
            **error
        })

    batch = None
    if request.json["quantity"] > 1:
        batch = uuid4().hex

    vouchers = []
    logs = []
    for x in range(request.json["quantity"]):
        key = uuid4().hex
        vouchers.append({
            "key": key,
            "code": str(uuid4().hex)[:10],
            "type": "voucher",
            "date_c": now(),

            "value": request.json["value"],
            "status": "inactive",  # unused, used
            "validity": None,

            "user": None
        })

        logs.append(log_template(
            user["key"],
            "created_voucher",
            key,
            misc={
                "batch": batch
            }
        ))

    database(vouchers+logs)

    return jsonify({
        "status": 200,
        **get_vouchers(db+vouchers)
    })


@ bp.put("/voucher/<key>")
def status(key):
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "admin" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorised access"
        })

    if (
        "status" not in request.json
        or not request.json["status"]
        or request.json["status"] not in ["inactive", "unused"]
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    voucher = query({"type": "voucher", "key": key}, db=db)
    if not voucher:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    old_status = voucher["status"]
    voucher["status"] = request.json["status"]
    log = log_template(
        user["key"],
        "changed_voucher_status",
        voucher["key"],
        misc={
            "from": old_status,
            "to": request.json["status"]
        }
    )

    database([voucher, log])

    logs = []
    for x in db:
        if x["type"] == "log" and x["entity"] == voucher["key"]:
            logs.append(x)

    logs.append(log)
    logs = sorted(logs, key=lambda d: d["date"], reverse=True)

    return jsonify({
        "status": 200,
        "voucher": voucher_schema(voucher),
        "logs": [log_schema(x, db) for x in logs]
    })


@bp.post("/use_voucher")
def use():
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })
    if not user["login"]:
        return jsonify({
            "status": 400,
            "error": "please login"
        })

    if "code" not in request.json or not request.json["code"]:
        return jsonify({
            "status": 400,
            "error": "this field is required"
        })

    if len(request.json["code"]) != 10:
        return jsonify({
            "status": 400,
            "error": "invalid code"
        })

    voucher = query({"type": "voucher", "code": request.json["code"]}, db=db)
    if not voucher:
        return jsonify({
            "status": 400,
            "error": "invalid code"
        })

    if voucher["status"] == "used":
        return jsonify({
            "status": 400,
            "error": "voucher used"
        })

    user["acc_balance"] += voucher["value"]
    voucher["status"] = "used"
    voucher["value"] = 0

    log = log_template(
        user["key"],
        "used_voucher",
        voucher["key"],
    )

    database([user, voucher, log])

    return jsonify({
        "status": 200,
        "user": user_schema(user, db)
    })
