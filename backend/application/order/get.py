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

    # FEATURE:do the full journey of item snapshot,
    # duplicate item on purchase
    # join item snapshot table on order view
    # get item snapshot on order item view
    # check if snapshot item is unchanged
    # if unchanged get the original item
    # if changed get the snapshot item
    #       then suggest to see the latest version
    cur.execute("""
        SELECT
            item.key, item.slug, item.name, item.price, item.status,
            COALESCE(item.files[1], NULL) as photo,
            order_item.variation, order_item.quantity
        FROM order_item
        LEFT JOIN "order" ON "order".key = order_item.order_key
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

    searchParams = {
        "search": "",
        "status": "created",
        "view": "",
        "order": "latest",
        "page_no": 1,
        "page_size": 24
    }
    search = request.args.get("search", searchParams["search"]).strip()
    status = request.args.get("status", searchParams["status"])
    view = request.args.get("view", searchParams["view"])
    order = request.args.get("order", searchParams["order"])
    page_no = int(request.args.get("page_no", searchParams["page_no"]))
    page_size = int(request.args.get("page_size", searchParams["page_size"]))

    order_by = {
        'latest': 'o.date_created',
        'oldest': 'o.date_created',
        'cost items ▼': 'o.cost_items',
        'cost items ▲': 'o.cost_items',
        'cost delivery ▼': 'o.cost_delivery',
        'cost delivery ▲': 'o.cost_delivery',
        'pay user ▼': 'o.pay_user',
        'pay user ▲': 'o.pay_user',
        'item count ▼': 'item_count',
        'item count ▲': 'item_count',
        'delivery date ▼': "o.timeline->>'delivery_date'",
        'delivery date ▲': "o.timeline->>'delivery_date'",
    }
    order_dir = {
        'latest': 'DESC',
        'oldest': 'ASC',
        'cost items ▼': 'DESC',
        'cost items ▲': 'ASC',
        'cost delivery ▼': 'DESC',
        'cost delivery ▲': 'ASC',
        'pay user ▼': 'DESC',
        'pay user ▲': 'ASC',
        'item count ▼': 'DESC',
        'item count ▲': 'ASC',
        'delivery date ▼': 'DESC',
        'delivery date ▲': 'ASC',
    }

    user_key = user["key"]
    if view == "all" and "order:view" in user["access"]:
        user_key = ""

    cur.execute(f"""
        SELECT
            o.*,
            u.name,
            u.username,
            COUNT(i.*) AS item_count,
            COUNT(*) OVER() AS _count
        FROM "order" o
        LEFT JOIN "user" u ON o.user_key = u.key
        LEFT JOIN item_snap i ON o.key = i.order_key
        WHERE (%s = 'all' OR o.status = %s)
        AND (%s = '' OR o.user_key::TEXT = %s)
        AND (%s = '' OR o.key::TEXT ILIKE %s)
        GROUP BY
            o.key,
            u.key
        ORDER BY {order_by[order]} {order_dir[order]}
        LIMIT %s OFFSET %s;
    """, (
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
        "total_page": ceil(orders[0]["_count"] / page_size) if orders else 0,
        "order_by": list(order_by.keys()),
        "searchParams": searchParams,
        "_status": order_status,
    })
