from datetime import datetime
from uuid import uuid4

from flask import Blueprint, jsonify, request
from psycopg2.extras import Json

from ..log import log
from ..postgres import db_close, db_open
from ..tools import get_session
from .get import (coupon_schema, for_list, get_many, threshold_unit_list,
                  value_unit_list)

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

    _for = request.json.get("for")
    value = request.json.get("value")
    value_unit = request.json.get("value_unit")
    threshold = request.json.get("threshold")
    threshold_unit = request.json.get("threshold_unit")

    error = {}
    if not _for or _for not in for_list:
        error["for"] = "This field is required"
    if not isinstance(value, int) or value < 1:
        error["value"] = "Please enter a valid number"
    if not value_unit or value_unit not in value_unit_list:
        error["value_unit"] = "This field is required"
    if not isinstance(threshold, int) or threshold < 0:
        error["threshold"] = "Please enter a valid number"
    if not threshold_unit or threshold_unit not in threshold_unit_list:
        error["threshold_unit"] = "This field is required"
    if error != {}:
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
            "for": _for,
            "value": value,
            "value_unit": value_unit,
            "threshold": threshold,
            "threshold_unit": threshold_unit,

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
        "coupon": coupon_schema(coupon),
        "coupons": coupons.json["coupons"],
        "total_page": coupons.json["total_page"]
    })


@bp.put("/coupon/validity/<key>")
def edit(key):
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
    if not coupon:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    error = {}

    valid_from = request.json.get("valid_from")
    valid_until = request.json.get("valid_until")

    if not valid_from:
        error["valid_from"] = "This field is required"
    elif valid_from == coupon["valid_from"]:
        error["valid_from"] = "No changes were made"
    else:
        try:
            datetime.strptime(valid_from, "%Y-%m-%dT%H:%M:%S")
        except Exception:
            error["valid_from"] = "invalid input"

    if not valid_until:
        error["valid_until"] = "This field is required"
    elif valid_until == coupon["valid_until"]:
        error["valid_until"] = "No changes were made"
    else:
        try:
            datetime.strptime(valid_until, "%Y-%m-%dT%H:%M:%S")
        except Exception:
            error["valid_until"] = "invalid input"

    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    old_coupon = coupon
    cur.execute("""
        UPDATE coupon SET valid_from = %s, valid_until = %s
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
        "coupon": coupon_schema(coupon)
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
    if not coupon:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    error = {}

    note = coupon["note"]
    if not note:
        error["note"] = "This field is required"

    if error != {}:
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
        misc={"note": note}
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
