from flask import Blueprint, jsonify, request
from .tools import token_to_user
from .schema import order_schema
from .database import database, query
from math import ceil

bp = Blueprint("order_get", __name__)


@bp.get("/orders")
def get_all():
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
            "error": "unauthorised access"
        })

    size = 24
    status = request.args.get("status")
    search = request.args.get("search")
    # page_no = int(request.args.get("page_no"))
    page_no = 1

    orders = []
    for row in db:
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
        "orders": [order_schema(order, db) for order in orders],
        "total_page": total_page
    })


@bp.get("/user_orders/<key>")
def get_for_user(key):
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if user["key"] != key and "admin" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorised access"
        })

    orders = []
    for x in db:
        if x["type"] == "order" and x["user_key"] == user["key"]:
            orders.append(order_schema(x, db))

    return jsonify({
        "status": 200,
        "orders": orders
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

    if order["info"]["account"] > user["acc_balance"]:
        order["info"]["account"] = 0

        order = database(order)

    pr = []
    for x in db:
        if (
            x["type"] == "order"
            and x["user_key"] == user["key"]
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
        "order": order_schema(order, db),
        "previous_recipients": pr,
    })


# @bp.get("/order_ref/<key>")
# def get_ref(key):
#     db = database()

#     user = token_to_user(db)
#     if not user:
#         return jsonify({
#             "status": 400,
#             "error": "invalid token"
#         })

#     order = query({"type": "order", "pay_reference": key}, db=db)
#     if not order:
#         return jsonify({
#             "status": 400,
#             "error": "invalid request"
#         })

#     return jsonify({
#         "status": 200,
#         "order": order_schema(order, db),
#     })
