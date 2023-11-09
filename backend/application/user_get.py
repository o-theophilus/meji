from flask import Blueprint, request, jsonify
from .schema import user_schema
from .tools import token_to_user
from .database import database
from math import ceil
import re


bp = Blueprint("user_get", __name__)


@bp.get("/user")
def get_user():
    db = database()

    me = token_to_user(db)
    if not me:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    user = None
    if "search" in request.args:

        if "user:view" not in me["roles"]:
            return jsonify({
                "status": 400,
                "error": "unauthorized access"
            })

        if request.args["search"]:
            for x in db:
                if x["type"] == "user" and (
                    x["key"] == request.args["search"]
                    or x["email"] == request.args["search"]
                ):
                    user = x

                    if "user:view_balance" not in me["roles"]:
                        user["acc_balance"] = "#"

                    break

        if not user:
            return jsonify({
                "status": 400,
                "error": "user not found"
            })

    else:
        user = me

    return jsonify({
        "status": 200,
        "user": user_schema(user, db)
    })


@bp.get("/users")
def get_users():
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "user:view" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    status = request.args["status"] if "status" in request.args else ""
    search = request.args["search"] if "search" in request.args else ""
    sort = request.args["sort"] if "sort" in request.args else "latest"
    page_no = int(request.args["page_no"]) if "page_no" in request.args else 1
    size = int(request.args["size"]) if "size" in request.args else 24

    users = []
    for x in db:
        if x["type"] != "user":
            continue
        if status and x["status"] != status:
            continue
        if (
            search
            and not re.search(
                search,
                f"{x['key']} {x['name']} {x['email']}",
                re.IGNORECASE
            )
        ):
            continue
        users.append(x)

    reverse = sort in ["latest", "name (z-a)"]

    if sort in ["latest", "oldest"]:
        sort = "date_c"
    elif sort in ["name (a-z)", "name (z-a)"]:
        sort = "name"

    users = sorted(users, key=lambda d: d[sort].lower() if isinstance(
        d[sort], str) else d[sort], reverse=reverse)

    total_page = ceil(len(users) / size)
    start = (page_no - 1) * size
    stop = start + size
    users = users[start: stop]

    return jsonify({
        "status": 200,
        "users": [user_schema(x, db) for x in users],
        "total_page": total_page
    })


@bp.get("/admin_users")
def admin_users():
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    page_no = int(request.args["page_no"]) if "page_no" in request.args else 1
    size = int(request.args["size"]) if "size" in request.args else 24

    search = "all:all:all"
    if "search" in request.args:
        search = request.args["search"]

    search = search.split(":")
    if len(search) != 3:
        return jsonify({
            "status": 400,
            "error": "invalid search"
        })

    _user, _type, _role = search

    if "user:view" not in user["roles"]:
        _user = user["key"]

    users = []
    for x in db:
        if x["type"] != "user" or len(x["roles"]) == 0:
            continue

        if _user != 'all':
            if not re.search(
                _user,
                f"{x['key']} {x['name']} {x['email']}",
                re.IGNORECASE
            ):
                continue

        if _type != 'all':
            x_types = [y.split(":")[0] for y in x["roles"]]
            if _type not in x_types:
                continue

        if _role != 'all':
            if f"{_type}:{_role}" not in x["roles"]:
                print("here 2")
                continue

        users.append(x)

    users = sorted(users, key=lambda d: len(d["roles"]), reverse=True)
    print(len(users))

    total_page = ceil(len(users) / size)

    start = (page_no - 1) * size
    stop = start + size
    users = users[start: stop]

    return jsonify({
        "status": 200,
        "users": [user_schema(x, db) for x in users],
        "total_page": total_page
    })
