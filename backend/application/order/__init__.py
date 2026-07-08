import os
from datetime import datetime, timedelta, timezone
from decimal import Decimal

import requests
from flask import Blueprint, request
from psycopg2.extras import Json

from ..cart.delivery import get_delivery_cost
from ..cart.get import has_adderss
from ..tools import log, rate_limit, send_mail, session

bp = Blueprint("order", __name__)


@bp.get("/order/check")
@session(True)
@rate_limit(20, 1)
@log("order")
def order_check(cur, user):
    cur.execute("""
        SELECT * FROM "order" WHERE user_key = %s AND status = 'cart';
    """, (user["key"],))
    order = cur.fetchone()
    if not order:
        return {
            "status": 404,
            "error": "invalid request"
        }, 404

    if not has_adderss(order["receiver"]):
        return {
            "status": 422,
            "error": "incomplete receiver information"
        }, 422

    cur.execute("""
        SELECT
            item.price,
            item.quantity AS available_quantity,
            item.status,
            order_item.quantity,
            item.metadata
        FROM order_item
        LEFT JOIN item ON item.key = order_item.item_key
        WHERE order_item.order_key = %s;
    """, (order["key"],))
    items = cur.fetchall()
    if len(items) == 0:
        return {
            "status": 404,
            "error": "invalid request"
        }, 404

    for x in items:
        if (
            x["status"] != 'active'
            or x["quantity"] == 0
            or x["quantity"] > x["available_quantity"]
        ):
            return {
                "status": 422,
                "error": "Some items in your cart are no longer available"
            }, 422

    total_order = sum(x["price"] * x["quantity"] for x in items)

    delivery_cost = get_delivery_cost(
        items, order["receiver"]["address"]["area"])

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
                applies_to = delivery_cost

            if coupon["benefit"]["value_unit"] == 'flat':
                discount = coupon["benefit"]["value"]
            elif coupon["benefit"]["value_unit"] == 'percent':
                discount = (applies_to * coupon["benefit"]["value"]) / 100
                discount = round(discount, 2)

            discount = min(discount, applies_to)

    pay = total_order + Decimal(delivery_cost) - Decimal(str(discount))
    if pay <= 0:
        return {
            "status": 400,
            "error": "invalid request"
        }, 400

    return {
        "status": 200,
        "pay": pay
    }, 200


@bp.post("/order")
@session(True)
@rate_limit(20, 1)
@log("order")
def cart_to_order(cur, user):
    cur.execute("""
        SELECT * FROM "order" WHERE user_key = %s AND status = 'cart';
    """, (user["key"],))
    order = cur.fetchone()
    if not order:
        return {
            "status": 404,
            "error": "invalid request"
        }, 404

    reference = request.json.get("reference")
    email_template_admin = request.json.get("email_template_admin")
    email_template_user = request.json.get("email_template_user")

    if (
        not reference
        or not email_template_admin
        or not email_template_user
    ):
        return {
            "status": 422,
            "error": "invalid request"
        }, 422

    cur.execute("""
        SELECT
            item.price,
            order_item.quantity,
            item.metadata
        FROM order_item
        LEFT JOIN item ON item.key = order_item.item_key
        WHERE order_item.order_key = %s;
    """, (order["key"],))
    items = cur.fetchall()
    if len(items) == 0:
        return {
            "status": 404,
            "error": "invalid request"
        }, 404

    total_order = sum(x["price"] * x["quantity"] for x in items)

    delivery_cost = get_delivery_cost(
        items, order["receiver"]["address"]["area"])

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
                applies_to = delivery_cost

            if coupon["benefit"]["value_unit"] == 'flat':
                discount = coupon["benefit"]["value"]
            elif coupon["benefit"]["value_unit"] == 'percent':
                discount = (applies_to * coupon["benefit"]["value"]) / 100
                discount = round(discount, 2)

            discount = min(discount, applies_to)

    pay = total_order + Decimal(delivery_cost) - Decimal(str(discount))

    cur.execute(
        """SELECT * FROM "order" WHERE payment_reference = %s;""",
        (reference,))
    if cur.fetchone():
        return {
            "status": 400,
            "error": "invalid request"
        }, 400

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
        return {
            "status": 400,
            "error": "invalid transaction"
        }, 400

    cur.execute("""
        INSERT INTO item_version(
            item_key, status, date_created, slug, name,
            tags, price, price_old, information, specification,
            files, variation, quantity, metadata
        )
        SELECT
            i.key, i.status, i.date_created, i.slug, i.name,
            i.tags, i.price, i.price_old, i.information, i.specification,
            i.files, i.variation, i.quantity, i.metadata
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
            AND v.metadata = i.metadata
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
        AND v.variation = i.variation
        AND v.metadata = i.metadata;
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

    prep_time = 0
    for x in items:
        if x["metadata"]["prep_time"] > prep_time:
            prep_time = x["metadata"]["prep_time"]

    order["timeline"]["created"] = f"{datetime.now(timezone.utc)}"
    order["timeline"]["delivery_date"] = f"{datetime.now(
        timezone.utc) + timedelta(days=prep_time)}"

    cur.execute("""
        UPDATE "order"
        SET
            status = 'created',
            order_cost = %s, delivery_cost = %s,
            timeline = %s,
            payment = %s,  payment_reference = %s
        WHERE key = %s RETURNING *;
    """, (
        total_order, delivery_cost, Json(order["timeline"]),
        pay, reference,
        order["key"]
    ))
    order = cur.fetchone()
    cur.execute(
        """INSERT INTO "order" (user_key) VALUES (%s);""",
        (user["key"],)
    )

    if discount > 0:
        cur.execute("""
            UPDATE coupon SET status = 'used'
            WHERE key = %s RETURNING *;
        """, (coupon["key"],))

        cur.execute("""
            INSERT INTO log (
                user_key, action, entity_type, entity_key, misc
            ) VALUES (%s, 'coupon.use', 'coupon', %s, %s);
        """, (
            user["key"], coupon["key"],
            {"entity_type": "order", "entity_key": order["key"]}
        ))

    cur.execute("""
        SELECT email FROM "user"
        WHERE 'order.email.created' = ANY(access);
    """)
    admins_to_notify = cur.fetchall()
    if not admins_to_notify:
        admins_to_notify = [os.environ["MAIL_USERNAME"]]

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

    return {
        "status": 200,
        "order": order,
        "log": {
            "entity_key": order["key"],
        }
    }, 200


@bp.put("/orders/<key>/delivery_date")
@session(True)
@rate_limit(20, 1)
@log("order")
def delivery_date(cur, user, key):
    if "order.edit_delivery_date" not in user["access"]:
        return {
            "status": 403,
            "error": "unauthorized access"
        }, 403

    cur.execute("""SELECT * FROM "order" WHERE key = %s;""", (key,))
    order = cur.fetchone()
    if not order or order["status"] != "created":
        return {
            "status": 404,
            "error": "invalid request"
        }, 404

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
        return {
            "status": 422,
            **error
        }, 422

    previous = order
    order["timeline"]["delivery_date"] = delivery_date

    cur.execute("""
        UPDATE "order" SET timeline = %s
        WHERE key = %s RETURNING *;
    """, (Json(order["timeline"]), order["key"]))
    order = cur.fetchone()

    return {
        "status": 200,
        "order": order,
        "log": {
            "entity_key": order["key"],
            "misc": {
                "from": f"{previous["timeline"]['delivery_date']}",
                "to": f"{order["timeline"]['delivery_date']}",
            }
        }
    }, 200


@bp.put("/orders/<key>/status/processing")
@session(True)
@rate_limit(20, 1)
@log("order")
def processing(cur, user, key):
    if "order.status.processing" not in user["access"]:
        return {
            "status": 403,
            "error": "unauthorized access"
        }, 403

    cur.execute("""SELECT * FROM "order" WHERE key = %s;""", (key,))
    order = cur.fetchone()
    if (
        not order
        or order["status"] not in ("created", "enroute")
    ):
        return {
            "status": 404,
            "error": "invalid request"
        }, 404

    comment = request.json.get("comment", "").strip()
    error = {}
    if not comment:
        error["comment"] = "This field is required"
    elif len(comment) > 500:
        error["comment"] = "This field cannot exceed 500 characters"
    if error:
        return {
            "status": 422,
            **error
        }, 422

    previous = order
    if "enroute" in order["timeline"]:
        del order["timeline"]["enroute"]
    order["timeline"]["processing"] = f"{datetime.now(timezone.utc)}"

    cur.execute("""
        UPDATE "order"
            SET status = 'processing', timeline = %s
        WHERE key = %s RETURNING *;
    """, (Json(order["timeline"]), order["key"]))
    order = cur.fetchone()

    return {
        "status": 200,
        "order": order,
        "log": {
            "entity_key": order["key"],
            "misc": {
                "from": previous['status'],
                "comment": comment
            }
        }
    }, 200


@bp.put("/orders/<key>/status/enroute")
@session(True)
@rate_limit(20, 1)
@log("order")
def enroute(cur, user, key):
    if "order.status.enroute" not in user["access"]:
        return {
            "status": 403,
            "error": "unauthorized access"
        }, 403

    cur.execute("""SELECT * FROM "order" WHERE key = %s;""", (key,))
    order = cur.fetchone()
    if (
        not order
        or order["status"] != "processing"
    ):
        return {
            "status": 404,
            "error": "invalid request"
        }, 404

    comment = request.json.get("comment", "").strip()
    error = {}
    if not comment:
        error["comment"] = "This field is required"
    elif len(comment) > 500:
        error["comment"] = "This field cannot exceed 500 characters"
    if error:
        return {
            "status": 422,
            **error
        }, 422

    previous = order
    order["timeline"]["enroute"] = f"{datetime.now(timezone.utc)}"

    cur.execute("""
        UPDATE "order"
            SET status = 'enroute', timeline = %s
        WHERE key = %s RETURNING *;
    """, (Json(order["timeline"]), order["key"]))
    order = cur.fetchone()

    return {
        "status": 200,
        "order": order,
        "log": {
            "entity_key": order["key"],
            "misc": {
                "from": previous['status'],
                "comment": comment
            }

        }
    }, 200


@bp.put("/orders/<key>/status/delivered")
@session(True)
@rate_limit(20, 1)
@log("order")
def delivered(cur, user, key):
    if "order.status.delivered" not in user["access"]:
        return {
            "status": 403,
            "error": "unauthorized access"
        }, 403

    cur.execute("""SELECT * FROM "order" WHERE key = %s;""", (key,))
    order = cur.fetchone()
    if not order or order["status"] != "enroute":
        return {
            "status": 404,
            "error": "invalid request"
        }, 404

    comment = request.json.get("comment", "").strip()
    email_template_user = request.json.get("email_template_user")
    email_template_admin = request.json.get("email_template_admin")

    cur.execute("""SELECT * FROM "order" WHERE key = %s;""", (key,))
    order = cur.fetchone()

    if not email_template_user or not email_template_admin:
        return {
            "status": 422,
            "error": "invalid request"
        }, 422

    error = {}
    if not comment:
        error["comment"] = "This field is required"
    elif len(comment) > 500:
        error["comment"] = "This field cannot exceed 500 characters"
    if error:
        return {
            "status": 422,
            **error
        }, 422

    previous = order
    order["timeline"]["delivered"] = f"{datetime.now(timezone.utc)}"

    cur.execute("""
        UPDATE "order"
            SET status = 'delivered', timeline = %s
        WHERE key = %s RETURNING *;
    """, (Json(order["timeline"]), order["key"]))
    order = cur.fetchone()

    cur.execute("""
        SELECT * FROM "user" WHERE key = %s;
    """, (order["user_key"],))
    user2 = cur.fetchone()
    send_mail(
        user2["email"],
        "Order Delivered - Thank you",
        email_template_user.format(name=user2["name"])
    )

    cur.execute("""
        SELECT email FROM "user"
        WHERE 'order.email.delivered' = ANY(access);
    """)
    admins = cur.fetchall()
    if admins:
        send_mail(
            [x["email"] for x in admins],
            "Order Delivered",
            email_template_admin.format(
                name=user2["name"],
                username=user2["username"]
            )
        )

    return {
        "status": 200,
        "order": order,
        "log": {
            "entity_key": order["key"],
            "misc": {
                "from": previous['status'],
                "comment": comment
            }
        }
    }, 200


@bp.put("/orders/<key>/status/canceled")
@session(True)
@rate_limit(20, 1)
@log("order")
def canceled(cur, user, key):
    if "order.status.canceled" not in user["access"]:
        return {
            "status": 403,
            "error": "unauthorized access"
        }, 403

    cur.execute("""SELECT * FROM "order" WHERE key = %s;""", (key,))
    order = cur.fetchone()
    if (
        not order
        or order["status"] not in ['created', 'processing', 'enroute']
    ):
        return {
            "status": 404,
            "error": "invalid request"
        }, 404

    comment = request.json.get("comment", "").strip()
    email_template_user = request.json.get("email_template_user")
    email_template_admin = request.json.get("email_template_admin")

    if not email_template_user or not email_template_admin:
        return {
            "status": 422,
            "error": "invalid request"
        }, 422

    error = {}
    if not comment:
        error["comment"] = "This field is required"
    elif len(comment) > 500:
        error["comment"] = "This field cannot exceed 500 characters"
    if error:
        return {
            "status": 422,
            **error
        }, 422

    previous = order
    order["timeline"]["canceled"] = f"{datetime.now(timezone.utc)}"

    cur.execute("""
        UPDATE "order"
        SET status = 'canceled', timeline = %s
        WHERE key = %s RETURNING *;
    """, (Json(order["timeline"]), order["key"]))
    order = cur.fetchone()

    cur.execute(
        """SELECT * FROM "user" WHERE key = %s;""",
        (order["user_key"],))
    user2 = cur.fetchone()
    send_mail(
        user2["email"],
        "Order Canceled",
        email_template_user.format(name=user2["name"])
    )

    cur.execute("""
        SELECT email FROM "user"
        WHERE 'order.email.canceled' = ANY(access);
    """)
    admins = cur.fetchall()
    if admins:
        send_mail(
            [x["email"] for x in admins],
            "Order Canceled",
            email_template_admin.format(
                name=user2["name"],
                username=user2["username"]
            )
        )

    return {
        "status": 200,
        "order": order,
        "log": {
            "entity_key": order["key"],
            "misc": {
                "from": previous['status'],
                "comment": comment
            }

        }
    }, 200


@bp.put("/orders/<key>/status/returning")
@session(True)
@rate_limit(20, 1)
@log("order")
def returning_(cur, user, key):
    cur.execute("""SELECT * FROM "order" WHERE key = %s;""", (key,))
    order = cur.fetchone()
    if (
        not order
        or user["key"] != order["user_key"]
        or order["status"] != "delivered"
    ):
        return {
            "status": 404,
            "error": "invalid request"
        }, 404

    comment = request.json.get("comment", "").strip()
    email_template_user = request.json.get("email_template_user")
    email_template_admin = request.json.get("email_template_admin")

    if not email_template_user or not email_template_admin:
        return {
            "status": 422,
            "error": "invalid request"
        }, 422

    error = {}
    if not comment:
        error["comment"] = "This field is required"
    elif len(comment) > 500:
        error["comment"] = "This field cannot exceed 500 characters"
    if error:
        return {
            "status": 422,
            **error
        }, 422

    if (
        datetime.now(timezone.utc) - datetime.fromisoformat(
            order["timeline"]["delivered"].replace("Z", "+00:00")
        ) > timedelta(days=7)
    ):
        return {
            "status": 422,
            "error": """The order is outside the return window.
                You can only return the order within 7 days of delivery."""
        }, 422

    previous = order
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

    cur.execute("""
        SELECT email FROM "user"
        WHERE 'order.email.returning' = ANY(access);
    """)
    admins = cur.fetchall()
    if admins:
        send_mail(
            [x["email"] for x in admins],
            "Returning Order",
            email_template_admin.format(
                name=user["name"],
                username=user["username"]
            )
        )

    return {
        "status": 200,
        "order": order,
        "log": {
            "entity_key": order["key"],
            "misc": {
                "from": previous['status'],
                "comment": comment
            }
        }
    }, 200


@bp.put("/orders/<key>/status/returned")
@session(True)
@rate_limit(20, 1)
@log("order")
def returned(cur, user, key):
    if "order.status.returned" not in user["access"]:
        return {
            "status": 403,
            "error": "unauthorized access"
        }, 403

    cur.execute("""SELECT * FROM "order" WHERE key = %s;""", (key,))
    order = cur.fetchone()
    if (
        not order
        or order["status"] != "returning"
    ):
        return {
            "status": 404,
            "error": "invalid request"
        }, 404

    comment = request.json.get("comment", "").strip()
    email_template_user = request.json.get("email_template_user")
    email_template_admin = request.json.get("email_template_admin")

    if not email_template_user or not email_template_admin:
        return {
            "status": 422,
            "error": "invalid request"
        }, 422

    error = {}
    if not comment:
        error["comment"] = "This field is required"
    elif len(comment) > 500:
        error["comment"] = "This field cannot exceed 500 characters"
    if error:
        return {
            "status": 422,
            **error
        }, 422

    order["timeline"]["returned"] = f"{datetime.now(timezone.utc)}"
    cur.execute("""
        UPDATE "order"
        SET status = 'returned', timeline = %s
        WHERE key = %s RETURNING *;
    """, (Json(order["timeline"]), order["key"]))
    order = cur.fetchone()

    cur.execute(
        """SELECT * FROM "user" WHERE key = %s;""",
        (order["user_key"],))
    order_user = cur.fetchone()
    send_mail(
        order_user["email"],
        "Order Returned",
        email_template_user.format(name=order_user["name"])
    )

    cur.execute("""
        SELECT email FROM "user"
        WHERE 'order.email.returned' = ANY(access);
    """)
    admins = cur.fetchall()
    if admins:
        send_mail(
            [x["email"] for x in admins],
            "Order Returned",
            email_template_admin.format(
                name=order_user["name"],
                username=order_user["username"]
            )
        )

    return {
        "status": 200,
        "order": order,
        "log": {
            "entity_key": order["key"],
            "misc": {
                "admin": user["key"],
                "comment": comment
            }
        }
    }, 200
