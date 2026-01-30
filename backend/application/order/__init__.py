from flask import Blueprint, jsonify, request
from ..tools import get_session, send_mail
from ..postgres import db_open, db_close
from ..storage import storage
from ..log import log
import os
import requests
from ..cart.get import get_cart_items
from .get import order_status
from datetime import datetime, timezone, timedelta
from psycopg2.extras import Json

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
            item.quantity AS available_quantity,
            item.status,
            order_item.quantity
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
        # TEST: check item availability
        # TODO: match messaging to frontend message
        # FIXME: HOW ABOUT IF ITEM IS DELETED?
        if (
            x["status"] != 'active'
            or x["quantity"] == 0
            or x["quantity"] > x["available_quantity"]
        ):
            return jsonify({
                "status": 400,
                "error": "Some items in your cart are no longer available"
            })

    pay = order["cost_delivery"]
    for x in items:
        pay += x["price"] * x["quantity"]

    # FEATURE: check Coupons here

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
        WHERE 'order:email_order_created' = ANY(access);
    """)
    admins = cur.fetchall()

    reference = request.json.get("reference")
    email_template_admin = request.json.get("email_template_admin")
    email_template_user = request.json.get("email_template_user")

    if (
        not order
        or admins == []
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

    pay = order["cost_delivery"]
    for x in items:
        pay += x["price"] * x["order_quantity"]

    # FEATURE: spend / use Coupons here

    cur.execute(
        """SELECT * FROM "order" WHERE pay_reference = %s;""",
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

    values_list = []
    for row in items:
        row["item_key"] = row["key"]
        row["order_key"] = order["key"]
        del row["key"]
        del row["order_quantity"]

        for x in row["files"]:
            storage.copy(x, "item", "item_snap")

        columns = list(row.keys())
        values = []
        for column in columns:
            if type(row[column]) is dict:
                row[column] = Json(row[column])
            values.append(row[column])
        values_list.append(tuple(values))

    cur.executemany(f"""
        INSERT INTO item_snap({', '.join(columns)})
        VALUES ({', '.join(['%s'] * len(columns))});
    """, values_list)

    order["timeline"]["created"] = f"{datetime.now(timezone.utc)}"
    order["timeline"]["delivery_date"
                      ] = f"{datetime.now(timezone.utc) + timedelta(days=7)}"

    cur.execute("""
        UPDATE "order"
        SET
            status = 'created',
            cost_items = %s, timeline = %s,
            pay_user = %s,  pay_reference = %s
        WHERE key = %s RETURNING *;
    """, (
        pay, Json(order["timeline"]),
        pay, reference,
        order["key"]
    ))
    order = cur.fetchone()
    get_cart_items(cur)

    log(
        cur=cur,
        user_key=user["key"],
        action="created order",
        entity_key=order["key"],
        entity_type="order"
    )

    send_mail(
        user["email"],
        "Processing Order",
        email_template_user.format(name=user["name"])
    )
    send_mail(
        [x["email"] for x in admins],
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


@bp.put("/order/delivery_date/<key>")
def delivery_date(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "order:edit_delivery_date" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
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
    # TODO: prevent backdating in frontend also
    delivery_date = request.json.get("delivery_date", "").strip()
    if not delivery_date or type(delivery_date) is not str:
        error["delivery_date"] = "This field is required"
    elif delivery_date == order["timeline"]["delivery_date"]:
        error["delivery_date"] = "No changes were made"
    else:
        try:
            datetime.strptime(delivery_date, "%Y-%m-%dT%H:%M:%S")
        except Exception:
            error["error"] = "invalid request"

    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    log(
        cur=cur,
        user_key=user["key"],
        action="changed order delivery date",
        entity_key=order["key"],
        entity_type="order",
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


@bp.put("/order/cancel/<key>")
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

    if "order:cancel" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
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

    comment = request.json.get("comment")
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
    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    log(
        cur=cur,
        user_key=user["key"],
        action="canceled order",
        entity_key=order["key"],
        entity_type="order",
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


@bp.put("/order/status/<key>")
def status(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "order:edit_status" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
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
        WHERE 'order:email_order_delivered' = ANY(access);
    """)
    admins = cur.fetchall()

    status = request.json.get("status")
    comment = request.json.get("comment")
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
    if error != {}:
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
        entity_key=order["key"],
        entity_type="order",
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
