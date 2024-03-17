from flask import Blueprint, jsonify, request
from .tools import token_to_user, user_schema, item_schema
from math import ceil
from uuid import uuid4
from .postgres import db_close, db_open
from datetime import datetime

bp = Blueprint("save", __name__)


@bp.get("/save")
def get():
    con, cur = db_open()

    user = token_to_user(cur)

    page_no = 1
    page_size = 24
    sort_by = "latest"

    cur.execute("""
        SELECT item.*, COUNT(*) OVER() AS total_items
        FROM save
        LEFT JOIN item ON save.user_key = item.key
        WHERE save.user_key = %s
        ORDER BY
            CASE %s
                WHEN 'latest' THEN log.date
                WHEN 'oldest' THEN log.date
                WHEN "name (a-z)" THEN save.name
                WHEN "name (z-a)" THEN save.name
                WHEN "cheap" THEN save.price
                WHEN "expensive" THEN save.price
                WHEN "discount" THEN discount
                WHEN "rating" THEN rating
                ELSE log.date
            END,
            CASE %s
                WHEN 'oldest' THEN ASC
                WHEN "name (a-z)" THEN ASC
                WHEN "cheap" THEN ASC
                ELSE DESC
            END
        LIMIT %s OFFSET %s;
    """, (
        user["key"],
        sort_by, sort_by,
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
def save():
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
