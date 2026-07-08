from flask import Blueprint, request

from ..coupon.get import coupon_schema
from ..tools import session
from .delivery import get_areas

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


def cart_items(cur, user_key):
    cur.execute("""
        SELECT * FROM "order"
        WHERE user_key = %s AND status = 'cart';
    """, (user_key,))
    cart = cur.fetchone()
    if not cart:
        cur.execute("""
            INSERT INTO "order" (user_key) VALUES (%s) RETURNING *
        ;""", (user_key,))
        cart = cur.fetchone()

    cur.execute("""
        SELECT
            item.key, item.slug, item.name, item.price, item.status,
            item.quantity AS available_quantity,
            COALESCE(item.files[1], NULL) as photo,
            order_item.variation, order_item.quantity,
            item.metadata
        FROM order_item
        LEFT JOIN item ON order_item.item_key = item.key
        WHERE order_item.order_key = %s
        ORDER BY order_item.date_created DESC
    ;""", (cart["key"],))
    items = cur.fetchall()

    for x in items:
        if "address" in x["metadata"]:
            del x["metadata"]["address"]

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
    """, (user_key,))
    previous_receivers = cur.fetchall()
    previous_receivers = [x['receiver'] for x in previous_receivers]

    cur.execute("""
        SELECT * FROM coupon WHERE order_key = %s;
    """, (cart["key"],))
    coupon = cur.fetchone()

    return {
        "status": 200,
        "cart": cart,
        "items": items,
        "previous_receivers": previous_receivers,
        "areas": get_areas(),
        "coupon": coupon_schema(coupon) if coupon else None
    }


@bp.get("/cart")
@session(False)
def _get_cart_items(cur, user):
    return cart_items(cur, user["key"]), 200
