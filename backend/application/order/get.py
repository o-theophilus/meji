from flask import Blueprint, request, jsonify
from math import ceil
from ..tools import get_session
from ..postgres import db_close, db_open


bp = Blueprint("order_get", __name__)


order_status = ['created', 'processing', 'enroute', 'delivered',
                'canceled']


@bp.get("/order/<key>")
def get(key):
    con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)

    cur.execute("""
        SELECT * FROM "order" WHERE key = %s;
    """, (key,))
    order = cur.fetchone()
    if not order:
        db_close(con, cur)
        return jsonify({
            "status": 404,
            "error": "Oops! The order you're looking for doesn't exist"
        })

    if (
        order["user_key"] != session["user"]["key"]
        and "order:view" not in session["user"]["access"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    # TODO:do the full journey
    cur.execute("""
        SELECT
            item.key, item.slug, item.name, item.price, item.status,
            COALESCE(item.files[1], NULL) as photo,
            order_item.variation, order_item.quantity
        FROM order_item
        LEFT JOIN "order" ON "order".key = order_item.order_key
        --LEFT JOIN item ON order_item.item_key = item.key
        LEFT JOIN item_snap AS item ON order_item.item_key = item.item_key
        WHERE "order".key = %s
        ORDER BY order_item.date_created DESC
    ;""", (order["key"],))
    items = cur.fetchall()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "order": order,
        "items": items,
        "_status": order_status,
    })


@bp.get("/orders")
def get_many():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    order_by = {
        'latest': 'date_created',
        'oldest': 'date_created',
        'cost_items (hi)': 'cost_items',
        'cost_items (lo)': 'cost_items',
        'cost_delivery (hi)': 'cost_delivery',
        'cost_delivery (lo)': 'cost_delivery',
        'pay_user (hi)': 'pay_user',
        'pay_user (lo)': 'pay_user',
        'delivery_date (hi)': 'delivery_date',
        'delivery_date (lo)': 'delivery_date',
    }

    order_dir = {
        'latest': 'DESC',
        'oldest': 'ASC',
        'cost_items (hi)': 'DESC',
        'cost_items (lo)': 'ASC',
        'cost_delivery (hi)': 'DESC',
        'cost_delivery (lo)': 'ASC',
        'pay_user (hi)': 'DESC',
        'pay_user (lo)': 'ASC',
        'delivery_date (hi)': 'DESC',
        'delivery_date (lo)': 'ASC',
    }

    status = request.args.get("status", "created")
    view = request.args.get("view", "")
    search = request.args.get("search", "").strip()
    order = request.args.get("order", "latest")
    page_no = int(request.args.get("page_no", 1))
    page_size = int(request.args.get("page_size", 24))

    user_key = user["key"]
    if view == "all" and "order:view" in user["access"]:
        user_key = ""

    cur.execute("""
        SELECT *, COUNT(*) OVER() AS _count
        FROM "order"
        WHERE (%s = 'all' OR status = %s)
            AND (%s = '' OR user_key::TEXT = %s)
            AND (%s = '' OR CONCAT_WS(', ', key) ILIKE %s)
        ORDER BY {} {}
        LIMIT %s OFFSET %s;
    """.format(
        order_by[order], order_dir[order]
    ), (
        status, status,
        user_key, user_key,
        search, f"%{search}%",
        page_size, (page_no - 1) * page_size
    ))
    orders = cur.fetchall()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "orders": orders,
        "order_by": list(order_by.keys()),
        "_status": order_status,
        "total_page": ceil(orders[0]["_count"] / page_size) if orders else 0
    })
