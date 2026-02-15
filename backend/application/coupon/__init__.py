from datetime import datetime, timezone
from uuid import uuid4

from flask import Blueprint, jsonify, request
from psycopg2.extras import Json

from ..log import log
from ..postgres import db_close, db_open
from ..tools import get_session
from .get import (coupon_applies_to, coupon_condition_unit, coupon_schema,
                  coupon_value_unit, get_many)

bp = Blueprint("coupon", __name__)


@bp.post("/coupon")
def add():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "coupon:add" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    applies_to = request.json.get("applies_to")
    value = request.json.get("value")
    value_unit = request.json.get("value_unit")
    condition = request.json.get("condition")
    condition_unit = request.json.get("condition_unit")

    error = {}
    if not applies_to or applies_to not in coupon_applies_to:
        error["applies_to"] = "This field is required"
    if not isinstance(value, int) or value < 1:
        error["value"] = "Please enter a valid number"
    if not value_unit or value_unit not in coupon_value_unit:
        error["value_unit"] = "This field is required"
    if not isinstance(condition, int) or condition < 0:
        error["condition"] = "Please enter a valid number"
    if not condition_unit or condition_unit not in coupon_condition_unit:
        error["condition_unit"] = "This field is required"
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    cur.execute("""
        INSERT INTO coupon (code, benefit) VALUES (%s, %s) RETURNING *;
    """, (
        uuid4().hex[-10:],
        Json({
            "applies_to": applies_to,
            "value": value,
            "value_unit": value_unit,
            "condition": condition,
            "condition_unit": condition_unit,

        })
    ))
    coupon = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="created coupon",
        entity_key=coupon["key"],
        entity_type="coupon"
    )

    coupons = get_many(cur)

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "coupon": coupon_schema(coupon, user["access"]),
        "coupons": coupons.json["coupons"],
        "total_page": coupons.json["total_page"]
    })


@bp.delete("/coupon/<key>")
def delete(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute('SELECT * FROM coupon WHERE key = %s;', (key,))
    coupon = cur.fetchone()
    if not coupon or coupon["status"] == "used":
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    error = {}

    comment = request.json.get("comment")
    if not comment:
        error["note"] = "This field is required"
    elif len(comment) > 500:
        error["comment"] = "This field cannot exceed 500 characters"

    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    cur.execute("""
        DELETE FROM coupon WHERE key = %s;
    """, (coupon["key"],))

    log(
        cur=cur,
        user_key=user["key"],
        action="deleted coupon",
        entity_key=coupon["key"],
        entity_type="coupon",
        misc={"comment": comment}
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.put("/coupon/validity/set/<key>")
def set_validity(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "coupon:edit_validity" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute('SELECT * FROM coupon WHERE key = %s;', (key,))
    coupon = cur.fetchone()
    if not coupon or coupon["status"] == "used":
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    error = {}

    valid_from = request.json.get("valid_from")
    valid_until = request.json.get("valid_until")

    try:
        valid_from = datetime.strptime(valid_from, "%Y-%m-%d").date()
    except Exception:
        error["valid_from"] = "invalid input"

    try:
        valid_until = datetime.strptime(valid_until, "%Y-%m-%d").date()
    except Exception:
        error["valid_until"] = "invalid input"

    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    if (
        coupon["valid_from"]
        and (valid_from.strftime("%Y-%m-%d"))
        == coupon["valid_from"].strftime("%Y-%m-%d")
        and coupon["valid_until"]
        and valid_until.strftime("%Y-%m-%d")
        == coupon["valid_until"].strftime("%Y-%m-%d")
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "No changes were made"
        })

    if valid_from < datetime.now(timezone.utc).date():
        error["valid_from"] = "Cannot set date in the past"
    if (valid_until) <= valid_from:
        error["valid_until"] = 'Cannot set date earlier or equal to start date'
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    old_coupon = coupon
    cur.execute("""
        UPDATE coupon SET status = 'active', valid_from = %s, valid_until = %s
        WHERE key = %s RETURNING *;
    """, (valid_from, valid_until, coupon["key"]))
    coupon = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="changed coupon validity",
        entity_key=coupon["key"],
        entity_type="coupon",
        misc={
            "from": f'{old_coupon[
                "valid_from"]} - {old_coupon["valid_until"]}',
            "to": f'{coupon["valid_from"]} - {coupon["valid_until"]}',
        }
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "coupon": coupon_schema(coupon, user["access"])
    })


@bp.put("/coupon/validity/clear/<key>")
def clear_validity(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "coupon:edit_validity" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute('SELECT * FROM coupon WHERE key = %s;', (key,))
    coupon = cur.fetchone()
    if not coupon or coupon["status"] == "used":
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    old_coupon = coupon
    cur.execute("""
        UPDATE coupon SET status = 'inactive',
            valid_from = NULL, valid_until = NULL
        WHERE key = %s RETURNING *;
    """, (coupon["key"],))
    coupon = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="cleared coupon validity",
        entity_key=coupon["key"],
        entity_type="coupon",
        misc={
            "from": f'{old_coupon[
                "valid_from"]} - {old_coupon["valid_until"]}',
        }
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "coupon": coupon_schema(coupon, user["access"])
    })


@bp.put("/coupon/cart/add")
def add_coupon_to_cart():
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
        entity_key=coupon["key"],
        entity_type="coupon",
        misc={"cart_key": cart["key"]}
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "coupon": coupon_schema(coupon, user["access"])
    })


@bp.put("/coupon/cart/remove")
def remove_coupon_from_cart():
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
        action="removed coupon to cart",
        entity_key=coupon["key"],
        entity_type="coupon",
        misc={"cart_key": cart["key"]}
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "coupon": None
    })
