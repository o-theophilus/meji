import os
from datetime import datetime, timedelta, timezone

import requests
from flask import Blueprint, jsonify, request
from psycopg2.extras import Json

from ..cart.get import get_cart_items
from ..log import log
from ..postgres import db_close, db_open
# from ..storage import storage
from ..tools import get_session, send_mail
from .get import order_status

bp = Blueprint("order", __name__)


@bp.get("/order/check")
def order_check():
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
    order = cur.fetchone()
    if not order:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if (
        "name" not in order["receiver"]
        or not order["receiver"]["name"]
        or "phone" not in order["receiver"]
        or not order["receiver"]["phone"]
        or "email" not in order["receiver"]
        or not order["receiver"]["email"]
        or "address" not in order["receiver"]
        or order["receiver"]["address"] == {}
        or "address" not in order["receiver"]["address"]
        or not order["receiver"]["address"]["address"]
        or "state" not in order["receiver"]["address"]
        or not order["receiver"]["address"]["state"]
        or "country" not in order["receiver"]["address"]
        or not order["receiver"]["address"]["country"]
        or "postal_code" not in order["receiver"]["address"]
        or not order["receiver"]["address"]["postal_code"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "incomplete receiver information"
        })

    cur.execute("""
        SELECT
            item.price,
            item.quantity,
            item.status,
            order_item.quantity AS order_quantity
        FROM order_item
        LEFT JOIN item ON item.key = order_item.item_key
        WHERE
            order_item.order_key = %s;
    """, (order["key"],))
    items = cur.fetchall()
    if len(items) == 0:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    for x in items:
        if (
            x["status"] != 'active'
            or x["order_quantity"] == 0
            or x["order_quantity"] > x["quantity"]
        ):
            return jsonify({
                "status": 400,
                "error": "Some items in your cart are no longer available"
            })

    total_order = sum(x["price"] * x["order_quantity"] for x in items)
    discount = 0

    cur.execute("""
        SELECT * FROM coupon WHERE order_key = %s;
    """, (order["key"],))
    coupon = cur.fetchone()
    if coupon and coupon["status"] == "active":
        condition_met = True
        if coupon["benefit"]["condition"] > 0:
            if coupon["benefit"]["condition_unit"] == 'total order':
                condition_met = total_order >= coupon["benefit"]["condition"]
            else:
                condition_met = False

        if condition_met:
            applies_to = 0
            if coupon["benefit"]["applies_to"] == 'total order':
                applies_to = total_order
            elif coupon["benefit"]["applies_to"] == 'delivery fee':
                applies_to = order["delivery_cost"]

            if coupon["benefit"]["value_unit"] == 'flat':
                discount = coupon["benefit"]["value"]
            elif coupon["benefit"]["value_unit"] == 'percent':
                discount = (applies_to * coupon["benefit"]["value"]) / 100
                discount = round(discount, 2)

            discount = min(discount, applies_to)

    pay = total_order + order["delivery_cost"] - discount
    pay = max(pay, 0)

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "pay": pay
    })


@bp.post("/order")
def cart_to_order():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute("""
        SELECT *
        FROM "order"
        WHERE user_key = %s AND status = 'cart';
    """, (user["key"],))
    order = cur.fetchone()

    cur.execute("""
        SELECT email FROM "user"
        WHERE 'order.email_order_created' = ANY(access);
    """)
    admins_to_notify = cur.fetchall()

    reference = request.json.get("reference")
    email_template_admin = request.json.get("email_template_admin")
    email_template_user = request.json.get("email_template_user")

    if (
        not order
        or admins_to_notify == []
        or not reference
        or not email_template_admin
        or not email_template_user
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("""
        SELECT
            item.*,
            order_item.quantity AS order_quantity
        FROM order_item
        LEFT JOIN item ON item.key = order_item.item_key
        WHERE
            order_item.order_key = %s;
    """, (order["key"],))
    items = cur.fetchall()
    if len(items) == 0:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    total_order = sum(x["price"] * x["order_quantity"] for x in items)
    discount = 0

    cur.execute("""
        SELECT * FROM coupon WHERE order_key = %s;
    """, (order["key"],))
    coupon = cur.fetchone()
    if coupon and coupon["status"] == "active":
        condition_met = True
        if coupon["benefit"]["condition"] > 0:
            if coupon["benefit"]["condition_unit"] == 'total order':
                condition_met = total_order >= coupon["benefit"]["condition"]
            else:
                condition_met = False

        if condition_met:
            applies_to = 0
            if coupon["benefit"]["applies_to"] == 'total order':
                applies_to = total_order
            elif coupon["benefit"]["applies_to"] == 'delivery fee':
                applies_to = order["delivery_cost"]

            if coupon["benefit"]["value_unit"] == 'flat':
                discount = coupon["benefit"]["value"]
            elif coupon["benefit"]["value_unit"] == 'percent':
                discount = (applies_to * coupon["benefit"]["value"]) / 100
                discount = round(discount, 2)

            discount = min(discount, applies_to)

    pay = total_order + order["delivery_cost"] - discount
    pay = max(pay, 0)

    cur.execute(
        """SELECT * FROM "order" WHERE payment_reference = %s;""",
        (reference,))
    if cur.fetchone():
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    resp = requests.get(
        f"https://api.paystack.co/transaction/verify/{reference}",
        headers={
            'Content-Type': 'application/json',
            "Authorization": os.environ["PAYSTACK_KEY"]
        }
    )
    resp = resp.json()

    if (
        not resp["status"]
        or "data" not in resp
        or "status" not in resp["data"]
        or resp["data"]["status"] != "success"
        or "reference" not in resp["data"]
        or resp["data"]["reference"] != reference
        or "amount" not in resp["data"]
        or resp["data"]["amount"]/100 != pay
        or "currency" not in resp["data"]
        or resp["data"]["currency"] != "NGN"
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid transaction"
        })

    cur.execute("""
        INSERT INTO item_version(
            item_key, status, date_created, slug, name,
            tags, price, price_old, information, specification,
            files, variation, quantity
        )
        SELECT
            i.key, i.status, i.date_created, i.slug, i.name,
            i.tags, i.price, i.price_old, i.information, i.specification,
            i.files, i.variation, i.quantity
        FROM order_item oi
        JOIN item i ON i.key = oi.item_key
        WHERE oi.order_key = %s
        AND NOT EXISTS (
            SELECT 1
            FROM item_version v
            WHERE v.item_key = i.key
            AND v.status = i.status
            AND v.slug = i.slug
            AND v.name = i.name
            AND v.price = i.price
            AND v.information = i.information
            AND v.specification = i.specification
            AND v.files = i.files
            AND v.variation = i.variation
        );
    """, (order["key"],))

    cur.execute("""
        UPDATE order_item oi
        SET item_key = NULL,  item_version_key = v.key
        FROM item i
        JOIN item_version v ON v.item_key = i.key
        WHERE oi.order_key = %s
        AND oi.item_key = i.key
        AND v.status = i.status
        AND v.slug = i.slug
        AND v.name = i.name
        AND v.price = i.price
        AND v.information = i.information
        AND v.specification = i.specification
        AND v.files = i.files
        AND v.variation = i.variation --RETURNING v.*;
    """, (order["key"],))
    # new_versions = cur.fetchall()

    # files = set()
    # for v in new_versions:
    #     files.update(v["files"])
    # for f in files:
    #     try:
    #         storage.copy(f, "item", "item_version")
    #     except Exception:
    #         pass

    # TODO: subtract from item quantity

    order["timeline"]["created"] = f"{datetime.now(timezone.utc)}"
    order["timeline"]["delivery_date"
                      ] = f"{datetime.now(timezone.utc) + timedelta(days=7)}"

    cur.execute("""
        UPDATE "order"
        SET
            status = 'created',
            order_cost = %s, timeline = %s,
            payment = %s,  payment_reference = %s
        WHERE key = %s RETURNING *;
    """, (
        total_order, Json(order["timeline"]),
        pay, reference,
        order["key"]
    ))
    order = cur.fetchone()
    get_cart_items(cur)

    log(
        cur=cur,
        user_key=user["key"],
        action="created order",
        entity_type="order",
        entity_key=order["key"],
    )

    if discount > 0:
        cur.execute("""
            UPDATE coupon SET status = 'used'
            WHERE key = %s RETURNING *;
        """, (coupon["key"],))
        log(
            cur=cur,
            user_key=user["key"],
            action="used coupon",
            entity_type="order",
            entity_key=order["key"],
            misc={
                "entity_type": "coupon",
                "entity_key": coupon["key"]
            }
        )

    send_mail(
        user["email"],
        "Processing Order",
        email_template_user.format(name=user["name"])
    )
    send_mail(
        [x["email"] for x in admins_to_notify],
        "New Order",
        email_template_admin.format(
            name=user["name"],
            username=user["username"]
        )
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "order": order,
    })


@bp.put("/orders/<key>/delivery_date")
def delivery_date(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "order.edit_delivery_date" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 403,
            "error": "unauthorized access"
        })

    cur.execute("""SELECT * FROM "order" WHERE key = %s;""", (key,))
    order = cur.fetchone()
    if not order or order["status"] != "created":
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = {}
    delivery_date = request.json.get("delivery_date", "").strip()
    if not delivery_date or type(delivery_date) is not str:
        error["delivery_date"] = "This field is required"
    elif delivery_date == order["timeline"]["delivery_date"]:
        error["delivery_date"] = "No changes were made"
    else:
        try:
            parsed_date = datetime.strptime(delivery_date, "%Y-%m-%dT%H:%M:%S")
            if parsed_date < datetime.now(timezone.utc):
                error["delivery_date"] = "Cannot set delivery date in the past"
        except Exception:
            error["error"] = "Invalid date format"

    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    log(
        cur=cur,
        user_key=user["key"],
        action="changed order delivery date",
        entity_type="order",
        entity_key=order["key"],
        misc={
            "from": f"{order["timeline"]['delivery_date']}",
            "to": delivery_date
        }
    )

    order["timeline"]["delivery_date"] = delivery_date

    cur.execute("""
        UPDATE "order" SET timeline = %s
        WHERE key = %s RETURNING *;
    """, (Json(order["timeline"]), order["key"]))
    order = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "order": order
    })


@bp.put("/orders/<key>/status")
def status(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "order.edit_status" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 403,
            "error": "unauthorized access"
        })

    cur.execute("""SELECT * FROM "order" WHERE key = %s;""", (key,))
    order = cur.fetchone()
    if not order:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute(
        """SELECT * FROM "user" WHERE key = %s;""",
        (order["user_key"],))
    order_user = cur.fetchone()
    cur.execute("""
        SELECT email FROM "user"
        WHERE 'order.email_order_delivered' = ANY(access);
    """)
    admins = cur.fetchall()

    status = request.json.get("status")
    comment = request.json.get("comment", "").strip()
    email_template_user = request.json.get("email_template_user")
    email_template_admin = request.json.get("email_template_admin")

    if (
        not order_user
        or admins == []
        or not status
        or status not in order_status[:-1]
        or not email_template_user
        or not email_template_admin
        or order["status"] in ["delivered", "canceled"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = {}
    if not comment:
        error["comment"] = "This field is required"
    elif len(comment) > 500:
        error["comment"] = "This field cannot exceed 500 characters"
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    i = order_status.index(order["status"])
    j = order_status.index(status)
    if i + 1 != j and i - 1 != j:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    log(
        cur=cur,
        user_key=user["key"],
        action="changed order status",
        entity_type="order",
        entity_key=order["key"],
        misc={
            "from": order['status'],
            "to": status,
            "comment": comment
        }
    )

    i = order_status.index(status)
    for x in order_status[i+1:]:
        if x in order["timeline"]:
            del order["timeline"][x]

    if status != "created":
        order["timeline"][status] = f"{datetime.now(timezone.utc)}"

    cur.execute("""
        UPDATE "order"
            SET status = %s, timeline = %s
        WHERE key = %s RETURNING *;
    """, (status, Json(order["timeline"]), order["key"]))
    order = cur.fetchone()

    if status == "delivered":
        send_mail(
            order_user["email"],
            "Order Delivered - Thank you",
            email_template_user.format(name=order_user["name"])
        )
        send_mail(
            [x["email"] for x in admins],
            "Order Delivered",
            email_template_admin.format(
                name=order_user["name"],
                username=order_user["username"]
            )
        )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "order": order
    })


@bp.delete("/orders/<key>/status")
def cancel(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute("""SELECT * FROM "order" WHERE key = %s;""", (key,))
    order = cur.fetchone()
    if not order:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if "order.cancel" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 403,
            "error": "unauthorized access"
        })

    cur.execute(
        """SELECT * FROM "user" WHERE key = %s;""",
        (order["user_key"],))
    order_user = cur.fetchone()
    cur.execute("""
        SELECT email FROM "user"
        WHERE 'order:email_order_canceled' = ANY(access);
    """)
    admins = cur.fetchall()

    comment = request.json.get("comment", "").strip()
    email_template_user = request.json.get("email_template_user")
    email_template_admin = request.json.get("email_template_admin")

    if (
        not order_user
        or admins == []
        or not email_template_user
        or not email_template_admin
        or order["status"] in ["delivered", "canceled"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = {}
    if not comment:
        error["comment"] = "This field is required"
    elif len(comment) > 500:
        error["comment"] = "This field cannot exceed 500 characters"
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    log(
        cur=cur,
        user_key=user["key"],
        action="canceled order",
        entity_type="order",
        entity_key=order["key"],
        misc={"comment": comment}
    )

    order["timeline"]["canceled"] = f"{datetime.now(timezone.utc)}"

    cur.execute("""
        UPDATE "order"
        SET status = 'canceled', timeline = %s
        WHERE key = %s RETURNING *;
    """, (Json(order["timeline"]), order["key"]))
    order = cur.fetchone()

    send_mail(
        order_user["email"],
        "Order Canceled",
        email_template_user.format(name=order_user["name"])
    )
    send_mail(
        [x["email"] for x in admins],
        "Order Canceled",
        email_template_admin.format(
            name=order_user["name"],
            username=order_user["username"]
        )
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "order": order
    })
