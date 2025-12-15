from flask import Blueprint, jsonify, request
from ..tools import get_session
from ..postgres import db_open, db_close
from psycopg2.extras import Json
from ..log import log
from .get import get_cart_items

bp = Blueprint("cart", __name__)


@bp.post("/cart")
def add_to_cart():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    item_key = request.json.get("key")
    quantity = request.json.get("quantity", 1)
    variation = request.json.get("variation", {})
    operation = request.json.get("operation", "replace")

    cur.execute("""
        SELECT * FROM item WHERE key = %s AND status = 'active'
    ;""", (item_key,))
    item = cur.fetchone()

    cur.execute("""
        SELECT * FROM "order" WHERE user_key = %s AND status = 'cart';
    """, (user["key"],))
    cart = cur.fetchone()
    if (
        not item
        or not cart
        or type(variation) is not dict
        or operation not in ["add", "replace"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    error = {}
    if not isinstance(quantity, int) or quantity < 1:
        error["quantity"] = "Please enter a valid number"

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
        action="added_to_cart",
        entity_key=cart["key"],
        entity_type="cart",
        misc={
            "key": order_item["item_key"],
            "variation": order_item["variation"],
            "quantity": order_item["quantity"]
        }
    )

    cart_items = get_cart_items(cur)

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "cart_items": cart_items.json["cart_items"]
    })


@bp.delete("/cart")
def remove_from_cart():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    item_key = request.json.get("key")
    variation = request.json.get("variation", {})

    cur.execute("""
        SELECT * FROM "order" WHERE user_key = %s AND status = 'cart';
    """, (user["key"],))
    cart = cur.fetchone()

    if not cart or not item_key or type(variation) is not dict:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute("""
        SELECT * FROM order_item
        WHERE order_key = %s AND item_key = %s AND variation = %s;
    """, (cart["key"], item_key, Json(variation)))
    if cur.fetchone():
        cur.execute("""
            DELETE FROM order_item
            WHERE order_key = %s AND item_key = %s AND variation = %s;
        """, (cart["key"], item_key, Json(variation)))

        log(
            cur=cur,
            user_key=user["key"],
            action="removed_from_cart",
            entity_key=cart["key"],
            entity_type="cart",
            misc={
                "key": item_key,
                "variation": variation
            }
        )

    cart_items = get_cart_items(cur)

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "cart_items": cart_items.json["cart_items"]
    })


# @bp.put("/cart/receiver")
# def receiver():
#     con, cur = db_open()

#     user = token_to_user(cur)
#     if not user:
#         db_close(con, cur)
#         return jsonify({
#             "status": 400,
#             "error": "invalid token"
#         })

#     cur.execute("""
#         SELECT * FROM "order"
#         WHERE user_key = %s AND status = 'cart';
#     """, (user["key"],))
#     cart = cur.fetchone()

#     if not cart:
#         db_close(con, cur)
#         return jsonify({
#             "status": 400,
#             "error": "invalid request"
#         })

#     error = {}
#     if "name" not in request.json or not request.json["name"]:
#         error["name"] = "this field is required"
#     if "phone" not in request.json or not request.json["phone"]:
#         error["phone"] = "this field is required"
#     if "line" not in request.json or not request.json["line"]:
#         error = "this field is required"
#     if "state" not in request.json or not request.json["state"]:
#         error["state"] = "this field is required"
#     if "country" not in request.json or not request.json["country"]:
#         error["country"] = "this field is required"
#     if "local_area" not in request.json or not request.json["local_area"]:
#         error["local_area"] = "this field is required"
#     if "postal_code" not in request.json or not request.json["postal_code"]:
#         error["postal_code"] = "this field is required"

#     if error != {}:
#         db_close(con, cur)
#         return jsonify({
#             "status": 400,
#             **error
#         })

#     log(
#         cur=cur,
#         user_key=user["key"],
#         action="edited_receiver",
#         entity_key=cart["key"],
#         entity_type="cart",
#         misc={
#             "from": f"""
#                 {cart["name"]} |
#                 {cart["phone"]} |
#                 {cart["line"]} |
#                 {cart["country"]} |
#                 {cart["state"]} |
#                 {cart["local_area"]} |
#                 {cart["postal_code"]}
#             """,
#             "to": f"""
#                 {request.json["name"]} |
#                 {request.json["phone"]} |
#                 {request.json["line"]} |
#                 {request.json["state"]} |
#                 {request.json["country"]} |
#                 {request.json["local_area"]} |
#                 {request.json["postal_code"]}
#             """
#         }
#     )

#     cur.execute("""
#         UPDATE "order"
#         SET
#             name = %s,
#             phone = %s,
#             line = %s,
#             country = %s,
#             state = %s,
#             local_area = %s,
#             postal_code = %s
#         WHERE key = %s
#         RETURNING *;
#     """, (
#         request.json["name"],
#         request.json["phone"],
#         request.json["line"],
#         request.json["country"],
#         request.json["state"],
#         request.json["local_area"],
#         request.json["postal_code"],
#         cart["key"]
#     ))
#     cart = cur.fetchone()

#     db_close(con, cur)
#     return jsonify({
#         "status": 200,
#         "cart": cart
#     })


# @bp.put("/cart/account")
# def account():
#     con, cur = db_open()

#     user = token_to_user(cur)
#     if not user:
#         db_close(con, cur)
#         return jsonify({
#             "status": 400,
#             "error": "invalid token"
#         })

#     cur.execute("""
#         SELECT * FROM "order"
#         WHERE user_key = %s AND status = 'cart';
#     """, (user["key"],))
#     cart = cur.fetchone()

#     if not cart:
#         db_close(con, cur)
#         return jsonify({
#             "status": 400,
#             "error": "invalid request"
#         })

#     cur.execute("""
#        SELECT
#             SUM(item.price * order_item.quantity) AS total
#         FROM item
#         LEFT JOIN order_item ON item.key = order_item.item_key
#         WHERE
#             order_item.order_key = %s
#             AND item.status = 'live';
#     """, (cart["key"],))
#     cost_items = cur.fetchone()[0]

#     error = None
#     if "amount" not in request.json:
#         error = "invalid request"
#     elif (
#         type(request.json["amount"]) not in [int, float]
#         or request.json["amount"] < 0
#     ):
#         error = "Please enter a valid amount"
#     elif request.json["amount"] > user["account_balance"]:
#         error = "amount larger than available balance"
#     elif request.json["amount"] > cost_items + cart["cost_delivery"]:
#         error = "amount larger than total cost"
#     if error:
#         db_close(con, cur)
#         return jsonify({
#             "status": 400,
#             "amount": error
#         })

#     log(
#         cur=cur,
#         user_key=user["key"],
#         action="changed_amount",
#         entity_key=cart["key"],
#         entity_type="cart",
#         misc={
#             "from": cart["pay_account"],
#             "to": request.json["amount"]
#         }
#     )

#     cur.execute("""
#         UPDATE "order"
#         SET pay_account = %s
#         WHERE key = %s
#         RETURNING *;
#     """, (
#         request.json["amount"],
#         cart["key"]
#     ))
#     cart = cur.fetchone()

#     db_close(con, cur)
#     return jsonify({
#         "status": 200,
#         "cart": cart
#     })
