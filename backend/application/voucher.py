from flask import Blueprint, jsonify, request
from .tools import token_to_user, user_schema
from uuid import uuid4
from math import ceil
from datetime import datetime, date, timedelta
from .postgres import db_close, db_open
from .log import log, get_voucher_log

bp = Blueprint("voucher", __name__)


@bp.post("/voucher")
def create():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })
    if "voucher:add" not in user["permissions"]:
        db_close(con, cur)
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
        db_close(con, cur)
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
            INSERT INTO voucher (key, version, batch, pin, value)
            VALUES (%s, %s, %s, %s, %s);
        """, (
            voucher_key,
            uuid4().hex,
            batch,
            str(uuid4().hex)[:10],
            request.json["value"]
        ))

        log(
            cur=cur,
            user_key=user["key"],
            action="created",
            entity_key=voucher_key,
            entity_type="voucher",
            misc={"batch": batch}
        )

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
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "voucher:view" not in user["permissions"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

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

    order = list(order_by.keys())[0]
    status = ""
    search = ""
    page_no = 1
    page_size = 24

    if "status" in request.args:
        status = request.args["status"]
    if "search" in request.args:
        search = request.args["search"].strip()
    if "order" in request.args:
        order = request.args["order"]
    if "page_no" in request.args:
        page_no = int(request.args["page_no"])
    if "page_size" in request.args:
        page_size = int(request.args["page_size"])

    cur.execute("""
        SELECT
            voucher.key,
            voucher.status,
            voucher.value,
            log.date AS date,
            COUNT(*) OVER() AS total_items
        FROM voucher
        LEFT JOIN log ON voucher.key = log.entity_key
        WHERE
            (%s = '' OR voucher.status = %s)
            AND (%s = '' OR voucher.key ILIKE %s)
            AND log.action = 'created'
            AND log.entity_type = 'voucher'
        ORDER BY {} {}
        LIMIT %s OFFSET %s;
    """.format(
        order_by[order], order_dir[order]
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
        "order_by": list(order_by.keys()),
        "voucher_status": ["created", 'activated', "deactivated",
                           'used', 'deleted', 'expired'],
        "total_page": ceil(vouchers[0][
            "total_items"] / page_size) if vouchers else 0
    }


@ bp.get("/voucher/<key>")
def get(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })
    if "voucher:view" not in user["permissions"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute("""
        SELECT voucher.*, log.date AS date
        FROM voucher
        LEFT JOIN log ON voucher.key = log.entity_key
        WHERE
            voucher.key = %s
            AND log.action = 'created'
            AND log.entity_type = 'voucher';
    """, (key,))
    voucher = cur.fetchone()
    if not voucher:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if "voucher:view_pin" not in user["permissions"]:
        voucher["pin"] = "#"

    logs = []
    if "log:view" in user["permissions"]:
        logs = get_voucher_log(cur, voucher["key"])

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "voucher": voucher,
        "logs": logs
    })


@ bp.put("/voucher/activate/<key>")
def activate(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "voucher:status" not in user["permissions"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    if "validity" not in request.json or not request.json["validity"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "this field is required"
        })

    if (
        type(request.json["validity"]) is not int
        or request.json["validity"] < 1
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "please enter a valid number"
        })

    validity = datetime.now() + timedelta(days=request.json["validity"])
    validity = validity.replace(hour=23, minute=59, second=59, microsecond=999)

    cur.execute('SELECT * FROM voucher WHERE key = %s;', (key,))
    voucher = cur.fetchone()
    if not voucher or voucher["status"] not in ["created", "deactivated"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("""
        UPDATE voucher
        SET status = 'activated', validity = %s
        WHERE key = %s;
    """, (
        validity,
        voucher["key"]
    ))

    cur.execute("""
        SELECT voucher.*, log.date AS date
        FROM voucher
        LEFT JOIN log ON voucher.key = log.entity_key
        WHERE
            voucher.key = %s
            AND log.action = 'created'
            AND log.entity_type = 'voucher';
    """, (voucher["key"],))
    voucher = cur.fetchone()

    if "voucher:view_pin" not in user["permissions"]:
        voucher["pin"] = "#"

    log(
        cur=cur,
        user_key=user["key"],
        action="activated",
        entity_key=voucher["key"],
        entity_type="voucher",
        misc={"validity": f"{validity}"}
    )

    logs = []
    if "log:view" in user["permissions"]:
        logs = get_voucher_log(cur, voucher["key"])

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "voucher": voucher,
        "logs": logs
    })


@ bp.put("/voucher/status/<key>")
def status(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "voucher:status" not in user["permissions"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    if "note" not in request.json or not request.json["note"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "this field is required"
        })

    cur.execute('SELECT * FROM voucher WHERE key = %s;', (key,))
    voucher = cur.fetchone()

    if (
        not voucher
        or "status" not in request.json
        or request.json["status"] not in ["deactivated", "deleted"]
        or (
            request.json["status"] == "deactivated"
            and voucher["status"] != "activated"
        )
        or (
            request.json["status"] == "deleted"
            and voucher["status"] not in ["created", "deactivated"]
        )
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("""
        UPDATE voucher
        SET status = %s, validity = NULL
        WHERE key = %s;
    """, (
        request.json["status"],
        voucher["key"]
    ))

    cur.execute("""
        SELECT voucher.*, log.date AS date
        FROM voucher
        LEFT JOIN log ON voucher.key = log.entity_key
        WHERE
            voucher.key = %s
            AND log.action = 'created'
            AND log.entity_type = 'voucher';
    """, (voucher["key"],))
    voucher = cur.fetchone()

    if "voucher:view_pin" not in user["permissions"]:
        voucher["pin"] = "#"

    log(
        cur=cur,
        user_key=user["key"],
        action=request.json["status"],
        entity_key=voucher["key"],
        entity_type="voucher",
        misc={"note": request.json["note"]}
    )

    logs = []
    if "log:view" in user["permissions"]:
        logs = get_voucher_log(cur, voucher["key"])

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "voucher": voucher,
        "logs": logs
    })


@bp.post("/voucher/use")
def use():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "pin" not in request.json or not request.json["pin"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "this field is required"
        })

    cur.execute('SELECT * FROM voucher WHERE pin = %s;',
                (request.json["pin"].lower(),))
    voucher = cur.fetchone()
    if not voucher or len(request.json["pin"]) != 10:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid pin"
        })

    if (
        voucher["status"] != "activated"
        or voucher['validity'].date() < date.today()
    ):
        error = "voucher is not active"

        log(
            cur=cur,
            user_key=user["key"],
            action="used",
            entity_key=voucher["key"],
            entity_type="voucher",
            status=400,
            misc={"error": error}
        )
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": error
        })

    log(
        cur=cur,
        user_key=user["key"],
        action="used",
        entity_key=voucher["key"],
        entity_type="voucher",
        misc={
            "value": voucher["value"],
            "balance": user["account_balance"],
            "new_balance": user["account_balance"] + voucher["value"]
        }
    )

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
