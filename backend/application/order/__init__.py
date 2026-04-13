import os
from datetime import datetime, timedelta, timezone

import requests
from flask import Blueprint, jsonify, request
from psycopg2.extras import Json

from ..cart.get import get_cart_items, has_adderss
from ..log import log
from ..postgres import db_close, db_open
from ..tools import get_session, send_mail

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

    if not has_adderss(order["receiver"]):
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
    if pay <= 0:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

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
        WHERE 'order.email.created' = ANY(access);
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
        AND v.variation = i.variation;
    """, (order["key"],))

    cur.execute("""
        UPDATE item i
        SET quantity = GREATEST(i.quantity - sub.total_quantity, 0)
        FROM (
            SELECT item_key, SUM(quantity) AS total_quantity
            FROM order_item
            WHERE order_key = %s
            GROUP BY item_key
        ) sub
        WHERE sub.item_key = i.key;
    """, (order["key"],))

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
    cur.execute(
        """INSERT INTO "order" (user_key) VALUES (%s);""", 
        (user["key"],)
    )

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


@bp.put("/orders/<key>/status/processing")
def processing(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "order.status.processing" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 403,
            "error": "unauthorized access"
        })

    cur.execute("""SELECT * FROM "order" WHERE key = %s;""", (key,))
    order = cur.fetchone()

    if (
        not order
        or order["status"] not in ("created", "enroute")
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    comment = request.json.get("comment", "").strip()

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
        action="changed order status",
        entity_type="order",
        entity_key=order["key"],
        misc={
            "from": order['status'],
            "to": "processing",
            "comment": comment
        }
    )

    if "enroute" in order["timeline"]:
        del order["timeline"]["enroute"]
    order["timeline"]["processing"] = f"{datetime.now(timezone.utc)}"

    cur.execute("""
        UPDATE "order"
            SET status = 'processing', timeline = %s
        WHERE key = %s RETURNING *;
    """, (Json(order["timeline"]), order["key"]))
    order = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "order": order
    })


@bp.put("/orders/<key>/status/enroute")
def enroute(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "order.status.enroute" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 403,
            "error": "unauthorized access"
        })

    cur.execute("""SELECT * FROM "order" WHERE key = %s;""", (key,))
    order = cur.fetchone()

    if (
        not order
        or order["status"] != "processing"
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    comment = request.json.get("comment", "").strip()

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
        action="changed order status",
        entity_type="order",
        entity_key=order["key"],
        misc={
            "from": order['status'],
            "to": "enroute",
            "comment": comment
        }
    )

    order["timeline"]["enroute"] = f"{datetime.now(timezone.utc)}"

    cur.execute("""
        UPDATE "order"
            SET status = 'enroute', timeline = %s
        WHERE key = %s RETURNING *;
    """, (Json(order["timeline"]), order["key"]))
    order = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "order": order
    })


@bp.put("/orders/<key>/status/delivered")
def delivered(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "order.status.delivered" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 403,
            "error": "unauthorized access"
        })

    comment = request.json.get("comment", "").strip()
    email_template_user = request.json.get("email_template_user")
    email_template_admin = request.json.get("email_template_admin")

    cur.execute("""SELECT * FROM "order" WHERE key = %s;""", (key,))
    order = cur.fetchone()
    cur.execute("""
        SELECT email FROM "user"
        WHERE 'order.email.delivered' = ANY(access);
    """)
    admins = cur.fetchall()

    if (
        not order
        or order["status"] != "enroute"
        or not admins
        or not email_template_user
        or not email_template_admin
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

    cur.execute(
        """SELECT * FROM "user" WHERE key = %s;""",
        (order["user_key"],))
    order_user = cur.fetchone()
    if not order_user:
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
            "to": "delivered",
            "comment": comment
        }
    )

    order["timeline"]["delivered"] = f"{datetime.now(timezone.utc)}"

    cur.execute("""
        UPDATE "order"
            SET status = 'delivered', timeline = %s
        WHERE key = %s RETURNING *;
    """, (Json(order["timeline"]), order["key"]))
    order = cur.fetchone()

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


@bp.put("/orders/<key>/status/canceled")
def canceled(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "order.status.canceled" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 403,
            "error": "unauthorized access"
        })

    comment = request.json.get("comment", "").strip()
    email_template_user = request.json.get("email_template_user")
    email_template_admin = request.json.get("email_template_admin")

    cur.execute("""SELECT * FROM "order" WHERE key = %s;""", (key,))
    order = cur.fetchone()
    cur.execute("""
        SELECT email FROM "user"
        WHERE 'order.email.canceled' = ANY(access);
    """)
    admins = cur.fetchall()

    if (
        not order
        or order["status"] not in ['created', 'processing', 'enroute']
        or not admins
        or not email_template_user
        or not email_template_admin
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

    cur.execute(
        """SELECT * FROM "user" WHERE key = %s;""",
        (order["user_key"],))
    order_user = cur.fetchone()
    if not order_user:
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
            "to": "canceled",
            "comment": comment
        }
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


@bp.put("/orders/<key>/status/returning")
def returning_(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    comment = request.json.get("comment", "").strip()
    email_template_user = request.json.get("email_template_user")
    email_template_admin = request.json.get("email_template_admin")

    cur.execute("""SELECT * FROM "order" WHERE key = %s;""", (key,))
    order = cur.fetchone()
    cur.execute("""
        SELECT email FROM "user"
        WHERE 'order.email.returning' = ANY(access);
    """)
    admins = cur.fetchall()

    if (
        not order
        or user["key"] != order["user_key"]
        or order["status"] != "delivered"
        or not admins
        or not email_template_user
        or not email_template_admin
    ):
        db_close(con, cur)
        return jsonify({
            "status": 403,
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

    if (
        datetime.now(timezone.utc) - datetime.fromisoformat(
            order["timeline"]["delivered"].replace("Z", "+00:00")
        ) > timedelta(days=7)
    ):
        db_close(con, cur)
        return jsonify({
            "status": 403,
            "error": """The order is outside the return window.
                You can only return the order within 7 days of delivery."""
        })

    log(
        cur=cur,
        user_key=user["key"],
        action="returning order",
        entity_type="order",
        entity_key=order["key"],
        misc={"comment": comment}
    )

    order["timeline"]["returning"] = f"{datetime.now(timezone.utc)}"

    cur.execute("""
        UPDATE "order"
        SET status = 'returning', timeline = %s
        WHERE key = %s RETURNING *;
    """, (Json(order["timeline"]), order["key"]))
    order = cur.fetchone()

    send_mail(
        user["email"],
        "Returning Order",
        email_template_user.format(name=user["name"])
    )
    send_mail(
        [x["email"] for x in admins],
        "Returning Order",
        email_template_admin.format(
            name=user["name"],
            username=user["username"]
        )
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "order": order
    })


@bp.put("/orders/<key>/status/returned")
def returned(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "order.status.returned" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 403,
            "error": "unauthorized access"
        })

    comment = request.json.get("comment", "").strip()
    email_template_user = request.json.get("email_template_user")
    email_template_admin = request.json.get("email_template_admin")

    cur.execute("""SELECT * FROM "order" WHERE key = %s;""", (key,))
    order = cur.fetchone()
    cur.execute("""
        SELECT email FROM "user"
        WHERE 'order.email.returned' = ANY(access);
    """)
    admins = cur.fetchall()

    if (
        not order
        or order["status"] != "returning"
        or not admins
        or not email_template_user
        or not email_template_admin
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

    cur.execute(
        """SELECT * FROM "user" WHERE key = %s;""",
        (order["user_key"],))
    order_user = cur.fetchone()
    if not order_user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    log(
        cur=cur,
        user_key=order_user["key"],
        action="returned order",
        entity_type="order",
        entity_key=order["key"],
        misc={
            "admin": user["key"],
            "comment": comment
        }
    )

    order["timeline"]["returned"] = f"{datetime.now(timezone.utc)}"

    cur.execute("""
        UPDATE "order"
        SET status = 'returned', timeline = %s
        WHERE key = %s RETURNING *;
    """, (Json(order["timeline"]), order["key"]))
    order = cur.fetchone()

    send_mail(
        order_user["email"],
        "Order Returned",
        email_template_user.format(name=order_user["name"])
    )
    send_mail(
        [x["email"] for x in admins],
        "Order Returned",
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
