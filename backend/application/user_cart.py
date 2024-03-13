from flask import Blueprint, jsonify, request
from .tools import token_to_user, now
from .schema import user_schema, item_schema
from uuid import uuid4
from .log import log_template
from .postgres import db_close, db_open
from datetime import datetime

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
        INSERT INTO cart_item (user_key, item_key, variation, quantity)
        VALUES (%s, %s, %s, %s);
        ON CONFLICT (user_key, item_key, variation)
        DO UPDATE SET quantity = quantity + EXCLUDED.quantity
        RETURNING *;
    """, (
        user["key"],
        request.json["key"],
        request.json["variation"],
        request.json["quantity"]
    ))

    cur.execute("""
        INSERT INTO cart (user_key, transaction_total_items)
        SELECT %s, SUM(cart_item.quantity * item.price) AS total
        FROM cart_item
        LEFT JOIN item ON cart_item.item_key = item.key
        WHERE cart_item.user_key = %s
        ON CONFLICT (user_key)
        DO UPDATE SET transaction_total_items = EXCLUDED.total;
    """, (
        user["key"],
        user["key"]
    ))

    cur.execute(log_template, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "added_to",
        request.json["key"],
        "cart",
        200,
        {
            **request.json["variation"],
            "quantity": request.json["quantity"]
        }
    ))

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })


@bp.get("/cart")
def get_cart():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    cur.execute("""
        INSERT INTO cart (user_key)
        VALUES (%s)
        ON CONFLICT (user_key) DO UPDATE
        SET transaction_account = CASE
            WHEN cart.transaction_account > %s THEN 0
            ELSE cart.transaction_account
        END
        RETURNING *;
    """, (user["key"], user["account_balance"]))
    cart = cur.fetchone()

    cart["delivery_date"] = f"{now(4).split('T')[0]}T10:00"

    cur.execute("""
        SELECT item.*, cart_item.variation AS variation,
            cart_item.quantity AS quantity
        FROM cart_item
        LEFT JOIN item ON cart_item.item_key = item.key
        WHERE cart_item.user_key = %s;
    """, (user["key"],))
    items = cur.fetchone()

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
        user["key"],
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


@bp.put("/cart_item_quantity")
def cart_item_quantity():
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
        SELECT *
        FROM cart_item
        WHERE user_key = %s AND item_key = %s;
    """, (
        user["key"],
        request.json["key"],
    ))
    cart_item = cur.fetchone()
    if not cart_item:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("""
        UPDATE cart_item
        SET quantity = %s
        WHERE
            user_key = %s
            AND item_key = %s
            AND variation = %s;

        DELETE FROM cart_item
        WHERE quantity = 0;
    """, (
        request.json["quantity"],
        user["key"],
        request.json["key"],
        request.json["variation"]
    ))

    cur.execute(log_template, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "changed_quantity" if request.json["quantity"
                                           ] > 0 else "removed_from",
        request.json["key"],
        "cart",
        200,
        {
            **request.json["variation"],
            "from_quantity": cart_item["quantity"],
            "to_quantity": request.json["quantity"]
        } if request.json["quantity"] > 0 else {
            **request.json["variation"]
        }
    ))

    cur.execute("SELECT * FROM cart_item WHERE user_key = %s;", (user["key"],))
    items = cur.fetchall()

    cart = []
    if items.length == 0:
        cur.execute("""
            UPDATE cart
            SET transaction_total_items = (
                SELECT SUM(cart_item.quantity * item.price)
                FROM cart_item
                LEFT JOIN item ON cart_item.item_key = item.key
                WHERE cart_item.user_key = %s
            )
            WHERE user_key = %s
            RETURNING *;
        """, (
            user["key"],
            user["key"]
        ))
        cart = cur.fetchone()
    else:
        cur.execute("""
            DELETE FROM cart
            WHERE user_key = %s;
        """, (user["key"],))

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "user": user_schema(user),
        "cart": cart,
        "items": [item_schema(x) for x in items],
    })


@bp.put("/cart_receiver")
def cart_receiver():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    cur.execute("SELECT * FROM cart WHERE user_key = %s;", (user["key"],))
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
        user["key"],
        "cart",
        200,
        {
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
        }
    ))

    cur.execute("""
        UPDATE cart
        SET
            receiver_name = %s,
            receiver_phone = %s,
            receiver_address_line = %s,
            receiver_address_country = %s,
            receiver_address_state = %s,
            receiver_address_local_area = %s,
            receiver_address_postal_code = %s
        WHERE user_key = %s;
        RETURNING *
    """, (
        request.json["name"],
        request.json["phone"],
        request.json["address_line"],
        request.json["address_state"],
        request.json["address_country"],
        request.json["address_local_area"],
        request.json["address_postal_code"],
        user["key"]
    ))
    cart = cur.fetchone()

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "cart": cart
    })


@bp.put("/cart_account")
def cart_account():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    cur.execute("SELECT * FROM cart WHERE user_key = %s;", (user["key"],))
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
    elif request.json["amount"] > cart["transaction"][
            "total_items"] + cart["transaction"]["delivery_fee"]:
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
        user["key"],
        "cart",
        200,
        {
            "from": cart["transaction_account_debit"],
            "to": request.json["amount"]
        }
    ))

    cur.execute("""
        UPDATE cart
        SET transaction_account_debit = %s
        WHERE user_key = %s;
        RETURNING *
    """, (
        request.json["amount"],
        user["key"]
    ))
    cart = cur.fetchone()

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "cart": cart
    })
