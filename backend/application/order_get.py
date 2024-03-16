from flask import Blueprint, jsonify, request
from .tools import token_to_user
from .schema import order_schema
from .log import log_template
from uuid import uuid4
from math import ceil
from .postgres import db_close, db_open
from datetime import datetime

bp = Blueprint("order_get", __name__)


@bp.get("/orders")
def get():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    status = request.args["status"] if "status" in request.args else "created"
    search = request.args["search"]
    page_no = int(request.args["page_no"]) if "page_no" in request.args else 1
    page_size = int(request.args["size"]) if "size" in request.args else 24
    sort_order = "DESC" if True else "ASC"
    sort_by = "date"

    cur.execute("""
        SELECT o.*, COUNT(*) OVER() AS total_items
        FROM (
            SELECT *
            FROM "order"
            WHERE status = %s
                AND status != "cart"
                AND (%s = '' OR CONCAT_WS(', ', key, name, email) ILIKE %s)
                AND (user_key = %s OR %s)
        ) AS o
        LEFT JOIN log ON o.key = log.user_key
            AND log.action = 'created'
            AND log.entity_type = 'order'
        ORDER BY
            CASE %s
                WHEN 'amount' THEN order.transaction_account_debit
                WHEN 'date' THEN log.date
                ELSE log.date
            END
            %s
        LIMIT %s OFFSET %s;
    """, (
        status,
        search, f"%{search}%",
        user["key"],
        "admin" in request.args and "order:view" not in user["roles"],
        sort_order, sort_by,
        page_size, (page_no - 1) * page_size
    ))
    orders = cur.fetchall()

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "orders": [order_schema(order) for order in orders],
        "total_page": ceil(orders[0][-1] / page_size) if orders else 0
    })


@bp.get("/order/<key>")
def get_one(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    cur.execute("""
        SELECT *,
        (
            SELECT ARRAY_AGG(ROW(
                item.slug,
                item.name,
                item.price,
                item.photos,
                order_item.variation,
                order_item.quantity
            )::jsonb)
            FROM order_item
            LEFT JOIN item ON order_item.item_key = item.key
            WHERE order_key = "order".key

        ) AS items
        FROM "order"
        WHERE key = %s AND status != 'cart';
    """, (key,))
    order = cur.fetchone()

    if (
        not order
        or (
            order["user_key"] != user["key"]
            and "order:view" not in user["roles"]
        )
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute(log_template, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "viewed",
        order["key"],
        "order",
        200,
        None
    ))

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "order": order_schema(order),
    })
