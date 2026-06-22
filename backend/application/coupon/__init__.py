from datetime import datetime, timezone
from uuid import uuid4

from flask import Blueprint, request
from psycopg2.extras import Json

from ..log import log
from ..postgres import db_close, db_open
from ..tools import get_session
from .get import (coupon_applies_to, coupon_condition_unit, coupon_schema,
                  coupon_value_unit, get_many)

bp = Blueprint("coupon", __name__)


@bp.post("/coupons")
def add():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return session
    user = session["user"]

    if "coupon.add" not in user["access"]:
        db_close(con, cur)
        return {
            "status": 403,
            "error": "unauthorized access"
        }, 403

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
        return {
            "status": 400,
            **error
        }, 400

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
        entity_type="coupon",
        entity_key=coupon["key"],
    )

    coupons = get_many(cur)

    db_close(con, cur)
    return {
        "status": 200,
        "coupon": coupon_schema(coupon, user["access"]),
        "coupons": coupons.json["coupons"],
        "total_page": coupons.json["total_page"]
    }, 200


@bp.delete("/coupons/<key>")
def delete(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return session
    user = session["user"]

    cur.execute('SELECT * FROM coupon WHERE key = %s;', (key,))
    coupon = cur.fetchone()
    if not coupon or coupon["status"] == "used":
        db_close(con, cur)
        return {
            "status": 400,
            "error": "Invalid request"
        }, 400

    error = {}

    comment = request.json.get("comment", "").strip()
    if not comment:
        error["note"] = "This field is required"
    elif len(comment) > 500:
        error["comment"] = "This field cannot exceed 500 characters"

    if error:
        db_close(con, cur)
        return {
            "status": 400,
            **error
        }, 400

    cur.execute("""
        DELETE FROM coupon WHERE key = %s;
    """, (coupon["key"],))

    log(
        cur=cur,
        user_key=user["key"],
        action="deleted coupon",
        entity_type="coupon",
        entity_key=coupon["key"],
        misc={"comment": comment}
    )

    db_close(con, cur)
    return {
        "status": 200
    }, 200


@bp.put("/coupons/<key>/validity")
def set_validity(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return session
    user = session["user"]

    if "coupon.edit_validity" not in user["access"]:
        db_close(con, cur)
        return {
            "status": 403,
            "error": "unauthorized access"
        }, 403

    cur.execute('SELECT * FROM coupon WHERE key = %s;', (key,))
    coupon = cur.fetchone()
    if not coupon or coupon["status"] == "used":
        db_close(con, cur)
        return {
            "status": 400,
            "error": "Invalid request"
        }, 400

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
        return {
            "status": 400,
            **error
        }, 400

    if (
        coupon["valid_from"]
        and (valid_from.strftime("%Y-%m-%d"))
        == coupon["valid_from"].strftime("%Y-%m-%d")
        and coupon["valid_until"]
        and valid_until.strftime("%Y-%m-%d")
        == coupon["valid_until"].strftime("%Y-%m-%d")
    ):
        db_close(con, cur)
        return {
            "status": 400,
            "error": "No changes were made"
        }, 400

    if valid_from < datetime.now(timezone.utc).date():
        error["valid_from"] = "Cannot set date in the past"
    if (valid_until) <= valid_from:
        error["valid_until"] = 'Cannot set date earlier or equal to start date'
    if error:
        db_close(con, cur)
        return {
            "status": 400,
            **error
        }, 400

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
        entity_type="coupon",
        entity_key=coupon["key"],
        misc={
            "from": f'{old_coupon[
                "valid_from"]} - {old_coupon["valid_until"]}',
            "to": f'{coupon["valid_from"]} - {coupon["valid_until"]}',
        }
    )

    db_close(con, cur)
    return {
        "status": 200,
        "coupon": coupon_schema(coupon, user["access"])
    }, 200


@bp.delete("/coupons/<key>/validity")
def clear_validity(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return session
    user = session["user"]

    if "coupon.edit_validity" not in user["access"]:
        db_close(con, cur)
        return {
            "status": 403,
            "error": "unauthorized access"
        }, 403

    cur.execute('SELECT * FROM coupon WHERE key = %s;', (key,))
    coupon = cur.fetchone()
    if not coupon or coupon["status"] == "used":
        db_close(con, cur)
        return {
            "status": 400,
            "error": "Invalid request"
        }, 400

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
        entity_type="coupon",
        entity_key=coupon["key"],
        misc={
            "from": f'{old_coupon[
                "valid_from"]} - {old_coupon["valid_until"]}',
        }
    )

    db_close(con, cur)
    return {
        "status": 200,
        "coupon": coupon_schema(coupon, user["access"])
    }, 200
