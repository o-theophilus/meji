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

    page_no = int(request.args["page_no"]) if "page_no" in request.args else 1
    size = int(request.args["size"]) if "size" in request.args else 24
    status = request.args["status"] if "status" in request.args else ""
    status = status.split(":") if status else status

    logs = []
    for x in db:
        if x["type"] != "log":
            continue
        if x["user"] != user["key"]:
            continue
        if (
            status
            and (
                x["entity_type"] != status[0]
                or x["action"] != status[1]
            )
        ):
            continue
        logs.append(x)

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
