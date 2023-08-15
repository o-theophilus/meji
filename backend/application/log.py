from flask import Blueprint, jsonify, request
from .tools import token_to_user
from .schema import log_schema
from .database import database, query
from math import ceil
from .tools import now
from uuid import uuid4

bp = Blueprint("log", __name__)


def log_template(
    user,
    action,
    entity,
    status=200,
    misc=None,
):
    return {
        "key": uuid4().hex,
        "date": now(),
        "type": "log",

        "user": user,
        "action": action,
        "entity": entity,
        "status": status,
        "misc": misc
    }


@bp.get("/logs")
def get():
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    page_no = 1
    if "page_no" in request.args:
        page_no = int(request.args.get("page_no"))
    size = 24
    action = None
    if "action" in request.args:
        action = request.args.get("action")

    logs = []
    for row in db:
        if row["type"] != "log":
            continue
        if row["user"] != user["key"]:
            continue
        if action and row["action"] != action:
            continue
        logs.append(row)

    # logs = sorted(logs, key=lambda d: d["date_u"])

    start = (page_no - 1) * size
    stop = start + size
    logs = logs[start: stop]

    return jsonify({
        "status": 200,
        "logs": [log_schema(x, db) for x in logs],
        "total_page": ceil(len(logs) / size)
    })


@bp.get("/log/<key>")
def get_one(key):
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    order = query({"type": "order", "key": key}, db=db)
    if not order:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if order["info"]["account"] > user["acc_balance"]:
        order["info"]["account"] = 0

        order = database(order)

    pr = []
    for x in db:
        if (
            x["type"] == "order"
            and x["user"] == user["key"]
            and x["status"] == "delivered"
        ):
            pr.append({
                "name": x["recipient"]["name"],
                "phone": x["recipient"]["phone"],
                "address": x["recipient"]["address"],
                "date": x["date_u"],
            })

    pr = sorted(pr, key=lambda d: d['date'])
    pr = pr[: 5]

    return jsonify({
        "status": 200,
        "order": log_schema(order, db),
        "previous_recipients": pr,
    })
