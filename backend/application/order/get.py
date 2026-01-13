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

    cur.execute("""
        SELECT
            item.key, item.slug, item.name, item.price, item.status,
            COALESCE(item.files[1], NULL) as photo,
            order_item.variation, order_item.quantity
        FROM order_item
        LEFT JOIN "order" ON "order".key = order_item.order_key
        LEFT JOIN item ON order_item.item_key = item.key
        WHERE "order".key = %s
        ORDER BY order_item.date_created DESC
    ;""", (order["key"],))
    items = cur.fetchall()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "order": order,
        "items": items
    })


@bp.get("/orders")
def get_many():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)

    # if "user:view" not in session["user"]["access"]:
    #     db_close(con, cur)
    #     return jsonify({
    #         "status": 400,
    #         "error": "unauthorized access"
    #     })

    order_by = {
        'latest': 'date_created',
        'oldest': 'date_created',
        # 'name (a-z)': 'name',
        # 'name (z-a)': 'name'
    }

    order_dir = {
        'latest': 'DESC',
        'oldest': 'ASC',
        'name (a-z)': 'ASC',
        'name (z-a)': 'DESC'
    }

    status = request.args.get("status", "created")
    search = request.args.get("search", "").strip()
    order = request.args.get("order", "latest")
    page_no = int(request.args.get("page_no", 1))
    page_size = int(request.args.get("size", 24))

    cur.execute("""
        SELECT *, COUNT(*) OVER() AS _count
        FROM "order"
        WHERE (%s = 'all' OR status = %s)
            AND (%s = '' OR CONCAT_WS(', ', key) ILIKE %s)
        ORDER BY {} {}
        LIMIT %s OFFSET %s;
    """.format(
        order_by[order], order_dir[order]
    ), (
        status, status,
        search, f"%{search}%",
        page_size, (page_no - 1) * page_size
    ))
    items = cur.fetchall()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "items": items,
        "order_by": list(order_by.keys()),
        "_status": order_status,
        "total_page": ceil(items[0]["_count"] / page_size) if items else 0
    })
