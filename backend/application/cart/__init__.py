from flask import Blueprint, jsonify, request
from ..tools import get_session
from ..postgres import db_open, db_close
from psycopg2.extras import Json
from ..log import log
import re
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
    operation = request.json.get("operation", "replace")

    cur.execute("""SELECT * FROM item WHERE key = %s;""", (item_key,))
    item = cur.fetchone()

    if (
        not item
        or type(variation) is not dict
        or operation not in ["add", "replace"]
    ):
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
    if error != {}:
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

    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
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
        SELECT * FROM order_item
        WHERE order_key = %s AND item_key = %s AND variation = %s;
    """, (cart["key"], item_key, Json(variation)))
    order_item = cur.fetchone()

    if order_item:
        cur.execute("""
            UPDATE order_item SET quantity = %s WHERE key = %s
            RETURNING *
        ;""", (
            order_item["quantity"] +
            quantity if operation == "add" else quantity,
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
        entity_key=cart["key"],
        entity_type="cart",
        misc={
            "key": order_item["item_key"],
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
            entity_key=cart["key"],
            entity_type="cart",
            misc={
                "key": item_key,
                "variation": variation
            }
        )

    items = get_cart_items(cur)

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "items": items.json["items"]
    })


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

    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    # coordinates = [0, 1]

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

    log(
        cur=cur,
        user_key=user["key"],
        action="edited cart receiver",
        entity_key=cart["key"],
        entity_type="cart",
        misc={
            "from": cart["receiver"],
            "to": receiver
        }
    )

    cur.execute("""
        UPDATE "order" SET receiver = %s WHERE key = %s RETURNING *;
    """, (Json(receiver), cart["key"]))
    cart = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "cart": cart
    })


@bp.post("/cart/receiver_clear")
def receiver_clear():
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

    log(
        cur=cur,
        user_key=user["key"],
        action="edited cart receiver",
        entity_key=cart["key"],
        entity_type="cart",
        misc={
            "from": cart["receiver"],
            "to": {}
        }
    )

    cur.execute("""
        UPDATE "order" SET receiver = %s WHERE key = %s RETURNING *;
    """, (Json({}), cart["key"]))
    cart = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "cart": cart
    })


@bp.put("/cart/coupon")
def coupon():
    # FEATURE: coupon
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

    cur.execute("""
       SELECT
            SUM(item.price * order_item.quantity) AS total
        FROM item
        LEFT JOIN order_item ON item.key = order_item.item_key
        WHERE
            order_item.order_key = %s
            AND item.status = 'live';
    """, (cart["key"],))
    cost_items = cur.fetchone()[0]

    error = None
    if "amount" not in request.json:
        error = "invalid request"
    elif (
        type(request.json["amount"]) not in [int, float]
        or request.json["amount"] < 0
    ):
        error = "Please enter a valid amount"
    elif request.json["amount"] > user["account_balance"]:
        error = "amount larger than available balance"
    elif request.json["amount"] > cost_items + cart["cost_delivery"]:
        error = "amount larger than total cost"
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "amount": error
        })

    log(
        cur=cur,
        user_key=user["key"],
        action="changed_amount",
        entity_key=cart["key"],
        entity_type="cart",
        misc={
            "from": cart["pay_account"],
            "to": request.json["amount"]
        }
    )

    cur.execute("""
        UPDATE "order"
        SET pay_account = %s
        WHERE key = %s
        RETURNING *;
    """, (
        request.json["amount"],
        cart["key"]
    ))
    cart = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "cart": cart
    })
