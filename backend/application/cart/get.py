from flask import Blueprint, jsonify, request
from ..tools import get_session
from ..postgres import db_open, db_close


bp = Blueprint("cart_get_items", __name__)


@bp.get("/cart")
def get_cart_items(cur=None):
    close_conn = not cur
    if not cur:
        con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        if close_conn:
            db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute("""
        SELECT * FROM "order"
        WHERE user_key = %s AND status = 'cart';
    """, (user["key"],))
    cart = cur.fetchone()
    if not cart:
        cur.execute("""
            INSERT INTO "order" (user_key) VALUES (%s) RETURNING *
        ;""", (user["key"],))
        cart = cur.fetchone()

    cur.execute("""
        SELECT
            item.key, item.slug, item.name, item.price, item.status,
            item.quantity AS available_quantity,
            COALESCE(item.files[1], NULL) as photo,
            order_item.variation, order_item.quantity
        FROM order_item
        LEFT JOIN "order" ON "order".key = order_item.order_key
        LEFT JOIN item ON order_item.item_key = item.key
        WHERE "order".key = %s
        ORDER BY order_item.date_created DESC
    ;""", (cart["key"],))
    items = cur.fetchall()

    for x in items:
        x["photo"] = f"{request.host_url}photo/item/{x['photo']}" if x[
            "photo"] else None

    if close_conn:
        db_close(con, cur)
    return jsonify({
        "status": 200,
        "cart": cart,
        "items": items
    })


# TODO: previous_receivers
@bp.get("/cart/previous_receivers")
def previous_receivers():
    con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute("""
        SELECT DISTINCT ON (o.receiver)
            o.receiver,
            MAX(log.date) as last_delivered
        FROM "order" o
        LEFT JOIN log
            ON o.key = log.entity_key
            AND log.entity_type = 'order'
            AND log.action = 'changed_status'
            AND (log.misc->>'to') = 'delivered'
        WHERE
            o.user_key = %s
            AND o.status = 'delivered'
            AND o.receiver IS NOT NULL
        GROUP BY o.receiver
        ORDER BY o.receiver, last_delivered DESC
        LIMIT 5;
    """, (user["key"],))
    items = cur.fetchall()
    items = [x['receiver'] for x in items]

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "items": items
    })
