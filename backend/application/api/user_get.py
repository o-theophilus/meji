from flask import Blueprint, request, jsonify
from .schema import user_schema
from .tools import token_to_user
from .database import database
from math import ceil
import re


bp = Blueprint("user_get", __name__)


def user_master(
    data=[],
    user_key="",
    size=24, status="confirm",
    order="date", order_dir="dsc",
    page_no=1,
    search=None
):

    users = []
    for row in db:
        if (
            "type" in row
            and row["type"] == "user"
            and row["status"] == status
            and row["key"] != user_key
        ):
            if search:
                if (
                    re.search(search, row["name"], re.IGNORECASE)
                    or re.search(search, row["email"], re.IGNORECASE)
                ):
                    users.append(row)
            else:
                users.append(row)

    if order == "date":
        order = "date_c"

    users = sorted(
        users, key=lambda d: d[order], reverse=order_dir == "dsc")

    total_page = ceil(len(users) / size)

    start = (page_no - 1) * size
    stop = start + size
    users = users[start: stop]

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "users": [user_schema(user, data) for user in users],
            "page_no": page_no,
            "total_page": total_page
        }
    })


@bp.get("/user")
def get():
    data = database()

    user = token_to_user(data)
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

    status = request.args.get("status")
    search = request.args.get("search")
    page_no = int(request.args.get("page_no"))
    order = request.args.get("order")
    order_dir = request.args.get("order_dir")

    params = {
        # "db": db,
        "user_key": user["key"],

        "search": search,
        "page_no": page_no,
        "order": order,
        "order_dir": order_dir
    }
    if status:
        params["status"] = status

    return user_master(**params).json


@bp.get("/user/<key>")
def get_one(key):
    data = database()

    me = token_to_user(data)
    if not me:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    if "admin" not in me["roles"]:
        return jsonify({
            "status": 102,
            "message": "unauthorised access"
        })

    user = query("user", "key", key, data)
    if not user or me["key"] == user["key"]:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "user": user_schema(user)
        }
    })
