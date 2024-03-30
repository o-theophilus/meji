from flask import Blueprint, request, jsonify
from .tools import token_to_user, user_schema
from math import ceil
from .postgres import db_close, db_open
import os
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4
from datetime import datetime
import json


bp = Blueprint("admin", __name__)


roles = {
    "admin": [
        ['manage_photo', 2]
    ],
    "user": [
        ['view', 1],
        ['view_balance', 2],
        ['set_role', 3]
    ],
    "item": [
        ['add', 2],
        ['edit_photo', 2],
        ['advert', 2],
        ['edit_status', 2],
        ['edit_name', 2],
        ['edit_tag', 2],
        ['edit_price', 2],
        ['edit_info', 2],
        ['edit_variation', 2]
    ],
    "voucher": [
        ['view', 1],
        ['add', 3],
        ['view_code', 3],  # change to view_pin
        ['status', 3]
    ],
    "log": [
        ['view', 1]
    ],
    "order": [
        ['view', 1],
        ['edit_eta', 2],
        ['status', 2],
        ['cancel', 2]
    ]
}


@bp.get("/admin/init")
def get():
    con, cur = db_open()
    email = os.environ["MAIL_USERNAME"]

    cur.execute('SELECT * FROM "user" WHERE email = %s;', (email,))
    if not cur.fetchone():
        cur.execute("""
                INSERT INTO "user" ( key, version, status, name, email,
                    password, roles)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """, (
            uuid4().hex,
            uuid4().hex,
            "confirmed",
            "Meji Admin",
            email,
            generate_password_hash(
                os.environ["MAIL_PASSWORD"], method="scrypt"),
            [f"{x}:{y[0]}" for x in roles for y in roles[x]]
        ))

    db_close(con, cur)

    return jsonify({
        "status": 200
    })


@bp.get("/admin/user")
def get_many():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    sort = request.args["sort"] if "sort" in request.args else "latest"
    page_no = int(request.args["page_no"]) if "page_no" in request.args else 1
    page_size = int(request.args["size"]) if "size" in request.args else 24

    search = "all:all:all"
    if "search" in request.args:
        search = request.args["search"]

    search = search.split(":")
    if len(search) != 3:
        return jsonify({
            "status": 400,
            "error": "invalid search"
        })

    user_key, role_type, role_action = search

    if "user:view" not in user["roles"]:
        user_key = user["key"]

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
            COUNT(*) OVER() AS total_items
        FROM "user"
        LEFT JOIN log ON "user".key = log.user_key
            AND log.action = 'created'
            AND log.entity_type = 'auth'
        WHERE
            array_length("user".roles, 1) IS NOT NULL
            AND (%s = 'all'
                OR CONCAT_WS(', ', "user".key, "user".name, "user".email)
                ILIKE %s)
            AND (%s = 'all' OR ARRAY_TO_STRING("user".roles, ',') ILIKE %s)
            AND (%s = 'all' OR ARRAY_TO_STRING("user".roles, ',') ILIKE %s)
        ORDER BY {} {}
        LIMIT %s OFFSET %s;
    """.format(
        order_by[sort], order_dir[sort]
    ), (
        user_key, f"%{user_key}%",
        role_type, f"%{role_type}:%",
        role_action, f"%{role_type}:{role_action}%",
        page_size, (page_no - 1) * page_size
    ))
    users = cur.fetchall()

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "users": [user_schema(x) for x in users],
        "total_page": ceil(users[0]["total_items"] / page_size) if users else 0
    })


@bp.put("/admin/role/<key>")
def role(key):
    con, cur = db_open()

    me = token_to_user(cur)
    cur.execute('SELECT * FROM "user" WHERE key = %s;', (key,))
    user = cur.fetchone()

    error = None
    if not me or "user:set_role" not in me["roles"]:
        error = "unauthorized access"
    elif "password" not in request.json:
        error = "this field is required"
    elif not check_password_hash(me["password"], request.json["password"]):
        error = "incorrect password"
    elif (
        not user
        or me["key"] == user["key"]
        or "roles" not in request.json
        or type(request.json["roles"]) is not list
        or user["email"] == os.environ["MAIL_USERNAME"]
        or user["status"] != "confirmed"
    ):
        error = "invalid request"

    if error:
        return jsonify({
            "status": 400,
            "error": error
        })

    cur.execute("""
        UPDATE "user"
        SET roles = %s
        WHERE key = %s;
    """, (
        request.json["roles"],
        user["key"]
    ))

    cur.execute("""
        INSERT INTO log (
            key, date, user_key, action, entity_key, entity_type, misc
        ) VALUES (%s, %s, %s, %s, %s, %s, %s);
    """, (
        uuid4().hex,
        datetime.now(),
        me["key"],
        "changed_role",
        user["key"],
        "admin",
        json.dumps({
            "from": user["roles"],
            "to": request.json["roles"]
        })
    ))

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })
