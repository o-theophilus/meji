from flask import Blueprint, request, jsonify
from .tools import token_to_user, user_schema
from math import ceil
from .postgres import db_close, db_open
import os
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4
from datetime import datetime
import json
from .advert import sizes
from .storage import drive, storage
from .log import log


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


@bp.get("/photo/error")
def photo_error():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "admin:manage_photo" not in user["permissions"]:
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute("""
        SELECT photo
        FROM "user";
    """)
    users_photo = cur.fetchall()
    users_photo = [x["photo"] for x in users_photo if x["photo"]]

    cur.execute("""
        SELECT photos
        FROM item;
    """)
    temp = cur.fetchall()
    items_photos = []
    for x in temp:
        if x["photos"] != []:
            items_photos += x["photos"]

    cur.execute("""
        SELECT *
        FROM advert;
    """)
    temp = cur.fetchall()
    adverts_photos = []
    for x in temp:
        for y in sizes:
            if x[f"photo_{y}"]:
                adverts_photos.append(x[f"photo_{y}"])

    all_used_photos = users_photo + items_photos + adverts_photos
    paths = drive().list()["names"]
    all_stored_photos = [x.split('/')[1] for x in paths]

    cur.execute("""
        SELECT "user".key, "user".name
        FROM "user"
        WHERE
            photo IS NOT NULL
            AND NOT photo = ANY(%s);
    """, (all_stored_photos,))
    _users = cur.fetchall()

    cur.execute("""
        SELECT item.key, item.name
        FROM item
        WHERE NOT ARRAY[%s] @> photos;
    """, (all_stored_photos,))
    _items = cur.fetchall()

    cur.execute("""
        SELECT advert.key, item.name
        FROM advert
        LEFT JOIN item ON advert.key = item.key
        WHERE
            (
                photo_300x300 IS NOT NULL
                AND NOT photo_300x300 = ANY(%s)
            ) OR (
                photo_300x600 IS NOT NULL
                AND NOT photo_300x600 = ANY(%s)
            ) OR (
                photo_600x300 IS NOT NULL
                AND NOT photo_600x300 = ANY(%s)
            ) OR (
                photo_900x300 IS NOT NULL
                AND NOT photo_900x300 = ANY(%s)
            );
    """, (
        all_stored_photos, all_stored_photos,
        all_stored_photos, all_stored_photos
    ))
    _adverts = cur.fetchall()

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "unused": [f"{request.host_url}photo/{x}"
                   for x in all_stored_photos if x not in all_used_photos],
        "users": _users,
        "items": _items,
        "adverts": _adverts
    })


@bp.delete("/photo/error")
def delete_photo():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "admin:manage_photo" not in user["permissions"]:
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    if (
        "photos" not in request.json
        or type(request.json["photos"]) is not list
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    for x in request.json["photos"]:
        pass
        storage(x.split("/")[-1], delete=True)

    log(
        user_key=user["key"],
        action="signed_up",
        entity_type="auth"
    )

    db_close(con, cur)

    return jsonify({
        "status": 200
    })
