from flask import Blueprint, request, jsonify
from .tools import token_to_user, user_schema
from math import ceil
from .postgres import db_close, db_open


bp = Blueprint("user_get", __name__)


@bp.get("/user")
def get():
    con, cur = db_open()

    me = token_to_user(cur)
    if not me:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    user = None
    if "search" in request.args:

        if "user:view" not in me["roles"]:
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

            if user and "user:view_balance" not in me["roles"]:
                user["acc_balance"] = "#"

        if not user:
            return jsonify({
                "status": 400,
                "error": "user not found"
            })

    else:
        user = me

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })


@bp.get("/users")
def get_many():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "user:view" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    status = request.args["status"] if "status" in request.args else ""
    search = request.args["search"] if "search" in request.args else ""
    sort_by = request.args["sort"] if "sort" in request.args else "latest"
    page_no = int(request.args["page_no"]) if "page_no" in request.args else 1
    page_size = int(request.args["size"]) if "size" in request.args else 24

    sort_order = "DESC" if sort_by in ["latest", "name (z-a)"] else "ASC"
    if sort_by in ["latest", "oldest"]:
        sort_by = "date"
    elif sort_by in ["name (a-z)", "name (z-a)"]:
        sort_by = "name"

    cur.execute("""
        SELECT user.*, log.date AS date, COUNT(*) OVER() AS total_items
        FROM "user"
        LEFT JOIN log ON user.key = log.user_key
            AND log.action = 'created'
            AND log.entity_type = 'auth'
        WHERE
            status = %s
            AND CONCAT_WS(', ', user.key, user.name, user.email) ILIKE %s
        ORDER BY
            CASE %s
                WHEN 'latest' THEN log.date
                WHEN 'oldest' THEN log.date
                WHEN "name (a-z)" THEN user.name
                WHEN "name (z-a)" THEN user.name
                ELSE log.date
            END,
            CASE %s
                WHEN 'oldest' THEN ASC
                WHEN "name (a-z)" THEN ASC
                ELSE DESC
            END
        LIMIT %s OFFSET %s;
    """, (
        status,
        f"%{search}%",
        sort_by,
        sort_order,
        page_size,
        (page_no - 1) * page_size
    ))
    users = cur.fetchall()

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "users": [user_schema(x) for x in users],
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


@bp.get("/user/transactions")
def get_transactions():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    page_no = int(request.args["page_no"]) if "page_no" in request.args else 1
    page_size = int(request.args["size"]) if "size" in request.args else 24

    cur.execute("""
        SELECT *, COUNT(*) OVER() AS total_items
        FROM (
            SELECT *
            FROM "user"
            WHERE user_key = %s AND (
                (
                    entity_type = "voucher"
                    AND action = "used")
                OR
                (
                    entity_type = "order"
                    AND action = "created"
                    AND (misc->>'value')::numeric > 0
                )
            )
        ) AS subquery
        ORDER BY date DESC
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
