from flask import Blueprint, jsonify, request
from .tools import token_to_user, user_schema
from uuid import uuid4
from math import ceil
from datetime import datetime, date
from .postgres import db_close, db_open
import json

bp = Blueprint("voucher", __name__)


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

        cur.execute("""
            INSERT INTO log (
                key, date, user_key, action, entity_key, entity_type, misc
            ) VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (
            uuid4().hex,
            datetime.now(),
            user["key"],
            "created",
            voucher_key,
            "voucher",
            json.dumps({"batch": batch})
        ))

    db_close(con, cur)

    return jsonify({
        "status": 200,
        **get_many()
    })


@bp.get("/voucher")
def get_many():
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
    sort = request.args["sort"] if "sort" in request.args else "latest"
    page_no = int(request.args["page_no"]) if "page_no" in request.args else 1
    page_size = int(request.args["page_size"]
                    ) if "page_size" in request.args else 24

    order_by = {
        'latest': 'log.date',
        'oldest': 'log.date',
        'high_value': 'voucher.value',
        'low_value': 'voucher.value'
    }

    order_dir = {
        'latest': 'DESC',
        'oldest': 'ASC',
        'high_value': 'DESC',
        'low_value': 'ASC'
    }

    cur.execute("""
        SELECT
            voucher.*,
            log.date AS date,
            COUNT(*) OVER() AS total_items
        FROM voucher
        LEFT JOIN log ON voucher.key = log.entity_key
            AND log.action = 'created'
            AND log.entity_type = 'voucher'
        WHERE
            (%s = '' OR voucher.status = %s)
            AND (%s = '' OR voucher.key ILIKE %s)
        ORDER BY {} {}
        LIMIT %s OFFSET %s;
    """.format(
        order_by[sort], order_dir[sort]
    ), (
        status, status,
        search, f'%{search}%',
        page_size,
        (page_no - 1) * page_size
    ))
    vouchers = cur.fetchall()

    db_close(con, cur)

    return {
        "status": 200,
        "vouchers": vouchers,
        "total_page": ceil(vouchers[0][
            "total_items"] / page_size) if vouchers else 0
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

    cur.execute("""
        SELECT voucher.*, log.date AS date
        FROM voucher
        LEFT JOIN log ON voucher.key = log.entity_key
            AND log.action = 'created'
            AND log.entity_type = 'voucher'
        WHERE voucher.key = %s;
    """, (key,))
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
        "voucher": voucher,
    })


@ bp.put("/voucher/activate/<key>")
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
        SET status = 'active', validity = %s
        WHERE key = %s;
    """, (
        validity,
        voucher["key"]
    ))

    cur.execute("""
        SELECT voucher.*, log.date AS date
        FROM voucher
        LEFT JOIN log ON voucher.key = log.entity_key
            AND log.action = 'created'
            AND log.entity_type = 'voucher'
        WHERE voucher.key = %s;
    """, (voucher["key"],))
    voucher = cur.fetchone()

    cur.execute("""
        INSERT INTO log (
            key, date, user_key, action, entity_key, entity_type, misc
        ) VALUES (%s, %s, %s, %s, %s, %s, %s);
    """, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "activated",
        voucher["key"],
        "voucher",
        json.dumps({"validity": validity})
    ))

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "voucher": voucher
    })


@ bp.put("/voucher/status/<key>")
def status(key):
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

    if (
        not voucher
        or "status" not in request.json
        or request.json["status"] not in ["deactivate", "delete"]
        or (
            request.json["status"] == "deactivate"
            and voucher["status"] != "active"
        )
        or (
            request.json["status"] == "delete"
            and voucher["status"] != "inactive"
        )
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("""
        UPDATE voucher
        SET status = %s, validity = NULL
        WHERE key = %s;
    """, (
        "deleted" if request.json["status"] == "delete" else "inactive",
        voucher["key"]
    ))

    cur.execute("""
        SELECT voucher.*, log.date AS date
        FROM voucher
        LEFT JOIN log ON voucher.key = log.entity_key
            AND log.action = 'created'
            AND log.entity_type = 'voucher'
        WHERE voucher.key = %s;
    """, (voucher["key"],))
    voucher = cur.fetchone()

    cur.execute("""
        INSERT INTO log (
            key, date, user_key, action, entity_key, entity_type
        ) VALUES (%s, %s, %s, %s, %s, %s);
    """, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "deactivated",
        voucher["key"],
        "voucher"
    ))

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "voucher": voucher
    })


@bp.post("/voucher/use")
def use():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "pin" not in request.json or not request.json["pin"]:
        return jsonify({
            "status": 400,
            "error": "this field is required"
        })

    cur.execute('SELECT * FROM voucher WHERE code = %s;',
                (request.json["pin"].lower(),))
    voucher = cur.fetchone()
    if not voucher or len(request.json["pin"]) != 10:
        return jsonify({
            "status": 400,
            "error": "invalid pin"
        })

    if (
        voucher["status"] != "active"
        or voucher['validity'].date() < date.today()
    ):
        error = f"voucher {voucher['status']}"

        cur.execute("""
            INSERT INTO log (
                key, date, user_key, action, entity_key,
                entity_type, status, misc
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """, (
            uuid4().hex,
            datetime.now(),
            user["key"],
            "used",
            voucher["key"],
            "voucher",
            400,
            json.dumps({"error": error})
        ))

        return jsonify({
            "status": 400,
            "error": error
        })

    cur.execute("""
    INSERT INTO log (
            key, date, user_key, action, entity_key, entity_type, misc
        ) VALUES (%s, %s, %s, %s, %s, %s, %s);
    """, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "used",
        voucher["key"],
        "voucher",
        json.dumps({
            "value": voucher["value"],
            "balance": user["account_balance"],
            "new_balance": user["account_balance"] + voucher["value"]
        })
    ))

    cur.execute("""
        UPDATE voucher
        SET status = 'used'
        WHERE key = %s;
    """, (voucher["key"],))

    cur.execute("""
        UPDATE "user"
        SET account_balance = "user".account_balance + %s
        WHERE key = %s
        RETURNING *;
    """, (
        voucher["value"],
        user["key"]
    ))
    user = cur.fetchone()

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })
