from flask import Blueprint, jsonify, request
from .tools import token_to_user, now, user_schema, item_schema
from uuid import uuid4
from .log import log_template
from .postgres import db_close, db_open
from datetime import datetime
import json

bp = Blueprint("cart", __name__)


@bp.post("/cart")
def add_to_cart():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if (
        "key" not in request.json
        or not request.json["key"]
        or "variation" not in request.json
        or "quantity" not in request.json
        or type(request.json["quantity"]) is not int
        or request.json["quantity"] < 0
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("""
        INSERT INTO "order" (key, version, user_key)
        SELECT (%s, %s, %s)
        WHERE NOT EXISTS (
            SELECT 1 FROM cart WHERE user_key = %s AND status = 'cart'
        )
        RETURNING *;
    """, (
        uuid4().hex,
        uuid4().hex,
        user["key"],
        user["key"]
    ))
    cart = cur.fetchone()

    cur.execute("""
        INSERT INTO order_item (order_key, item_key, variation, quantity)
        VALUES (%s, %s, %s, %s);
        ON CONFLICT (order_key, item_key, variation)
        DO UPDATE SET quantity = quantity + EXCLUDED.quantity
        RETURNING *;
    """, (
        user["key"],
        cart["key"],
        request.json["variation"],
        request.json["quantity"]
    ))

    cur.execute("""
        UPDATE "order"
        SET cost_items = (
            SELECT SUM(order_item.quantity * item.price)
            FROM order_item
            LEFT JOIN item ON order_item.item_key = item.key
            WHERE order_item.order_key = %s
        )
        WHERE key = %s;
    """, (
        cart["key"],
        cart["key"]
    ))

    cur.execute(log_template, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "added_to",
        cart["key"],
        "cart",
        200,
        json.dumps({
            "key": request.json["key"],
            **request.json["variation"],
            "quantity": request.json["quantity"]
        })
    ))

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })


@bp.get("/cart")
def get():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    cur.execute("""
        SELECT *,
            ARRAY(
                SELECT JSON_BUILD_OBJECT(
                    'slug', item.slug,
                    'name', item.name,
                    'price', item.price,
                    'photo', COALESCE(item.photos[1], NULL),
                    'variation', order_item.variation,
                    'quantity', order_item.quantity
                )
                FROM order_item
                LEFT JOIN item ON order_item.item_key = item.key
                WHERE order_item.order_key = "order".key
            ) AS items
        FROM "order"
        WHERE user_key = %s AND status = 'cart';
    """, (user["key"],))
    cart = cur.fetchone()

    pr = []
    items = []

    if cart:
        cart["delivery_date"] = f"{now(4).split('T')[0]}T10:00"

        cur.execute("""
            SELECT item.*, order_item.variation AS variation,
                order_item.quantity AS quantity
            FROM order_item
            LEFT JOIN item ON order_item.item_key = item.key
            WHERE order_item.order_key = %s;
        """, (cart["key"],))
        items = cur.fetchall()

        cur.execute("""
            SELECT DISTINCT
                o.receiver_name,
                o.receiver_phone,
                o.receiver_address_line,
                o.receiver_address_country,
                o.receiver_address_state,
                o.receiver_address_local_area,
                o.receiver_address_postal_code
            FROM (
                SELECT *
                FROM "order"
                WHERE user_key = %s AND status = "delivered"
            ) AS o
            LEFT JOIN log ON o.key = log.entity_key
                AND log.entity_type = 'order'
                AND log.action = 'delivered'
            ORDER BY log.date DESC
            LIMIT 5;
        """, (user["key"],))
        pr = cur.fetchone()

        cur.execute(log_template, (
            uuid4().hex,
            datetime.now(),
            user["key"],
            "viewed",
            cart["key"],
            "cart",
            200,
            None
        ))

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "cart": cart,
        "items": [item_schema(x) for x in items],
        "previous_receivers": pr
    })


@bp.put("/cart/quantity")
def quantity():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    cur.execute("""
        SELECT * FROM "order"
        WHERE user_key = %s AND status = "cart";
    """, (user["key"],))
    cart = cur.fetchone()

    cur.execute("""
        SELECT *
        FROM order_item
        WHERE order_key = %s
            AND item_key = %s
            AND variation = %s;
    """, (
        cart["key"],
        request.json["key"],
        request.json["variation"]
    ))
    cart_item = cur.fetchone()

    if (
        "key" not in request.json
        or not request.json["key"]
        or "variation" not in request.json
        or "quantity" not in request.json
        or type(request.json["quantity"]) is not int
        or request.json["quantity"] < 0
        or not cart
        or not cart_item
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("""
        UPDATE order_item
        SET quantity = %s
        WHERE key = %s;

        DELETE FROM order_item
        WHERE quantity = 0;
    """, (
        request.json["quantity"],
        cart_item["key"]
    ))

    cur.execute(log_template, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "changed_quantity" if request.json["quantity"
                                           ] > 0 else "removed_from",
        cart["key"],
        "cart",
        200,
        json.dumps({
            "key": request.json["key"],
            **request.json["variation"],
            "from_quantity": cart_item["quantity"],
            "to_quantity": request.json["quantity"]
        } if request.json["quantity"] > 0 else {
            "key": request.json["key"],
            **request.json["variation"]
        })
    ))

    cur.execute("""
        SELECT item.*, order_item.variation AS variation,
            order_item.quantity AS quantity
        FROM order_item
        LEFT JOIN item ON order_item.item_key = item.key
        WHERE order_item.order_key = %s;
    """, (cart["key"],))
    items = cur.fetchall()

    cart = []
    if items.length != 0:
        cur.execute("""
            UPDATE "order"
            SET cost_items = (
                SELECT SUM(order_item.quantity * item.price)
                FROM order_item
                LEFT JOIN item ON order_item.item_key = item.key
                WHERE order_item.order_key = %s
            )
            WHERE key = %s
            RETURNING *;
        """, (
            cart["key"],
            cart["key"]
        ))
        cart = cur.fetchone()
    else:
        cur.execute("DELETE FROM 'order'' WHERE key = %s;", (cart["key"],))

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "user": user_schema(user),
        "cart": cart,
        # TODO => user proper schema
        "items": [item_schema(x) for x in items]
    })


@bp.put("/cart/receiver")
def receiver():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    cur.execute("""
        SELECT * FROM "order"
        WHERE user_key = %s AND status = "cart";
    """, (user["key"],))
    cart = cur.fetchone()

    if not cart:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = {}
    if "name" not in request.json or not request.json["name"]:
        error["name"] = "this field is required"
    if "phone" not in request.json or not request.json["phone"]:
        error["phone"] = "this field is required"

    if "address" not in request.json or not request.json["address"]:
        error["line"] = "this field is required"
        error["state"] = "this field is required"
        error["country"] = "this field is required"
        error["postal_code"] = "this field is required"
    else:
        if (
            "line" not in request.json["address"]
            or not request.json["address"]["line"]
        ):
            error["address"] = "this field is required"
        if (
            "state" not in request.json["address"]
            or not request.json["address"]["state"]
        ):
            error["state"] = "this field is required"
        if (
            "country" not in request.json["address"]
            or not request.json["address"]["country"]
        ):
            error["country"] = "this field is required"
        if (
            "postal_code" not in request.json["address"]
            or not request.json["address"]["postal_code"]
        ):
            error["postal_code"] = "this field is required"

    if error != {}:
        return jsonify({
            "status": 400,
            **error
        })

    cur.execute(log_template, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "edited_receiver",
        cart["key"],
        "cart",
        200,
        json.dumps({
            "from": f"""
                {cart["receiver_name"]} |
                {cart["receiver_phone"]} |
                {cart["receiver_address_line"]} |
                {cart["receiver_address_country"]} |
                {cart["receiver_address_state"]} |
                {cart["receiver_address_local_area"]} |
                {cart["receiver_address_postal_code"]}
            """,
            "to": f"""
                {request.json["name"]} |
                {request.json["phone"]} |
                {request.json["address_line"]} |
                {request.json["address_state"]} |
                {request.json["address_country"]} |
                {request.json["address_local_area"]} |
                {request.json["address_postal_code"]}
            """
        })
    ))

    cur.execute("""
        UPDATE "order"
        SET
            receiver_name = %s,
            receiver_phone = %s,
            receiver_address_line = %s,
            receiver_address_country = %s,
            receiver_address_state = %s,
            receiver_address_local_area = %s,
            receiver_address_postal_code = %s
        WHERE key = %s;
        RETURNING *
    """, (
        request.json["name"],
        request.json["phone"],
        request.json["address_line"],
        request.json["address_state"],
        request.json["address_country"],
        request.json["address_local_area"],
        request.json["address_postal_code"],
        cart["key"]
    ))
    cart = cur.fetchone()

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "cart": cart
    })


@bp.put("/cart/account")
def account():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    cur.execute("""
        SELECT * FROM "order"
        WHERE user_key = %s AND status = "cart";
    """, (user["key"],))
    cart = cur.fetchone()

    if not cart:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

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
    elif request.json["amount"] > cart["cost_items"] + cart["cost_delivery"]:
        error = "amount larger than total cost "
    if error:
        return jsonify({
            "status": 400,
            "amount": error
        })

    cur.execute(log_template, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "changed_amount",
        cart["key"],
        "cart",
        200,
        json.dumps({
            "from": cart["pay_account_debit"],
            "to": request.json["amount"]
        })
    ))

    cur.execute("""
        UPDATE "order"
        SET pay_account_debit = %s
        WHERE key = %s;
        RETURNING *
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
