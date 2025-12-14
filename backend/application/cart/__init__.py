from flask import Blueprint, jsonify, request
from .tools import token_to_user, user_schema
from uuid import uuid4
from ..postgres import db_open, db_close
import json
from .log import log

bp = Blueprint("cart", __name__)


@bp.post("/cart")
def add_to_cart():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
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
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("""
        SELECT *
        FROM item
        WHERE key = %s AND status = 'live';
    """, (request.json["key"],))
    item = cur.fetchone()
    if not item or item["status"] != "live":
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("""
        SELECT *
        FROM "order"
        WHERE user_key = %s AND status = 'cart';
    """, (user["key"],))
    cart = cur.fetchone()

    if not cart:
        cur.execute("""
            INSERT INTO "order" (key, version, user_key)
            VALUES (%s, %s, %s)
            RETURNING *;
        """, (
            uuid4().hex,
            uuid4().hex,
            user["key"]
        ))
        cart = cur.fetchone()

    cur.execute("""
        SELECT *
        FROM order_item
        WHERE
            order_key = %s
            AND item_key = %s
            AND variation = %s;
    """, (
        cart["key"],
        item["key"],
        json.dumps(request.json["variation"])
    ))
    if cur.fetchone():
        cur.execute("""
            UPDATE order_item
            SET quantity = order_item.quantity + %s
            WHERE
                order_key = %s
                AND item_key = %s
                AND variation = %s;
        """, (
            request.json["quantity"],
            cart["key"],
            item["key"],
            json.dumps(request.json["variation"]),
        ))

    else:
        cur.execute("""
            INSERT INTO order_item (
                key, order_key, item_key, variation, quantity)
            VALUES (%s, %s, %s, %s, %s);
        """, (
            uuid4().hex,
            cart["key"],
            item["key"],
            json.dumps(request.json["variation"]),
            request.json["quantity"]
        ))

    log(
        cur=cur,
        user_key=user["key"],
        action="added_to",
        entity_key=cart["key"],
        entity_type="cart",
        misc={
            "key": request.json["key"],
            **request.json["variation"],
            "quantity": request.json["quantity"]
        }
    )

    cur.execute("""
        SELECT item_key, variation
        FROM order_item
        WHERE order_key = %s;
    """, (cart["key"],))
    cart_items = cur.fetchall()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(
            user,
            cart=[f"{x['item_key']}_{json.dumps(x['variation'])}"
                  for x in cart_items]
        )
    })


# @bp.put("/cart/quantity")
# def quantity():
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

#     if (
#         "key" not in request.json
#         or not request.json["key"]
#         or "variation" not in request.json
#         or "quantity" not in request.json
#         or type(request.json["quantity"]) is not int
#         or request.json["quantity"] < 0
#         or not cart
#     ):
#         db_close(con, cur)
#         return jsonify({
#             "status": 400,
#             "error": "invalid request"
#         })

#     cur.execute("""
#         SELECT *
#         FROM order_item
#         WHERE order_key = %s
#             AND item_key = %s
#             AND variation = %s;
#     """, (
#         cart["key"],
#         request.json["key"],
#         json.dumps(request.json["variation"])
#     ))
#     item = cur.fetchone()
#     if not item:
#         db_close(con, cur)
#         return jsonify({
#             "status": 400,
#             "error": "invalid request"
#         })

#     cur.execute("""
#         UPDATE order_item
#         SET quantity = %s
#         WHERE key = %s;

#         DELETE FROM order_item
#         WHERE quantity = 0;
#     """, (
#         request.json["quantity"],
#         item["key"]
#     ))

#     log(
#         cur=cur,
#         user_key=user["key"],
#         action="changed_quantity" if request.json[
#             "quantity"] > 0 else "removed_from",
#         entity_key=cart["key"],
#         entity_type="cart",
#         misc={
#             "key": request.json["key"],
#             **request.json["variation"],
#             "from_quantity": item["quantity"],
#             "to_quantity": request.json["quantity"]
#         } if request.json["quantity"] > 0 else {
#             "key": request.json["key"],
#             **request.json["variation"]
#         }
#     )

#     cur.execute("""
#         SELECT
#             item.key,
#             item.slug,
#             item.name,
#             item.price,
#             item.status,
#             COALESCE(item.photos[1], NULL) AS photo,
#             order_item.variation,
#             order_item.quantity
#         FROM item
#         LEFT JOIN order_item ON item.key = order_item.item_key
#         WHERE order_item.order_key = %s;
#     """, (cart["key"],))
#     items = cur.fetchall()

#     if items == []:
#         cur.execute("""DELETE FROM "order" WHERE key = %s;""", 
# (cart["key"],))
#         db_close(con, cur)
#         return jsonify({
#             "status": 200,
#             "user": user_schema(user),
#             "cart": None,
#             "items": []
#         })

#     cost_items = 0
#     for x in items:
#         cost_items += x["price"] * x["quantity"]
#         x["photo"] = f"{request.host_url}photo/{x['photo']}"

#     if (
#         cart["pay_account"] > user["account_balance"]
#         or cart["pay_account"] > cost_items
#     ):
#         cur.execute("""
#             UPDATE "order"
#             SET pay_account = 0
#             WHERE key = %s
#             RETURNING *;
#         """, (cart["key"],))
#         cart = cur.fetchone()

#     db_close(con, cur)
#     return jsonify({
#         "status": 200,
#         "cart": cart,
#         "items": items,
#         "user": user_schema(
#             user,
#             cart=[f"{x['key']}_{json.dumps(x['variation'])}"
#                   for x in items]
#         )
#     })


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
