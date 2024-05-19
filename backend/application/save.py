from flask import Blueprint, jsonify, request
from .tools import token_to_user, user_schema, item_schema
from math import ceil
from uuid import uuid4
from .postgres import db_close, db_open
from .log import log

bp = Blueprint("save", __name__)


@bp.get("/save")
def get():
    con, cur = db_open()

    user = token_to_user(cur)

    order_by = {
        'latest': 'save_log.date',
        'oldest': 'save_log.date',
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

    order = list(order_by.keys())[0]
    page_no = 1
    page_size = 24
    search = ""

    if "page_no" in request.args:
        page_no = int(request.args["page_no"])
    if "size" in request.args:
        page_size = int(request.args["size"])
    if "order" in request.args:
        order = request.args["order"]
    if "search" in request.args:
        search = request.args["search"].strip()

    cur.execute("""
        WITH item_sub AS (
            SELECT
                DISTINCT ON (log.entity_key) log.entity_key AS key,
                (log.misc->>'price')::float AS old_price,
                (100 * ((log.misc->>'price')::float - item.price))
                    / (log.misc->>'price')::float AS discount,
                log.date
            FROM log
            LEFT JOIN item ON item.key = log.entity_key
            WHERE
                log.action = 'edited'
                AND log.entity_type = 'item'
                AND (log.misc->>'price')::float > item.price
            ORDER BY log.entity_key, log.date DESC
        ),

        save_log AS (
            SELECT
                DISTINCT ON (save.item_key) save.*,
                log.date, log.action
            FROM save
            LEFT JOIN log ON save.item_key = log.entity_key
            WHERE
                save.user_key = %s
                AND (log.action = 'saved' OR log.action = 'unsaved')
                AND log.entity_type = 'item'
            ORDER BY save.item_key, log.date DESC
        )

        SELECT
            item.*,
            CASE
                WHEN item.show_discount = 'true' THEN item_sub.old_price
                WHEN item.show_discount = 'false' THEN NULL
                WHEN item_sub.date > item.show_discount::timestamp THEN NULL
                ELSE item_sub.old_price
            END AS old_price,
            COALESCE(item_sub.discount, 0) AS discount,
            COALESCE(AVG(feedback.rating), 0) AS rating,
            COALESCE(ARRAY_AGG(feedback.rating), ARRAY[]::int[]) AS ratings,
            COUNT(*) OVER() AS total_items
        FROM item
        LEFT JOIN item_sub ON item.key = item_sub.key
        LEFT JOIN save_log ON item.key = save_log.item_key
        LEFT JOIN feedback ON item.key = feedback.item_key
        WHERE
            save_log.action = 'saved'
            AND (%s = '' OR item.name ILIKE %s)
        GROUP BY
            item.key, item.status, item.name, item.slug,
            item.price, item.show_discount, item.information, item.photos,
            item.tags, item.variation, item.available_quantity,
            item_sub.discount, item_sub.old_price, item_sub.date,
            save_log.date
        ORDER BY {} {}
        LIMIT %s OFFSET %s;
    """.format(
        order_by[order], order_dir[order]
    ), (
        user["key"],
        search, f"%{search}%",
        page_size, (page_no - 1) * page_size
    ))
    items = cur.fetchall()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "items": [item_schema(x) for x in items],
        "order_by": list(order_by.keys()),
        "total_page": ceil(items[0]["total_items"] / page_size) if items else 0
    })


@bp.post("/save")
def save():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if (
        "key" not in request.json
        or not request.json["key"]
        or "save" not in request.json
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("SELECT * FROM item WHERE key = %s;", (request.json["key"],))
    item = cur.fetchone()
    if not item:
        db_close(con, cur)
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
        item["key"]
    ))
    saved_item = cur.fetchone()

    if saved_item and not request.json["save"]:
        cur.execute("DELETE FROM save WHERE key = %s;", (saved_item["key"],))

        log(
            cur=cur,
            user_key=user["key"],
            action="unsaved",
            entity_key=item["key"],
            entity_type="item"
        )

    elif not saved_item and request.json["save"] and item["status"] == "live":
        cur.execute("""
            INSERT INTO save (key, user_key, item_key)
            VALUES (%s, %s, %s);
        """, (
            uuid4().hex,
            user["key"],
            item["key"]
        ))

        log(
            cur=cur,
            user_key=user["key"],
            action="saved",
            entity_key=item["key"],
            entity_type="item"
        )

    cur.execute("SELECT * FROM save WHERE save.user_key = %s;", (user["key"],))
    saves = cur.fetchall()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user, saves=[x["item_key"] for x in saves]),
    })
