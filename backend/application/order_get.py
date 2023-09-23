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

    if "admin" in request.args and "admin" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    page_no = 1
    if "page_no" in request.args:
        page_no = int(request.args.get("page_no"))
    size = 24
    status = "ordered"
    if "status" in request.args:
        status = request.args.get("status")

    orders = []
    for row in db:
        if row["type"] != "order":
            continue
        if status and row["status"] != status:
            continue
        if "admin" not in request.args and row["user"] != user["key"]:
            continue
        orders.append(row)

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
    if not order:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if (
        order["info"]["account"] > user["acc_balance"]
        and order["status"] == "pending"
    ):
        order["info"]["account"] = 0
        database(order)

    previous_recipients = []
    for x in db:
        if (
            x["type"] == "order"
            and x["user"] == user["key"]
            and x["status"] == "delivered"
        ):
            previous_recipients.append({
                "name": x["recipient"]["name"],
                "phone": x["recipient"]["phone"],
                "address": x["recipient"]["address"],
                "date": x["date_u"],
            })

    previous_recipients = sorted(previous_recipients, key=lambda d: d['date'])

    return jsonify({
        "status": 200,
        "order": order_schema(order, db),
        "previous_recipients": previous_recipients[:5]
    })
