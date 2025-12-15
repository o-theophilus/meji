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
        SELECT * FROM "order" WHERE user_key = %s AND status = 'cart';
    """, (user["key"],))
    if not cur.fetchone():
        cur.execute("""
            INSERT INTO "order" (user_key) VALUES (%s);
        """, (user["key"],))

    cur.execute("""
        SELECT
            item.key, item.slug, item.name, item.price, item.status,
            COALESCE(item.files[1], NULL) as photo,
            order_item.variation, order_item.quantity
        FROM "order"
        LEFT JOIN order_item ON "order".key = order_item.order_key
        LEFT JOIN item ON order_item.item_key = item.key
        WHERE "order".user_key = %s AND "order".status = 'cart'
        ORDER BY order_item.date_created DESC
    ;""", (user["key"],))
    cart_items = cur.fetchall()

    for x in cart_items:
        print(x["photo"])
        x["photo"] = f"{request.host_url}file/{x['photo']}" if x[
            "photo"] else None
        print(x["photo"])

    if close_conn:
        db_close(con, cur)
    return jsonify({
        "status": 200,
        "cart_items": cart_items
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
