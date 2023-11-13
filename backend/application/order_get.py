from flask import Blueprint, jsonify, request
from .tools import token_to_user
from .schema import order_schema
from .database import database, query
from math import ceil

bp = Blueprint("order_get", __name__)


@bp.get("/orders")
def get():
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    page_no = int(request.args["page_no"]) if "page_no" in request.args else 1
    size = int(request.args["size"]) if "size" in request.args else 24
    status = request.args["status"] if "status" in request.args else "created"
    is_admin = "admin" in request.args

    if is_admin and "order:view" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    orders = []
    for x in db:
        if x["type"] != "order":
            continue
        if status and x["status"] != status:
            continue
        if not is_admin and x["user"] != user["key"]:
            continue
        orders.append(x)

    # orders = sorted(orders, key=lambda d: d["date_u"])

    total_page = ceil(len(orders) / size)
    start = (page_no - 1) * size
    stop = start + size
    orders = orders[start: stop]

    return jsonify({
        "status": 200,
        "orders": [order_schema(order, db) for order in orders],
        "total_page": total_page
    })


@bp.get("/order/<key>")
def get_one(key):
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    order = query({"type": "order", "key": key}, db=db)
    if (
        not order
        or (
            order["user"] != user["key"]
            and "order:view" not in user["roles"]
        )
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    return jsonify({
        "status": 200,
        "order": order_schema(order, db),
    })
