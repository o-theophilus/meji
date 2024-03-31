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


permissions = {
    "admin": [
        ['manage_photo', 2]
    ],
    "user": [
        ['view', 1],
        ['view_balance', 2],
        ['set_permission', 3]
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
        ['view_pin', 3],
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
                    password, permissions)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """, (
            uuid4().hex,
            uuid4().hex,
            "confirmed",
            "Meji Admin",
            email,
            generate_password_hash(
                os.environ["MAIL_PASSWORD"], method="scrypt"),
            [f"{x}:{y[0]}" for x in permissions for y in permissions[x]]
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

    _user, _type, _action = search

    if "user:view" not in user["permissions"]:
        _user = user["key"]

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
            array_length("user".permissions, 1) IS NOT NULL
            AND (%s = 'all'
                OR CONCAT_WS(', ', "user".key, "user".name, "user".email)
                ILIKE %s)
            AND (%s = 'all' OR ARRAY_TO_STRING("user".permissions, ',')
                ILIKE %s)
            AND (%s = 'all' OR ARRAY_TO_STRING("user".permissions, ',')
                ILIKE %s)
        ORDER BY {} {}
        LIMIT %s OFFSET %s;
    """.format(
        order_by[sort], order_dir[sort]
    ), (
        _user, f"%{_user}%",
        _type, f"%{_type}:%",
        _action, f"%{_type}:{_action}%",
        page_size, (page_no - 1) * page_size
    ))
    users = cur.fetchall()

    db_close(con, cur)

    permits = {
        "all": ['all']
    }
    for x in permissions:
        if x not in permits:
            permits[x] = ["all"]
            for y in permissions[x]:
                permits[x].append(y[0])

    return jsonify({
        "status": 200,
        "users": [user_schema(x) for x in users],
        "permissions": permits,
        "total_page": ceil(users[0]["total_items"] / page_size) if users else 0
    })


@bp.put("/admin/permission/<key>")
def permission(key):
    con, cur = db_open()

    me = token_to_user(cur)
    cur.execute('SELECT * FROM "user" WHERE key = %s;', (key,))
    user = cur.fetchone()

    error = None
    if not me or "user:set_permission" not in me["permissions"]:
        error = "unauthorized access"
    elif "password" not in request.json:
        error = "this field is required"
    elif not check_password_hash(me["password"], request.json["password"]):
        error = "incorrect password"
    elif (
        not user
        or me["key"] == user["key"]
        or "permissions" not in request.json
        or type(request.json["permissions"]) is not list
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
        SET permissions = %s
        WHERE key = %s;
    """, (
        request.json["permissions"],
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
        "changed_permission",
        user["key"],
        "admin",
        json.dumps({
            "from": user["permissions"],
            "to": request.json["permissions"]
        })
    ))

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })
