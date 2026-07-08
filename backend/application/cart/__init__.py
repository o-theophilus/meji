import re

from flask import Blueprint, request
from psycopg2.extras import Json

from ..coupon import coupon_schema
from ..tools import log, rate_limit, session
from .delivery import get_areas

bp = Blueprint("cart", __name__)


@bp.post("/cart")
@session(False)
@rate_limit(20, 1)
@log("cart")
def add(cur, user):
    cur.execute("""
        SELECT * FROM "order" WHERE user_key = %s AND status = 'cart';
    """, (user["key"],))
    cart = cur.fetchone()
    if not cart:
        return {
            "status": 404,
            "error": "Invalid request"
        }, 404

    item_key = request.json.get("key")
    quantity = request.json.get("quantity", 1)
    variation = request.json.get("variation", {})

    cur.execute("""SELECT * FROM item WHERE key = %s;""", (item_key,))
    item = cur.fetchone()
    if (
        not item
        or item["status"] != "active"
        or item["quantity"] == 0
    ):
        return {
            "status": 404,
            "error": "Invalid request"
        }, 404

    if type(variation) is not dict:
        return {
            "status": 422,
            "error": "Invalid request"
        }, 422

    error = {}
    if not isinstance(quantity, int) or quantity < 1:
        error["quantity"] = "Please enter a valid number"
    elif quantity > item["quantity"]:
        s = "s" if item['quantity'] > 1 else ""
        error["quantity"
              ] = f"Only {item['quantity']} item{s} available in stock"

    invalid_keys = [x for x in variation if x not in item["variation"]]
    for x in invalid_keys:
        del variation[x]

    for x, val in item["variation"].items():
        if x not in variation or variation[x] not in val:
            error[x] = f"Please select a {x}"

    if error:
        return {
            "status": 422,
            **error
        }, 422

    cur.execute("""
        SELECT * FROM order_item
        WHERE order_key = %s AND item_key = %s AND variation = %s;
    """, (cart["key"], item_key, Json(variation)))
    order_item = cur.fetchone()

    if order_item:
        cur.execute("""
            UPDATE order_item SET quantity = %s WHERE key = %s
            RETURNING *
        ;""", (
            order_item["quantity"] + quantity,
            order_item["key"]
        ))
    else:
        cur.execute("""
            INSERT INTO order_item (
                order_key, item_key, variation, quantity)
            VALUES (%s, %s, %s, %s)
            RETURNING *
        ;""", (cart["key"], item_key, Json(variation), quantity))
    order_item = cur.fetchone()

    # TODO: fix ths get in frontend
    # resp = get_cart_items(cur)

    return {
        "status": 200,
        "log": {
            "entity_key": cart["key"],
            "misc": {
                "entity_type": "item",
                "entity_key": order_item["item_key"],
                "variation": order_item["variation"],
                "quantity": order_item["quantity"]
            }
        }
    }, 200


@bp.delete("/cart")
@session(False)
@rate_limit(20, 1)
@log("cart")
def remove(cur, user):
    cur.execute("""
        SELECT * FROM "order" WHERE user_key = %s AND status = 'cart';
    """, (user["key"],))
    cart = cur.fetchone()
    if not cart:
        return {
            "status": 404,
            "error": "invalid request"
        }, 404

    item_key = request.json.get("key")
    variation = request.json.get("variation", {})

    if not item_key or type(variation) is not dict:
        return {
            "status": 422,
            "error": "Invalid request"
        }, 422

    cur.execute("""
        DELETE FROM order_item
        WHERE order_key = %s AND item_key = %s AND variation = %s
        RETURNING *
    ;""", (cart["key"], item_key, Json(variation)))
    if not cur.fetchone():
        return {
            "status": 404,
            "error": "invalid request"
        }, 404

    # TODO: fix ths get in frontend
    # resp = get_cart_items(cur)

    return {
        "status": 200,
        "log": {
            "entity_key": cart["key"],
            "misc": {
                "entity_type": "item",
                "entity_key": item_key,
                "variation": variation
            }
        }
    }, 200


@bp.post("/cart/quantity")
@session(False)
@rate_limit(20, 1)
@log("cart")
def quantity(cur, user):
    item_key = request.json.get("key")
    quantity = request.json.get("quantity", 1)
    variation = request.json.get("variation", {})

    cur.execute("""
        SELECT * FROM "order" WHERE user_key = %s AND status = 'cart';
    """, (user["key"],))
    cart = cur.fetchone()
    cur.execute("""SELECT * FROM item WHERE key = %s;""", (item_key,))
    item = cur.fetchone()
    cur.execute("""
        SELECT * FROM order_item
        WHERE order_key = %s AND item_key = %s AND variation = %s;
    """, (cart["key"], item_key, Json(variation)))
    order_item = cur.fetchone()
    if (
        not item
        or item["status"] != "active"
        or item["quantity"] == 0
        or not cart
        or not order_item
    ):
        return {
            "status": 404,
            "error": "Invalid request"
        }, 404

    if type(variation) is not dict:
        return {
            "status": 422,
            "error": "Invalid request"
        }, 422

    error = None
    if not isinstance(quantity, int) or quantity < 1:
        error = "Please enter a valid number"
    elif quantity > item["quantity"]:
        s = "s" if item['quantity'] > 1 else ""
        error = f"Only {item['quantity']} item{s} available in stock"
    if error:
        return {
            "status": 422,
            "error": error
        }, 422

    previous = order_item
    cur.execute("""
        UPDATE order_item SET quantity = %s WHERE key = %s
        RETURNING *
    ;""", (quantity, order_item["key"]))
    order_item = cur.fetchone()

    # TODO: fix ths get in frontend
    # resp = get_cart_items(cur)

    return {
        "status": 200,
        "log": {
            "entity_key": cart["key"],
            "misc": {
                "entity_type": "item",
                "entity_key": order_item["item_key"],
                "variation": order_item["variation"],
                "from_quantity": previous["quantity"],
                "to_quantity": order_item["quantity"],
            }
        }
    }, 200


@bp.delete("/cart/receiver")
@bp.post("/cart/receiver")
@session(False)
@rate_limit(20, 1)
@log("cart")
def receiver(cur, user):
    cur.execute("""
        SELECT * FROM "order" WHERE user_key = %s AND status = 'cart';
    """, (user["key"],))
    cart = cur.fetchone()
    if not cart:
        return {
            "status": 404,
            "error": "invalid request"
        }, 404

    if request.method == "POST":
        error = {}
        name = ' '.join(request.json.get("name", "").strip().split())
        phone = request.json.get("phone", "").replace(" ", "")
        email = request.json.get("email", "").strip()
        address = request.json.get("address")
        area = request.json.get("area")
        state = "Lagos"
        country = 'Nigeria'

        if not name:
            error["name"] = "This field is required"
        elif len(name) > 100:
            error["name"] = "This field cannot exceed 100 characters"

        if not name:
            error['phone'] = "This field is required"
        elif len(phone) > 20:
            error["phone"] = "This field cannot exceed 20 characters"

        if not email:
            error["email"] = "This field is required"
        elif not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
            error["email"] = "Invalid email address"
        elif len(email) > 255:
            error["email"] = "This field cannot exceed 255 characters"

        if not address:
            error["address"] = "This field is required"
        elif len(address) > 255:
            error["address"] = "This field cannot exceed 255 characters"

        if not area:
            error["area"] = "This field is required"
        elif area not in get_areas():
            error["area"] = "Invalid selection"

        if not state:
            error["state"] = "This field is required"
        elif len(state) > 20:
            error["state"] = "This field cannot exceed 20 characters"

        if not country:
            error["country"] = "This field is required"
        elif len(country) > 20:
            error["country"] = "This field cannot exceed 20 characters"

        if error:
            return {
                "status": 422,
                **error
            }, 422

        receiver = {
            "name": name,
            "phone": phone,
            "email": email,
            "address": {
                "address": address,
                "area": area,
                "state": state,
                "country": country,
            }
        }
    else:
        receiver = {}

    previous = cart
    cur.execute("""
        UPDATE "order" SET receiver = %s WHERE key = %s
        RETURNING *;
    """, (Json(receiver), cart["key"]))
    cart = cur.fetchone()

    # TODO: fix ths get in frontend
    # resp = get_cart_items(cur)

    return {
        "status": 200,
        "log": {
            "entity_key": cart["key"],
            "misc": {
                "from": previous["receiver"],
                "to": cart["receiver"],
            }
        }
    }, 200


@bp.post("/cart/coupon")
@session(False)
@rate_limit(20, 1)
@log("cart")
def add_coupon(cur, user):
    cur.execute("""
        SELECT * FROM "order" WHERE user_key = %s AND status = 'cart';
    """, (user["key"],))
    cart = cur.fetchone()
    if not cart:
        return {
            "status": 404,
            "error": "invalid request"
        }, 404

    code = request.json.get("code", "").strip()

    error = None
    if not code:
        error = "This field is required"
    elif len(code) != 10:
        error = "This must be 10 characters"
    if error:
        return {
            "status": 422,
            "code": error
        }, 422

    cur.execute(
        'SELECT * FROM coupon WHERE LOWER(code) = %s;',
        (code.lower(),))
    coupon = cur.fetchone()
    if not coupon:
        return {
            "status": 404,
            "code": "Invalid coupon code"
        }, 404

    if coupon["status"] == "inactive":
        error = "this coupon is inactive"
    elif coupon["status"] == "used":
        error = "This coupon has been used"
    elif coupon["status"] == "expired":
        error = "This coupon has expired"
    if error:
        return {
            "status": 422,
            "code": error
        }, 422

    cur.execute("""
        UPDATE coupon SET order_key = %s WHERE key = %s
        RETURNING *;
    """, (cart["key"], coupon["key"]))
    coupon = cur.fetchone()

    return {
        "status": 200,
        "coupon": coupon_schema(coupon),
        "log": {
            "entity_key": cart["key"],
            "misc": {
                "entity_type": "coupon",
                "entity_key": coupon["key"]
            }
        }
    }, 200


@bp.delete("/cart/coupon")
@session(False)
@rate_limit(20, 1)
@log("cart")
def remove_coupon(cur, user):
    cur.execute("""
        SELECT * FROM "order" WHERE user_key = %s AND status = 'cart';
    """, (user["key"],))
    cart = cur.fetchone()
    cur.execute(
        'SELECT * FROM coupon WHERE order_key = %s;',
        (cart["key"],))
    coupon = cur.fetchone()
    if not cart or not coupon:
        return {
            "status": 404,
            "error": "invalid request"
        }, 404

    cur.execute("""
        UPDATE coupon SET order_key = NULL WHERE key = %s;
    """, (coupon["key"],))

    return {
        "status": 200,
        "coupon": None,
        "log": {
            "entity_key": cart["key"],
            "misc": {
                "entity_type": "coupon",
                "entity_key": coupon["key"]
            }
        }
    }, 200
