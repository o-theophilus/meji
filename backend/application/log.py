from flask import Blueprint, jsonify, request
from .tools import token_to_user
from .schema import log_schema
from .database import database, query
from math import ceil
from datetime import datetime
from uuid import uuid4
import re
import json

bp = Blueprint("log", __name__)


def log_template(
    user_key,
    action,
    entity_key=None,
    entity_type=None,
    status=200,
    misc={}
):
    return ("""INSERT INTO log (
        key,
        date,
        user_key,
        action,
        entity_key,
        entity_type,
        status,
        misc
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s
    );""", [
        uuid4().hex, datetime.now(),  user_key, action,
        entity_key, entity_type, status, json.dumps(misc)
    ])


@bp.get("/logs")
def get_many():
    db = database()
    db_log = database(db_name="log")

    user = token_to_user()
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    page_no = int(request.args["page_no"]) if "page_no" in request.args else 1
    size = int(request.args["size"]) if "size" in request.args else 24

    search = "all:all:all:all"
    if "search" in request.args:
        search = request.args["search"]

    search = search.split(":")
    if len(search) != 4:
        return jsonify({
            "status": 400,
            "error": "invalid search"
        })

    _user, _type, _action, _entity = search

    if "log:view" not in user["roles"]:
        _user = user["key"]

    logs = []
    for x in db_log:

        if _user != 'all':
            y = query({"type": "user", "key": x["user"]}, db=db)

            if not y or not re.search(
                _user,
                f"{y['key']} {y['name']} {y['email']}",
                re.IGNORECASE
            ):
                continue

        if _type != 'all':
            if x["entity_type"] != _type:
                continue

        if _action != 'all':
            if x["action"] != _action:
                continue

        if _entity != 'all':
            y = query({"type": x["entity_type"], "key": x["entity"]}, db=db)
            if not y or not re.search(
                _entity,
                f"""
                {y['key'] if 'key' in y else ""}
                {y['name'] if 'name' in y else ""}
                {y['email'] if 'email' in y else ""}
                """,
                re.IGNORECASE
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
