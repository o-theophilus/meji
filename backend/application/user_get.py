from flask import Blueprint, request, jsonify
from .tools import token_to_user, user_schema
from math import ceil
from .postgres import db_close, db_open
from .admin import permissions


bp = Blueprint("user_get", __name__)


@bp.get("/user")
def get():
    con, cur = db_open()

    me = token_to_user(cur)
    if not me:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    user = None
    if "search" in request.args:

        if "user:view" not in me["permissions"]:
            db_close(con, cur)
            return jsonify({
                "status": 400,
                "error": "unauthorized access"
            })

        if request.args["search"]:
            cur.execute("""
                SELECT *
                FROM "user"
                WHERE key = %s OR email = %s;
            """, (
                request.args["search"],
                request.args["search"]
            ))
            user = cur.fetchone()

            if user and "user:view_balance" not in me["permissions"]:
                user["acc_balance"] = "#"

        if not user:
            db_close(con, cur)
            return jsonify({
                "status": 400,
                "error": "user not found"
            })

    else:
        user = me

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user),
        "permissions": permissions
    })


@bp.get("/users")
def get_many():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "user:view" not in user["permissions"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    status = request.args["status"] if "status" in request.args else ""
    search = request.args["search"] if "search" in request.args else ""
    order = request.args["order"] if "order" in request.args else "latest"
    page_no = int(request.args["page_no"]) if "page_no" in request.args else 1
    page_size = int(request.args["size"]) if "size" in request.args else 24

    order_by = {
        'latest': 'log.date',
        'oldest': 'log.date',
        'name (a-z)': '"user".name',
        'name (z-a)': '"user".name'
    }

    order_dir = {
        'latest': 'DESC',
        'oldest': 'ASC',
        'name (a-z)': 'ASC',
        'name (z-a)': 'DESC'
    }

    cur.execute("""
        SELECT
            "user".*,
            log.date AS date,
            COUNT(*) OVER() AS total_items
        FROM "user"
        LEFT JOIN log ON "user".key = log.user_key
        WHERE
            (
                %s = '' OR "user".status = %s
            ) AND (
                %s = ''
                OR CONCAT_WS(', ', "user".key, "user".name, "user".email
                ) ILIKE %s
            )
            AND log.action = 'created'
            AND log.entity_type = 'auth'
        ORDER BY {} {}
        LIMIT %s OFFSET %s;
    """.format(
        order_by[order], order_dir[order]
    ), (
        status, status,
        search, f"%{search}%",
        page_size, (page_no - 1) * page_size
    ))
    users = cur.fetchall()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "users": [user_schema(x) for x in users],
        "order_by": list(order_by.keys()),
        "user_status": ['anonymous', 'signedup', 'confirmed'],
        "total_page": ceil(users[0]["total_items"] / page_size) if users else 0
    })


def trx_schema(x):
    return {
        "date": x["date"],
        "direction": ("credit" if x["entity_type"] == "voucher"
                      else "debit"),
        "entity": x["entity"],
        "entity_type": x["entity_type"],
        "status": x["status"],
        "misc": x["misc"]
    }


@bp.get("/user/transaction")
def get_transactions():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    page_no = int(request.args["page_no"]) if "page_no" in request.args else 1
    page_size = int(request.args["size"]) if "size" in request.args else 24

    cur.execute("""
        SELECT *, COUNT(*) OVER() AS total_items
        FROM "user"
        LEFT JOIN log ON "user".key = log.user_key
        WHERE
            user_key = %s AND (
                (
                    log.entity_type = 'voucher'
                    AND log.action = 'used'
                ) OR (
                    log.entity_type = 'order'
                    AND log.action = 'created'
                    AND (log.misc->>'pay_account')::numeric > 0
                )
            )
        ORDER BY log.date DESC
        LIMIT %s OFFSET %s;
    """, (
        user["key"],
        page_size,
        (page_no - 1) * page_size
    ))
    trans = cur.fetchall()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "transactions": [trx_schema(x) for x in trans],
        "total_page": ceil(trans[0]["total_items"] / page_size) if trans else 0
    })
