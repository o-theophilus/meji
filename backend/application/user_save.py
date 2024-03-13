from flask import Blueprint, jsonify, request
from .tools import token_to_user
from .schema import user_schema, item_schema
from math import ceil
from uuid import uuid4
from .postgres import db_close, db_open
from datetime import datetime

bp = Blueprint("save", __name__)


@bp.get("/save")
def get_saves():
    con, cur = db_open()

    user = token_to_user(cur)

    page_no = 1
    page_size = 24
    sort_order = "DESC" if True else "ASC"
    sort_by = "date"

    cur.execute("""
        SELECT item.*, COUNT(*) OVER() AS total_items
        FROM (
            SELECT *
            FROM save
            WHERE user_key = %s
        ) AS save
        LEFT JOIN item ON save.user_key = item.key
        ORDER BY
            CASE %s
                WHEN 'name' THEN item.name
                WHEN 'price' THEN item.price
                WHEN 'date' THEN save.date
                ELSE save.date
            END
            %s
        LIMIT %s OFFSET %s;
    """, (
        user["key"],
        sort_by,
        sort_order,
        page_size,
        (page_no - 1) * page_size
    ))

    items = cur.fetchall()

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "items": [item_schema(x) for x in items],
        "total_page": ceil(items[0][-1] / page_size) if items else 0
    })


@bp.post("/save")
def save_item():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if (
        "key" not in request.json
        or not request.json["key"]
        or "save" not in request.json
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("SELECT * FROM item WHERE key = %s;", (request.json["key"],))
    item = cur.fetchone()
    if not item:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("""
        SELECT *
        FROM save
        WHERE user_key = %s, item_key = %s;
    """, (
        user["key"],
        request.json["key"]
    ))
    saved_item = cur.fetchone()

    if saved_item and not request.json["save"]:
        cur.execute("DELETE FROM save WHERE key = %s;", (saved_item["key"],))

    elif not saved_item and request.json["save"]:
        cur.execute("""
            INSERT INTO save (key, date, user_key, item_key)
            VALUES (%s, %s, %s, %s);
        """, (
            uuid4().hex,
            datetime.now(),
            user["key"],
            item["key"]
        ))

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "user": user_schema(user),
    })
