from flask import Blueprint, jsonify, request
from .tools import token_to_user
from .schema import order_schema
from .database import database
from math import ceil

bp = Blueprint("order_get", __name__)


@bp.get("/order")
def get_all():
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

    size = 24
    status = request.args.get("status")
    search = request.args.get("search")
    page_no = int(request.args.get("page_no"))

    orders = []
    for row in data:
        if row["type"] == "order":
            if status and search:
                if row["status"] == status:
                    orders.append(row)
            elif search:
                if row["key"] == search:
                    orders.append(row)
            elif status:
                if row["status"] == status:
                    orders.append(row)
            else:
                orders.append(row)

    # orders = sorted(orders, key=lambda d: d["date_u"])

    total_page = ceil(len(orders) / size)

    start = (page_no - 1) * size
    stop = start + size
    orders = orders[start: stop]

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "orders": [order_schema(order, data) for order in orders],
            "total_page": total_page
        }
    })


@bp.get("/order_/<key>")
def get_for_user(key):
    data = database()

    user = token_to_user(data)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    if user["key"] != key and "admin" not in user["roles"]:
        return jsonify({
            "status": 102,
            "message": "unauthorised access"
        })

    orders = []
    for row in data:
        if row["type"] == "order" and row["user_key"] == user["key"]:
            orders.append(row)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "orders": [order_schema(order, data) for order in orders]
        }
    })


@bp.get("/order/<key>")
def get_one(key):
    data = database()

    user = token_to_user(data)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    order = query("order", "key", key, data)
    if not order:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    if order["info"]["account"] > user["acc_balance"]:
        order["info"]["account"] = 0

        order = database(order)

    pr = []
    for row in data:
        if (
            row["type"] == "order"
            and row["user_key"] == user["key"]
            and row["status"] == "delivered"
        ):
            pr.append({
                "name": row["recipient"]["name"],
                "phone": row["recipient"]["phone"],
                "address": row["recipient"]["address"],
                "date": row["date_u"],
            })

    pr = sorted(pr, key=lambda d: d['date'])
    pr = pr[: 5]

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "order": order_schema(order, data),
            "previous_recipients": pr,
        }
    })


@bp.get("/order_ref/<key>")
def get_ref(key):
    data = database()

    user = token_to_user(data)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    order = query("order", "pay_reference", key, data)
    if not order:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "order": order_schema(order, data),
        }
    })
