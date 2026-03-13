import re

from flask import Blueprint, jsonify, request
from psycopg2.extras import Json

from ..coupon import coupon_schema
from ..log import log
from ..postgres import db_close, db_open
from ..tools import get_session
from .get import get_cart_items

bp = Blueprint("cart", __name__)


@bp.post("/cart")
def add_to_cart():
    con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    item_key = request.json.get("key")
    quantity = request.json.get("quantity", 1)
    variation = request.json.get("variation", {})

    cur.execute("""SELECT * FROM item WHERE key = %s;""", (item_key,))
    item = cur.fetchone()

    cur.execute("""
        SELECT * FROM "order"
        WHERE user_key = %s AND status = 'cart';
    """, (user["key"],))
    cart = cur.fetchone()

    if not item or not cart or type(variation) is not dict:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    error = {}
    if item["status"] != "active":
        error["error"] = "This item is not currently available"
    elif item["quantity"] == 0:
        error["error"] = "Sorry, this item is currently out of stock"
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

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
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

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

    log(
        cur=cur,
        user_key=user["key"],
        action="added item to cart",
        entity_type="cart",
        entity_key=cart["key"],
        misc={
            "entity_type": "item",
            "entity_key": order_item["item_key"],
            "variation": order_item["variation"],
            "quantity": order_item["quantity"]
        }
    )

    items = get_cart_items(cur)

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "items": items.json["items"]
    })


@bp.delete("/cart")
def remove_from_cart():
    con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    item_key = request.json.get("key")
    variation = request.json.get("variation", {})

    if not item_key or type(variation) is not dict:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute("""
        SELECT * FROM "order"
        WHERE user_key = %s AND status = 'cart';
    """, (user["key"],))
    cart = cur.fetchone()
    if not cart:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("""
        DELETE FROM order_item
        WHERE order_key = %s AND item_key = %s AND variation = %s
        RETURNING *
    ;""", (cart["key"], item_key, Json(variation)))
    if cur.fetchone():
        log(
            cur=cur,
            user_key=user["key"],
            action="removed item from cart",
            entity_type="cart",
            entity_key=cart["key"],
            misc={
                "entity_type": "item",
                "entity_key": item_key,
                "variation": variation
            }
        )

    items = get_cart_items(cur)

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "items": items.json["items"]
    })


@bp.post("/cart/quantity")
def quantity():
    con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    item_key = request.json.get("key")
    quantity = request.json.get("quantity", 1)
    variation = request.json.get("variation", {})

    cur.execute("""SELECT * FROM item WHERE key = %s;""", (item_key,))
    item = cur.fetchone()

    cur.execute("""
        SELECT * FROM "order"
        WHERE user_key = %s AND status = 'cart';
    """, (user["key"],))
    cart = cur.fetchone()

    cur.execute("""
        SELECT * FROM order_item
        WHERE order_key = %s AND item_key = %s AND variation = %s;
    """, (cart["key"], item["key"], Json(variation)))
    order_item = cur.fetchone()

    if not item or not cart or not order_item or type(variation) is not dict:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    error = None
    if item["status"] != "active":
        error = "This item is not currently available"
    elif item["quantity"] == 0:
        error = "Sorry, this item is currently out of stock"
    elif not isinstance(quantity, int) or quantity < 1:
        error = "Please enter a valid number"
    elif quantity > item["quantity"]:
        s = "s" if item['quantity'] > 1 else ""
        error = f"Only {item['quantity']} item{s} available in stock"
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": error
        })

    cur.execute("""
        UPDATE order_item SET quantity = %s WHERE key = %s
    ;""", (quantity, order_item["key"]))

    log(
        cur=cur,
        user_key=user["key"],
        action="updated cart item quantity",
        entity_type="cart",
        entity_key=cart["key"],
        misc={
            "entity_type": "item",
            "entity_key": order_item["item_key"],
            "variation": order_item["variation"],
            "from_quantity": order_item["quantity"],
            "to_quantity": quantity
        }
    )

    items = get_cart_items(cur)

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "items": items.json["items"]
    })


@bp.delete("/cart/receiver")
@bp.post("/cart/receiver")
def receiver():
    con, cur = db_open()

    session = get_session(cur, True)
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
            "status": 400,
            "error": "invalid request"
        })

    if request.method == "POST":
        error = {}
        name = ' '.join(request.json.get("name", "").strip().split())
        phone = request.json.get("phone", "").replace(" ", "")
        email = request.json.get("email", "").strip()
        address = request.json.get("address")
        state = request.json.get("state")
        country = request.json.get("country")
        postal_code = request.json.get("postal_code")

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

        if not state:
            error["state"] = "This field is required"
        elif len(state) > 20:
            error["state"] = "This field cannot exceed 20 characters"

        if not country:
            error["country"] = "This field is required"
        elif len(country) > 20:
            error["country"] = "This field cannot exceed 20 characters"

        if postal_code and len(postal_code) > 10:
            error["postal_code"] = "This field cannot exceed 10 characters"

        if error:
            db_close(con, cur)
            return jsonify({
                "status": 400,
                **error
            })

        receiver = {
            "name": name,
            "phone": phone,
            "email": email,
            "address": {
                "address": address,
                "state": state,
                "country": country,
                "postal_code": postal_code
            }
        }

        delivery_cost = 1500
    else:
        receiver = {}
        delivery_cost = 0

    log(
        cur=cur,
        user_key=user["key"],
        action="edited cart receiver",
        entity_type="cart",
        entity_key=cart["key"],
        misc={
            "from": cart["receiver"],
            "to": receiver
        }
    )

    cur.execute("""
        UPDATE "order" SET receiver = %s, delivery_cost = %s
        WHERE key = %s RETURNING *;
    """, (Json(receiver), delivery_cost, cart["key"]))
    cart = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "cart": cart
    })


@bp.post("/cart/coupon")
def add_coupon():
    con, cur = db_open()

    session = get_session(cur, True)
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
            "status": 400,
            "error": "invalid request"
        })

    code = request.json.get("code", "").strip()

    error = None
    coupon = None
    if not code:
        error = "This field is required"
    elif len(code) != 10:
        error = "This must be 10 characters"
    if not error:
        cur.execute(
            'SELECT * FROM coupon WHERE LOWER(code) = %s;',
            (code.lower(),))
        coupon = cur.fetchone()
        if not coupon:
            error = "Invalid coupon code"
        elif coupon["status"] == "inactive":
            error = "this coupon is inactive"
        elif coupon["status"] == "used":
            error = "This coupon has been used"
        elif coupon["status"] == "expired":
            error = "This coupon has expired"
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "code": error
        })

    cur.execute("""
        UPDATE coupon SET order_key = %s WHERE key = %s
        RETURNING *;
    """, (cart["key"], coupon["key"]))
    coupon = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="added coupon to cart",
        entity_type="cart",
        entity_key=cart["key"],
        misc={
            "entity_type": "coupon",
            "entity_key": coupon["key"]
        }
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "coupon": coupon_schema(coupon, user["access"])
    })


@bp.delete("/cart/coupon")
def remove_coupon():
    con, cur = db_open()

    session = get_session(cur, True)
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
            "status": 400,
            "error": "invalid request"
        })

    cur.execute(
        'SELECT * FROM coupon WHERE order_key = %s;',
        (cart["key"],))
    coupon = cur.fetchone()
    if not coupon:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("""
        UPDATE coupon SET order_key = NULL WHERE key = %s;
    """, (coupon["key"],))

    log(
        cur=cur,
        user_key=user["key"],
        action="removed coupon from cart",
        entity_type="cart",
        entity_key=cart["key"],
        misc={
            "entity_type": "coupon",
            "entity_key": coupon["key"]
        }
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "coupon": None
    })
