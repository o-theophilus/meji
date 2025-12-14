from flask import Blueprint, jsonify, request
from ..tools import get_session
from ..postgres import db_open, db_close


bp = Blueprint("cart_get", __name__)


@bp.get("/cart")
def get():
    con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute("""
        SELECT * FROM "order"
        WHERE user_key = %s AND status = 'cart';
    """, (user["key"],))
    cart = cur.fetchone()

    if not cart:
        db_close(con, cur)
        return jsonify({
            "status": 200,
            "cart": None,
            "items": []
        })

    cur.execute("""
        SELECT
            item.key,
            item.slug,
            item.name,
            item.price,
            item.status,
            COALESCE(item.photos[1], NULL) AS photo,
            order_item.variation,
            order_item.quantity
        FROM item
        LEFT JOIN order_item ON item.key = order_item.item_key
        WHERE order_item.order_key = %s;
    """, (cart["key"],))
    items = cur.fetchall()

    cost_items = 0
    for x in items:
        cost_items += x["price"] * x["quantity"]
        x["photo"] = f"{request.host_url}photo/{x['photo']}"

    if (
        cart["pay_account"] > user["account_balance"]
        or cart["pay_account"] > cost_items
    ):
        cur.execute("""
            UPDATE "order"
            SET pay_account = 0
            WHERE key = %s
            RETURNING *;
        """, (cart["key"],))
        cart = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "cart": cart,
        "items": items
    })


@bp.get("/cart/previous_receivers")
def previous_receivers():
    con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute("""
        SELECT
            DISTINCT ON (
                o.name, o.phone, o.line, o.country,
                o.state, o.local_area, o.postal_code
            )
            o.name, o.phone, o.line, o.country,
            o.state, o.local_area, o.postal_code,
            log.date
        FROM "order" o
        LEFT JOIN log ON o.key = log.entity_key
        WHERE
            o.user_key = %s
            AND o.status = 'delivered'
            AND log.entity_type = 'order'
            AND log.action = 'changed_status'
            AND (log.misc->>'to') = 'delivered'
        ORDER BY o.name, o.phone, o.line, o.country,
                o.state, o.local_area, o.postal_code, log.date DESC
        LIMIT 5;
    """, (user["key"],))
    prev = cur.fetchall()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "prev": prev
    })
