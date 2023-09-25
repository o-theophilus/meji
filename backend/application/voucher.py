from flask import Blueprint, jsonify, request
from .tools import token_to_user, now
from uuid import uuid4
from .database import database, query
from .schema import user_schema, log_schema
from .log import log_template
from math import ceil
from datetime import datetime, date

bp = Blueprint("voucher", __name__)


def voucher_schema(voucher):
    return {
        "key": voucher["key"],
        "date": voucher["date_c"],
        "value": voucher["value"],
        "validity": voucher["validity"],
        "status": voucher["status"],
    }


def get_vouchers(db):
    status = request.args["status"] if "status" in request.args else ""
    # search = request.args["search"] if "search" in request.args else ""
    # sort = request.args["sort"] if "sort" in request.args else "latest"
    page_no = int(request.args["page_no"]) if "page_no" in request.args else 1
    size = int(request.args["size"]) if "size" in request.args else 24

    vouchers = []
    for x in db:
        if x["type"] != "voucher":
            continue
        if status and x["status"] != status:
            continue
        vouchers.append(x)

    # vouchers = sorted(logs, key=lambda d: d["date_u"])

    total_page = ceil(len(vouchers) / size)

    start = (page_no - 1) * size
    stop = start + size
    vouchers = vouchers[start: stop]

    return {
        "vouchers": [voucher_schema(x) for x in vouchers],
        "total_page": total_page
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
            "error": "unauthorized access"
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
        "voucher": {
            **voucher_schema(voucher),
            "code": voucher["code"],
            "logs": [log_schema(x, db) for x in logs]
        }
    })


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
            "error": "unauthorized access"
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
            "error": "unauthorized access"
        })

    error = {}

    if "value" not in request.json or not request.json["value"]:
        error["value"] = "this field is required"
    elif (
        type(request.json["value"]) not in [int, float]
        or request.json["value"] <= 0
    ):
        error["value"] = "please enter a valid value"

    if "quantity" not in request.json or not request.json["quantity"]:
        error["quantity"] = "this field is required"
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
            "status": "inactive",  # active, used, deleted, expired
            "validity": None,

            "user": None
        })

        logs.append(log_template(
            user["key"],
            "created",
            key,
            "voucher",
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
            "error": "unauthorized access"
        })

    if (
        "status" not in request.json
        or not request.json["status"]
        or request.json["status"] not in ["inactive", "active"]
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

    log = log_template(
        user["key"],
        "changed_status",
        voucher["key"],
        "voucher",
        misc={
            "from": voucher["status"],
            "to": request.json["status"]
        }
    )
    voucher["status"] = request.json["status"]

    database([voucher, log])

    logs = []
    for x in db:
        if x["type"] == "log" and x["entity"] == voucher["key"]:
            logs.append(x)

    logs.append(log)
    logs = sorted(logs, key=lambda d: d["date"], reverse=True)

    return jsonify({
        "status": 200,
        "voucher": {
            **voucher_schema(voucher),
            "code": voucher["code"],
            "logs": [log_schema(x, db) for x in logs]
        }
    })


@ bp.put("/activate_voucher/<key>")
def activate(key):
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
            "error": "unauthorized access"
        })

    if "validity" not in request.json or not request.json["validity"]:
        return jsonify({
            "status": 400,
            "error": "this field is required"
        })

    validity = request.json["validity"]

    if (
        len(validity) != 10
        or validity[4] != validity[7] != '-'
        or not validity[:4].isdigit()
        or not validity[5:7].isdigit()
        or not validity[8:].isdigit()
    ):
        return jsonify({
            "status": 400,
            "error": "invalid date format"
        })

    if datetime.strptime(validity, '%Y-%m-%d').date() < date.today():
        return jsonify({
            "status": 400,
            "error": 'cannot be back dated'
        })

    voucher = query({"type": "voucher", "key": key}, db=db)
    if not voucher or voucher["status"] != "inactive":
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    log = log_template(
        user["key"],
        "activated",
        voucher["key"],
        "voucher",
        misc={
            "from": voucher["status"],
            "to": "active",
            "validity": validity
        }
    )
    voucher["status"] = "active"
    voucher["validity"] = validity

    database([voucher, log])

    logs = []
    for x in db:
        if x["type"] == "log" and x["entity"] == voucher["key"]:
            logs.append(x)

    logs.append(log)
    logs = sorted(logs, key=lambda d: d["date"], reverse=True)

    return jsonify({
        "status": 200,
        "voucher": {
            **voucher_schema(voucher),
            "code": voucher["code"],
            "logs": [log_schema(x, db) for x in logs]
        }
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

    if "code" not in request.json or not request.json["code"]:
        return jsonify({
            "status": 400,
            "error": "this field is required"
        })

    voucher = query(
        {
            "type": "voucher",
            "code": request.json["code"].lower()
        }, db=db
    )
    if not voucher or len(request.json["code"]) != 10:
        return jsonify({
            "status": 400,
            "error": "invalid code"
        })

    if (
        voucher["status"] != "active"
        or datetime.strptime(
            voucher["validity"], '%Y-%m-%d').date() < date.today()
    ):
        error = f"voucher {voucher['status']}"
        database(log_template(
            user["key"],
            "used",
            voucher["key"],
            "voucher",
            400,
            {"error": error}
        ))
        return jsonify({
            "status": 400,
            "error": error
        })

    user["acc_balance"] += voucher["value"]
    voucher["value"] = 0
    voucher["status"] = "used"

    log = log_template(
        user["key"],
        "used",
        voucher["key"],
        "voucher",
    )

    database([user, voucher, log])

    return jsonify({
        "status": 200,
        "user": user_schema(user, db)
    })
