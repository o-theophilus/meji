from flask import Blueprint, jsonify, request
from .tools import token_to_user
from math import ceil
from .postgres import db_close, db_open

bp = Blueprint("log", __name__)


# TODO: do not use this template
log_template = """
    INSERT INTO log (
        key, date, user_key, action, entity_key, entity_type, status, misc
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
"""


@bp.get("/log")
def get():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    page_no = int(request.args["page_no"]) if "page_no" in request.args else 1
    page_size = int(
        request.args["page_size"]) if "page_size" in request.args else 24

    search = "all:all:all:all"
    if "search" in request.args:
        search = request.args["search"]

    search = search.split(":")
    if len(search) != 4:
        return jsonify({
            "status": 400,
            "error": "invalid search"
        })

    user_id, entity_type, user_action, entity_id = search

    if "log:view" not in user["roles"]:
        user_id = user["key"]

    cur.execute("""
        SELECT
            log.*,
            "user".name AS user_name,
            COALESCE(usr.name, item.name, "order".key, voucher.key,
                advert.key) AS entity_name,
            COUNT(*) OVER() AS total_items
        FROM log
        LEFT JOIN "user" ON log.user_key = "user".key
        LEFT JOIN "user" usr ON log.entity_type = 'admin'
            AND log.entity_key = usr.key
        LEFT JOIN item ON log.entity_type = 'item'
            AND log.entity_key = item.key
        LEFT JOIN "order" ON (log.entity_type = 'order'
            OR log.entity_type = 'cart') AND log.entity_key = "order".key
        LEFT JOIN voucher ON log.entity_type = 'voucher'
            AND log.entity_key = voucher.key
        LEFT JOIN advert ON log.entity_type = 'advert'
            AND log.entity_key = advert.key
        LEFT JOIN otp ON log.entity_type = 'otp'
            AND log.entity_key = otp.key
        WHERE
            (%s = 'all' OR CONCAT_WS(
                ', ', log.user_key, "user".name, "user".email
            ) ILIKE %s)
            AND (%s = 'all' OR log.entity_type = %s)
            AND (%s = 'all' OR log.action = %s)
            AND (%s = 'all' OR CONCAT_WS(
                ', ', log.entity_key, "user".name, "user".email, item.name
            ) ILIKE %s)
        ORDER BY log.date DESC
        LIMIT %s OFFSET %s;
    """, (
        user_id, f"%{user_id}%",
        entity_type, entity_type,
        user_action, user_action,
        entity_id, f"%{entity_id}%",
        page_size, (page_no - 1) * page_size
    ))
    logs = cur.fetchall()

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "logs": logs,
        "total_page": ceil(logs[0]["total_items"] / page_size) if logs else 0
    })


@bp.get("/log/action")
def search_query():
    con, cur = db_open()

    cur.execute("""
        SELECT DISTINCT ON (entity_type, action) entity_type, action
        FROM log;
    """)

    actions = {"all": ["all"]}
    for x in cur.fetchall():
        if x["entity_type"] in actions:
            actions[x["entity_type"]].append(x["action"])
        else:
            actions[x["entity_type"]] = ["all", x["action"]]

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "actions": actions
    })
