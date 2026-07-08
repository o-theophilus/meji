from math import ceil

from flask import Blueprint, request

from ..coupon.get import coupon_schema
from ..tools import session

bp = Blueprint("order_get", __name__)


order_status = ['created', 'processing', 'enroute',
                'delivered',
                'canceled', 'returning', 'returned']


@bp.get("/orders/<key>")
@session(False)
def get(cur, _user, key):
    cur.execute("""
        SELECT * FROM "order" WHERE key = %s;
    """, (key,))
    order = cur.fetchone()
    if not order:
        return {
            "status": 404,
            "error": "Oops! The order you're looking for doesn't exist"
        }, 404

    if (
        order["user_key"] != session["user"]["key"]
        and "order.view" not in session["user"]["access"]
    ):
        return {
            "status": 403,
            "error": "unauthorized access"
        }, 403

    cur.execute("""
        SELECT
            v.key, v.slug, v.name, v.price, v.status,
            COALESCE(v.files[1], NULL) as photo,
            order_item.variation, order_item.quantity,
            CASE
                WHEN v.status = v.status
                AND v.slug = v.slug
                AND v.name = v.name
                AND v.price = v.price
                AND v.information = v.information
                AND v.specification = v.specification
                AND v.files = v.files
                AND v.variation = v.variation
                THEN false
                ELSE true
            END AS changed
        FROM order_item
        LEFT JOIN item_version v ON order_item.item_version_key = v.key
        LEFT JOIN item i ON v.item_key = i.key
        WHERE order_item.order_key = %s
        ORDER BY order_item.date_created DESC
    ;""", (order["key"], ))
    items = cur.fetchall()

    cur.execute("""
        SELECT * FROM coupon WHERE order_key = %s;
    """, (order["key"],))
    coupon = cur.fetchone()

    return {
        "status": 200,
        "order": order,
        "items": items,
        "coupon": coupon_schema(coupon) if coupon else None
    }, 200


@bp.get("/orders")
@session(True)
def many(cur, user):
    order_by = {
        'latest': 'o.date_created',
        'oldest': 'o.date_created',
        'cost items ▼': 'o.order_cost',
        'cost items ▲': 'o.order_cost',
        'cost delivery ▼': 'o.delivery_cost',
        'cost delivery ▲': 'o.delivery_cost',
        'pay user ▼': 'o.payment',
        'pay user ▲': 'o.payment',
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

    searchParams = {
        "search": "",
        "status": "created",
        "view": "me",
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
    page_size = min(page_size, 100)

    user_key = user["key"]
    if view == "all" and "order.view" in user["access"]:
        user_key = ""

    cur.execute(f"""
        SELECT
            o.*,
            u.name,
            u.username,
            COUNT(order_item.*) AS item_count,
            COUNT(*) OVER() AS _count
        FROM "order" o
        LEFT JOIN "user" u ON o.user_key = u.key
        LEFT JOIN order_item ON o.key = order_item.order_key
        LEFT JOIN item_version item ON order_item.item_key = item.key
        WHERE (%s = 'all' OR o.status = %s)
        AND o.status != 'cart'
        AND (%s = '' OR o.user_key::TEXT = %s)
        AND (%s = '' OR o.key::TEXT ILIKE %s)
        GROUP BY
            o.key,
            u.key
        ORDER BY {order_by[order]} {order_dir[order]}, o.key DESC
        LIMIT %s OFFSET %s;
    """, (
        status, status,
        user_key, user_key,
        search, f"%{search}%",
        page_size, (page_no - 1) * page_size
    ))
    orders = cur.fetchall()

    return {
        "status": 200,
        "orders": orders,
        "total_page": ceil(orders[0]["_count"] / page_size) if orders else 0,
        "order_by": list(order_by.keys()),
        "searchParams": searchParams,
        "_status": order_status,
        "view": ['me', 'all'],
    }, 200
