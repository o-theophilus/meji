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
    sort = "latest"

    order_by = {
        'latest': 'log.date',
        'oldest': 'log.date',
        'name (a-z)': 'item.name',
        'name (z-a)': 'item.name',
        'cheap': 'item.price',
        'expensive': 'item.price',
        'discount': 'discount',
        'rating': 'rating'
    }

    order_dir = {
        'latest': 'DESC',
        'oldest': 'ASC',
        'name (a-z)': 'ASC',
        'name (z-a)': 'DESC',
        'cheap': 'ASC',
        'expensive': 'DESC',
        'discount': 'DESC',
        'rating': 'DESC'
    }
    cur.execute("""
        SELECT
            item.*,
            CASE
                WHEN COUNT(feedback.*) = 0 THEN NULL
                ELSE SUM(feedback.rating) / COUNT(feedback.*)
            END AS rating,
            ARRAY_AGG(feedback.rating) AS ratings,
            COUNT(*) OVER() AS total_items
        FROM (
            SELECT *,
                CASE
                    WHEN old_price = 0 THEN 0
                    ELSE (100 * (old_price - price)) / old_price
                END AS discount
            FROM item
        ) AS item
        LEFT JOIN save ON item.key = save.item_key
        LEFT JOIN log ON item.key = log.entity_key
            AND log.action = 'created'
            AND log.entity_type = 'item'
        LEFT JOIN feedback ON item.key = feedback.item_key
        WHERE save.user_key = %s

        GROUP BY
            item.key, item.version, item.status, item.name, item.slug,
            item.price, item.old_price, item.information, item.photos,
            item.tags, item.adverts, item.variation, item.available_quantity,
            item.discount, log.date
        ORDER BY {} {}
        LIMIT %s OFFSET %s;
    """.format(
        order_by[sort], order_dir[sort]
    ), (
        user["key"],
        page_size, (page_no - 1) * page_size
    ))

    items = cur.fetchall()

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "items": [item_schema(x) for x in items],
        "total_page": ceil(items[0]["total_items"] / page_size) if items else 0
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
        WHERE user_key = %s AND item_key = %s;
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

    cur.execute("""
        SELECT
            CASE
                WHEN COUNT(save.*) = 0 THEN ARRAY[]::character[]
                ELSE ARRAY_AGG(save.item_key)
            END AS saves
        FROM save
        WHERE save.user_key = %s;
    """, (user["key"],))
    saves = cur.fetchone()

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "user": user_schema(user, saves=saves["saves"]),
    })
