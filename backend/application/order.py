from flask import Blueprint, jsonify, request
from .tools import token_to_user, send_mail, user_schema
import requests
import os
from .postgres import db_close, db_open
from math import ceil
from .log import log
from datetime import datetime, timedelta

bp = Blueprint("order", __name__)


order_status = ['created', 'processing', 'enroute', 'delivered',
                'canceled']


@bp.post("/order")
def cart_to_order():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    cur.execute("""
        SELECT *
        FROM "order"
        WHERE user_key = %s AND status = 'cart';
    """, (user["key"],))
    order = cur.fetchone()

    if (
        not order
        or "email_template_admin" not in request.json
        or not request.json["email_template_admin"]
        or "email_template_user" not in request.json
        or not request.json["email_template_user"]
        or "reference" not in request.json
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if (
        not order["name"]
        or not order["phone"]
        or not order["line"]
        or not order["country"]
        or not order["state"]
        or not order["local_area"]
        or not order["postal_code"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid delivery address"
        })

    to_pay = order["cost_items"] + order[
        "cost_delivery"] - order["pay_account"]

    if to_pay > 0:
        if not request.json['reference']:
            db_close(con, cur)
            return jsonify({
                "status": 400,
                "error": "invalid request"
            })

        cur.execute("""SELECT * FROM "order" WHERE pay_reference = %s;""",
                    (request.json['reference'],))
        if cur.fetchone():
            db_close(con, cur)
            return jsonify({
                "status": 400,
                "error": "invalid request"
            })

        ref = request.json['reference']
        resp = requests.get(
            f"https://api.paystack.co/transaction/verify/{ref}",
            headers={
                'Content-Type': 'application/json',
                "Authorization": os.environ["PAYSTACK_KEY"]
            }
        )
        resp = resp.json()

        if (
            not resp["status"]
            or "data" not in resp
            or "status" not in resp["data"]
            or resp["data"]["status"] != "success"
            or "reference" not in resp["data"]
            or resp["data"]["reference"] != request.json["reference"]
            or "amount" not in resp["data"]
            or resp["data"]["amount"]/100 != to_pay
            or "currency" not in resp["data"]
            or resp["data"]["currency"] != "NGN"
        ):
            db_close(con, cur)
            return jsonify({
                "status": 400,
                "error": "invalid transaction"
            })

    cur.execute("""
        UPDATE "user"
        SET account_balance = "user".account_balance - %s
        WHERE key = %s;
    """, (
        order["pay_account"],
        user["key"]
    ))

    cur.execute("""
        UPDATE "order"
        SET
            status = 'created',
            pay_user = %s,
            pay_reference = %s
        WHERE user_key = %s AND status = 'cart'
        RETURNING *;
    """, (
        to_pay,
        request.json['reference'] if request.json['reference'] else None,
        user["key"]
    ))
    order = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="created",
        entity_key=order["key"],
        entity_type="order",
        misc={
            "debit": order["pay_account"],
            "account_balance": user["account_balance"] + order["pay_account"],
            "new_balance": user["account_balance"]
        }
    )

    send_mail(
        os.environ["MAIL_USERNAME"],
        "New Order",
        request.json["email_template_admin"].format(
            order_key=order["key"]
        )
    )
    send_mail(
        user["email"],
        "Processing Order",
        request.json["email_template_user"].format(
            order_key=order["key"]
        )
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "order": order,
        "user": user_schema(user)
    })


@bp.get("/order")
def get_many():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    order_by = {
        'latest': 'log.date',
        'oldest': 'log.date',
        'low_cost': '"order".pay_account',
        'high_cost': '"order".pay_account'
    }

    order_dir = {
        'latest': 'DESC',
        'oldest': 'ASC',
        'low_cost': 'ASC',
        'high_cost': 'DESC'
    }

    order = list(order_by.keys())[0]
    status = "created"
    search = ""
    page_no = 1
    page_size = 24

    if "status" in request.args:
        status = request.args["status"]
    if "search" in request.args:
        search = request.args["search"].strip()
    if "page_no" in request.args:
        page_no = int(request.args["page_no"])
    if "size" in request.args:
        page_size = int(request.args["size"])
    if "order" in request.args:
        order = request.args["order"]

    cur.execute("""
        SELECT
            "order".*,
            ARRAY(
                SELECT JSON_BUILD_OBJECT(
                    'name', item.name,
                    'variation', order_item.variation,
                    'quantity', order_item.quantity
                )
                FROM order_item
                LEFT JOIN item ON order_item.item_key = item.key
                WHERE order_item.order_key = "order".key
            ) AS items,
            COUNT(*) OVER() AS total_items
        FROM "order"
        LEFT JOIN log ON "order".key = log.entity_key
        WHERE
            (%s = 'all' OR "order".status = %s)
            AND "order".status != 'cart'
            AND (%s IS NULL OR "order".key ILIKE %s)
            AND ("order".user_key = %s OR %s)
            AND log.action = 'created'
            AND log.entity_type = 'order'
        ORDER BY {} {}
        LIMIT %s OFFSET %s;
    """.format(
        order_by[order], order_dir[order]
    ), (
        status, status,
        search, f"%{search}%",
        user["key"],
        "admin" in request.args and "order:view" not in user["permissions"],
        page_size, (page_no - 1) * page_size
    ))
    orders = cur.fetchall()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "orders": orders,
        "order_by": list(order_by.keys()),
        "order_status": order_status,
        "total_page": ceil(
            orders[0]["total_items"] / page_size) if orders else 0
    })


@bp.get("/order/<key>")
def get(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    cur.execute("""
        SELECT *
        FROM "order"
        WHERE key = %s AND status != 'cart';
    """, (key,))
    order = cur.fetchone()

    cur.execute("""
        SELECT
            item.key AS key,
            item.slug AS slug,
            item.name AS name,
            item.price AS price,
            COALESCE(item.photos[1], NULL) AS photo,
            order_item.variation AS variation,
            order_item.quantity AS quantity
        FROM item
        LEFT JOIN order_item ON item.key = order_item.item_key
        WHERE order_item.order_key = %s;
    """, (order["key"],))
    items = cur.fetchall()

    if (
        not order
        or items == []
        or (
            order["user_key"] != user["key"]
            and "order:view" not in user["permissions"]
        )
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    for x in items:
        x["photo"] = f"{request.host_url}photo/{x['photo']}"

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "order": order,
        "items": items,
        "order_status": order_status
    })


@bp.put("/order/eta/<key>")
def date(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "order:edit_eta" not in user["permissions"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute("""SELECT * FROM "order" WHERE key = %s;""", (key,))
    order = cur.fetchone()

    if not order:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

# TODO: make sure delivery_date is datetime
    if (
        "delivery_date" not in request.json
        or not request.json["delivery_date"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "this field is required"
        })

    log(
        cur=cur,
        user_key=user["key"],
        action="changed_date",
        entity_key=order["key"],
        entity_type="order",
        misc={
            "from": f"{order['delivery_date']}",
            "to": request.json['delivery_date']
        }
    )

    cur.execute("""
        UPDATE "order"
        SET delivery_date = %s
        WHERE key = %s
        RETURNING *;
    """, (
        request.json['delivery_date'],
        order["key"]
    ))
    order = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "order": order
    })


@bp.put("/order/status/<key>")
def status(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "order:status" not in user["permissions"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute("""SELECT * FROM "order" WHERE key = %s;""", (key,))
    order = cur.fetchone()

    if order and order["user_key"] == user["key"]:
        order_user = user
    else:
        cur.execute("""SELECT * FROM "user" WHERE key = %s;""",
                    (order["user_key"],))
        order_user = cur.fetchone()

    if (
        not order or not order_user
        or "status" not in request.json
        or not request.json["status"]
        or request.json["status"] not in order_status[:-1]
        or "email_template" not in request.json
        or order["status"] in ["delivered", "canceled"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    i = order_status.index(order["status"])
    j = order_status.index(request.json["status"])
    if i + 1 != j and i - 1 != j:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if "note" not in request.json or not request.json["note"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "note": "this field is required"
        })

    if (
        (
            not order["delivery_date"]
            and order["status"] == "created"
        ) or (
            order["status"] == "processing"
            and request.json['status'] == "created"
        )
    ):
        new_date = None
        if not order["delivery_date"]:
            new_date = datetime.now() + timedelta(days=4)
            new_date = new_date.replace(
                hour=10, minute=0, second=0, microsecond=0)

        log(
            cur=cur,
            user_key=user["key"],
            action="changed_date",
            entity_key=order["key"],
            entity_type="order",
            misc={
                "from": order["delivery_date"],
                "to": new_date
            }
        )

        cur.execute("""
            UPDATE "order"
            SET delivery_date = %s
            WHERE key = %s;
        """, (
            new_date,
            order["key"]
        ))

    log(
        cur=cur,
        user_key=user["key"],
        action="changed_status",
        entity_key=order["key"],
        entity_type="order",
        misc={
            "from": order['status'],
            "to": request.json['status'],
            "note": request.json["note"]
        }
    )

    cur.execute("""
        UPDATE "order"
        SET status = %s
        WHERE key = %s
        RETURNING *;
    """, (
        request.json["status"],
        order["key"]
    ))
    order = cur.fetchone()

    if request.json["status"] == "delivered":
        send_mail(
            order_user["email"],
            "Order Delivered - Thank you",
            request.json["email_template"].format(
                name=order_user["name"]
            )
        )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "order": order
    })


@bp.put("/order/cancel/<key>")
def cancel(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    cur.execute("""SELECT * FROM "order" WHERE key = %s;""", (key,))
    order = cur.fetchone()
    cur.execute("""SELECT * FROM "user" WHERE key = %s;""",
                (order["user_key"],))
    order_user = cur.fetchone()

    if (
        "order:cancel" not in user["permissions"]
        and user["key"] != order_user["key"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    if (
        not order or not order_user
        or order["status"] in ["delivered", "canceled"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if (
        "note" not in request.json
        or not request.json["note"]
        or "email_template_admin" not in request.json
        or not request.json["email_template_admin"]
        or "email_template_user" not in request.json
        or not request.json["email_template_user"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "note": "this field is required"
        })

    log(
        cur=cur,
        user_key=user["key"],
        action="canceled",
        entity_key=order["key"],
        entity_type="order",
        misc={
            "from": order['status'],
            "to": "canceled",
            "note": request.json["note"]
        }
    )

    cur.execute("""
        UPDATE "order"
        SET status = 'canceled'
        WHERE key = %s
        RETURNING *;
    """, (key))
    order = cur.fetchone()

    send_mail(
        os.environ["MAIL_USERNAME"],
        "Cancelled Order",
        request.json["email_template_admin"]
    )
    send_mail(
        user["email"],
        "Cancelled Order",
        request.json["email_template_user"].format(
            user_name=order_user["name"]
        )
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "order": order
    })
