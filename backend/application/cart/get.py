from flask import Blueprint, jsonify, request

from ..coupon.get import coupon_schema
from ..postgres import db_close, db_open
from ..tools import get_session
from .delivery import get_areas, get_delivery_price

bp = Blueprint("cart_get_items", __name__)


def has_adderss(x):
    if (
        "name" not in x
        or not x["name"]
        or "phone" not in x
        or not x["phone"]
        or "email" not in x
        or not x["email"]
        or "address" not in x
        or x["address"] == {}
        or "address" not in x["address"]
        or not x["address"]["address"]
        or "area" not in x["address"]
        or x["address"]["area"] not in get_areas()
        or "state" not in x["address"]
        or not x["address"]["state"]
        or "country" not in x["address"]
        or not x["address"]["country"]
    ):
        return False
    return True


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
            order_item.variation, order_item.quantity,
            item.package
        FROM order_item
        LEFT JOIN "order" ON "order".key = order_item.order_key
        LEFT JOIN item ON order_item.item_key = item.key
        WHERE "order".key = %s
        ORDER BY order_item.date_created DESC
    ;""", (cart["key"],))
    items = cur.fetchall()

    delivery_cost = 0
    if has_adderss(cart["receiver"]) and items:
        delivery_cost = get_delivery_price(
            items, cart["receiver"]["address"]["area"])
    cur.execute("""
        UPDATE "order" SET delivery_cost = %s
        WHERE key = %s RETURNING *;
    """, (delivery_cost, cart["key"]))
    cart = cur.fetchone()

    for x in items:
        del x["package"]
        x["photo"] = f"{request.host_url}photo/item/{x['photo']}" if x[
            "photo"] else None

    cur.execute("""
        SELECT DISTINCT ON (o.receiver::jsonb)
            o.receiver,
            (o.timeline->>'delivered')::timestamptz AS last_delivered
        FROM "order" o
        WHERE o.user_key = %s
        AND o.status = 'delivered'
        ORDER BY
            o.receiver::jsonb,
            (o.timeline->>'delivered')::timestamptz DESC
        LIMIT 5;
    """, (user["key"],))
    previous_receivers = cur.fetchall()
    previous_receivers = [x['receiver'] for x in previous_receivers]

    cur.execute("""
        SELECT * FROM coupon WHERE order_key = %s;
    """, (cart["key"],))
    coupon = cur.fetchone()

    if close_conn:
        db_close(con, cur)
    return jsonify({
        "status": 200,
        "cart": cart,
        "items": items,
        "previous_receivers": previous_receivers,
        "areas": get_areas(),
        "coupon": coupon_schema(coupon) if coupon else None
    })
