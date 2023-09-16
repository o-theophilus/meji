from flask import Blueprint, jsonify, request
from .tools import token_to_user
from .schema import log_schema
from .database import database
from math import ceil
from .tools import now
from uuid import uuid4

bp = Blueprint("log", __name__)


def log_template(
    user,
    action,
    entity,
    entity_type=None,
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
        "entity_type": entity_type,
        "status": status,
        "misc": misc
    }


@bp.get("/log")
def get_many():
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

    logs = sorted(logs, key=lambda d: d["date"], reverse=True)

    total_page = ceil(len(logs) / size)

    start = (page_no - 1) * size
    stop = start + size
    logs = logs[start: stop]

    return jsonify({
        "status": 200,
        "logs": [log_schema(x, db) for x in logs],
        "total_page": total_page
    })
