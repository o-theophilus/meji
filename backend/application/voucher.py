from flask import Blueprint, jsonify, request
from .tools import token_to_user
from uuid import uuid4
from .schema import user_schema
from .log import log_template
from math import ceil
from datetime import datetime, date
from .postgres import db_close, db_open

bp = Blueprint("voucher", __name__)


def voucher_schema(voucher):
    return {
        "key": voucher["key"],
        "code": voucher["code"],
        "date": voucher["date_c"],
        "value": voucher["value"],
        "validity": voucher["validity"],
        "status": voucher["status"],
    }


@bp.post("/voucher")
def create():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })
    if "voucher:add" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    error = {}

    if "value" not in request.json or not request.json["value"]:
        error["value"] = "this field is required"
    elif (
        type(request.json["value"]) not in [int, float]
        or request.json["value"] <= 0
    ):
        error["value"] = "please enter a valid value"

    if "quantity" not in request.json or not request.json["quantity"]:
        error["quantity"] = "this field is required"
    elif (
        type(request.json["quantity"]) is not int
        or request.json["quantity"] < 1
    ):
        error["quantity"] = "please enter a valid quantity"

    if error != {}:
        return jsonify({
            "status": 400,
            **error
        })

    batch = None
    if request.json["quantity"] > 1:
        batch = uuid4().hex

    for x in range(request.json["quantity"]):
        voucher_key = uuid4().hex
        cur.execute("""
            INSERT INTO voucher (key, version, batch, code, value)
            VALUES (%s, %s, %s, %s, %s);
        """, (
            voucher_key,
            uuid4().hex,
            batch,
            str(uuid4().hex)[:10],
            request.json["value"]
        ))

        cur.execute(log_template, (
            uuid4().hex,
            datetime.now(),
            user["key"],
            "created",
            voucher_key,
            "voucher",
            200,
            {"batch": batch}
        ))

    db_close(con, cur)

    return jsonify({
        "status": 200,
        **get_vouchers()
    })


@bp.get("/voucher")
def get_vouchers():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "voucher:view" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    status = request.args["status"] if "status" in request.args else ""
    search = request.args["search"] if "search" in request.args else ""
    page_no = int(request.args["page_no"]) if "page_no" in request.args else 1
    page_size = int(request.args["page_size"]
                    ) if "page_size" in request.args else 24
    sort_order = "DESC" if True else "ASC"
    sort_by = "date"

    cur.execute("""
        SELECT voucher.*, COUNT(*) OVER() AS total_items
        FROM (
            SELECT *
            FROM voucher
            WHERE status = %s AND key ILIKE %s
        ) AS voucher
        LEFT JOIN log ON voucher.key = log.entity_key
            AND log.action = 'created'
            AND log.entity_type = 'voucher'
        ORDER BY
            CASE %s
                WHEN 'value' THEN voucher.value
                WHEN 'date' THEN log.date
                ELSE log.date
            END
            %s
        LIMIT %s OFFSET %s;
    """, (
        status,
        f'%{search}%',
        sort_order,
        sort_by,
        page_size,
        (page_no - 1) * page_size
    ))
    vouchers = cur.fetchall()

    db_close(con, cur)

    return {
        "status": 200,
        "vouchers": [voucher_schema(x) for x in vouchers],
        "total_page": ceil(vouchers[0][-1] / page_size) if vouchers else 0
    }


@ bp.get("/voucher/<key>")
def get(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })
    if "voucher:view" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute('SELECT * FROM voucher WHERE key = %s;', (key,))
    voucher = cur.fetchone()
    if not voucher:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if "voucher:view_code" not in user["roles"]:
        voucher["code"] = "#"

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "voucher": voucher_schema(voucher),
    })


@ bp.put("/voucher/<key>")
def activate(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "voucher:status" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    if "validity" not in request.json or not request.json["validity"]:
        return jsonify({
            "status": 400,
            "error": "this field is required"
        })

    validity = request.json["validity"]

    if (
        len(validity) != 10
        or validity[4] != validity[7] != '-'
        or not validity[:4].isdigit()
        or not validity[5:7].isdigit()
        or not validity[8:].isdigit()
    ):
        return jsonify({
            "status": 400,
            "error": "invalid date format"
        })

    if datetime.strptime(validity, '%Y-%m-%d').date() < date.today():
        return jsonify({
            "status": 400,
            "error": 'cannot be back dated'
        })

    cur.execute('SELECT * FROM voucher WHERE key = %s;', (key,))
    voucher = cur.fetchone()
    if not voucher or voucher["status"] != "inactive":
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("""
            UPDATE voucher
            SET status = %s, validity = %s
            WHERE key = %s;
        """, (
        "active",
        validity,
        voucher["key"]
    ))

    cur.execute(log_template, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "activated",
        voucher["key"],
        "voucher",
        200,
        {
            "validity": validity
        }
    ))

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "voucher": voucher_schema(voucher)
    })


@ bp.put("/voucher_/<key>")
def inactivate(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "voucher:status" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute('SELECT * FROM voucher WHERE key = %s;', (key,))
    voucher = cur.fetchone()
    if not voucher or voucher["status"] != "active":
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("""
            UPDATE voucher
            SET status = %s, validity = %s
            WHERE key = %s;
        """, (
        "inactive",
        None,
        voucher["key"]
    ))

    cur.execute(log_template, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "deactivated",
        voucher["key"],
        "voucher",
        200,
        None
    ))

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "voucher": voucher_schema(voucher)
    })


@ bp.delete("/voucher/<key>")
def delete(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "voucher:status" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute('SELECT * FROM voucher WHERE key = %s;', (key,))
    voucher = cur.fetchone()
    if not voucher or voucher["status"] != "inactive":
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("""
            UPDATE voucher
            SET status = %s, validity = %s
            WHERE key = %s;
        """, (
        "deleted",
        None,
        voucher["key"]
    ))

    cur.execute(log_template, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "deleted",
        voucher["key"],
        "voucher",
        200,
        None
    ))

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "voucher": voucher_schema(voucher)
    })


@bp.post("/use_voucher")
def use():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "code" not in request.json or not request.json["code"]:
        return jsonify({
            "status": 400,
            "error": "this field is required"
        })

    cur.execute('SELECT * FROM voucher WHERE code = %s;',
                (request.json["code"].lower(),))
    voucher = cur.fetchone()
    if not voucher or len(request.json["code"]) != 10:
        return jsonify({
            "status": 400,
            "error": "invalid code"
        })

    if (
        voucher["status"] != "active"
        or datetime.strptime(
            voucher["validity"], '%Y-%m-%d').date() < date.today()
    ):
        error = f"voucher {voucher['status']}"

        cur.execute(log_template, (
            uuid4().hex,
            datetime.now(),
            user["key"],
            "used",
            voucher["key"],
            "voucher",
            400,
            {"error": error}
        ))

        return jsonify({
            "status": 400,
            "error": error
        })

    cur.execute(log_template, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "used",
        voucher["key"],
        "voucher",
        200,
        {
            "value": voucher["value"],
            "balance": user["acc_balance"],
            "new_balance": user["acc_balance"] + voucher["value"]
        }
    ))

    cur.execute("""
            UPDATE "user"
            SET acc_balance = %s
            WHERE key = %s
            RETURNING *;
        """, (
        user["acc_balance"] + voucher["value"],
        voucher["key"]
    ))
    user = cur.fetchone()

    cur.execute("""
            UPDATE voucher
            SET status = %s
            WHERE key = %s;
        """, (
        "used",
        voucher["key"]
    ))

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })
