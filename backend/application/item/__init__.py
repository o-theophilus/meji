from flask import Blueprint, jsonify, request
import re
from uuid import uuid4
from werkzeug.security import check_password_hash
from ..tools import reserved_words, get_session
from ..postgres import db_open, db_close
from ..storage import storage
from ..log import log
from .get import get_many, item_schema
from psycopg2.extras import Json
from decimal import Decimal
from datetime import datetime

bp = Blueprint("item", __name__)


@bp.post("/item")
def add():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "item:add" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    name = ' '.join(request.json.get("name", "").strip().split())

    error = {}
    if not name:
        error["name"] = "This field is required"
    elif len(name) > 100:
        error["name"] = "This field cannot exceed 100 characters"
    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    slug = re.sub('-+', '-', re.sub('[^a-zA-Z0-9]', '-', name.lower()))
    slug = slug[:100]
    cur.execute('SELECT * FROM item WHERE slug = %s;', (slug,))
    item = cur.fetchone()
    if item or slug in reserved_words:
        slug = f"{slug[:89]}-{str(uuid4().hex)[:10]}"

    cur.execute("""
        INSERT INTO item (name, slug)
        VALUES (%s, %s) RETURNING *;
    """, (name, slug))
    item = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="created item",
        entity_key=item["key"],
        entity_type="item"
    )

    items = get_many(cur)

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "item": item_schema(item),
        "items": items.json["items"],
        "total_page": items.json["total_page"]
    })


@bp.put("/item/<key>")
def edit(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute('SELECT * FROM item WHERE key = %s;', (key,))
    item = cur.fetchone()
    if not item:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    error = {}

    status = item["status"]
    date_created = item["date_created"]
    name = item["name"]
    slug = item["slug"]
    tags = item["tags"]
    price = item["price"]
    price_old = item["price_old"]
    information = item["information"]
    variation = item["variation"]
    quantity = item["quantity"]

    if "status" in request.json:
        status = request.json.get("status")
        if "item:edit_status" not in user["access"]:
            error["status"] = "unauthorized access"
        elif not status or status not in ['active', 'draft']:
            error["status"] = "Invalid request"
        elif status == item["status"]:
            error["status"] = "No changes were made"
        elif status == "active" and item["files"] == []:
            error["status"] = "no photo"

    if "date_created" in request.json:
        date_created = request.json.get("date_created")
        if "item:edit_date" not in user["access"]:
            error["date_created"] = "unauthorized access"
        elif not date_created:
            error["date_created"] = "This field is required"
        elif date_created == item["date_created"]:
            error["date_created"] = "No changes were made"
        else:
            try:
                datetime.strptime(date_created, "%Y-%m-%dT%H:%M:%S")
            except Exception:
                error["date_created"] = "invalid input"

    if "name" in request.json:
        name = ' '.join(request.json.get("name", "").strip().split())
        if "item:edit_name" not in user["access"]:
            error["name"] = "unauthorized access"
        elif not name:
            error["name"] = "This field is required"
        elif name == item["name"]:
            error["name"] = "No changes were made"
        elif len(name) > 100:
            error["name"] = "This field cannot exceed 100 characters"
        else:
            slug = re.sub('-+', '-', re.sub('[^a-zA-Z0-9]', '-', name.lower()))
            slug = slug[:100]
            cur.execute('SELECT * FROM item WHERE key != %s AND slug = %s;',
                        (item["key"], slug))
            slug_in_use = cur.fetchone()
            if (slug_in_use or slug in reserved_words):
                slug = f"{slug[:89]}-{str(uuid4().hex)[:10]}"

    if "tags" in request.json:
        tags = request.json.get("tags")
        if "item:edit_tag" not in user["access"]:
            error["tags"] = "unauthorized access"
        elif type(tags) is not list:
            error["tags"] = "This field is required"
        elif set(tags) == set(item["tags"]):
            error["tags"] = "No changes were made"

    if "price" in request.json or "price_old" in request.json:
        price = request.json.get("price", price)
        price_old = 0 if price == 0 else request.json.get(
            "price_old", price_old)

        if "item:edit_price" not in user["access"]:
            error["error"] = "unauthorized access"
        elif price == item["price"] and price_old == item["price_old"]:
            error["error"] = "No changes were made"
        if not isinstance(price, (int, float)) or price < 0:
            error["price"] = "Please enter a valid number"
        if not isinstance(price_old, (int, float)) or price_old < 0:
            error["price_old"] = "Please enter a valid number"
        elif price_old <= price and price_old != 0:
            error["price_old"] = "This must be greater than current price"

    if "information" in request.json:
        information = request.json.get("information")
        if "item:edit_information" not in user["access"]:
            error["information"] = "unauthorized access"
        elif information == item["information"]:
            error["information"] = "No changes were made"
        elif len(information) > 5000:
            error["information"] = "This field cannot exceed 5000 characters"

    if "variation" in request.json:
        variation = request.json.get("variation")
        if "item:edit_variation" not in user["access"]:
            error["variation"] = "unauthorized access"
        elif type(variation) is not dict:
            error["variation"] = "This field is required"
        elif variation == item["variation"]:
            error["variation"] = "No changes were made"

    if "quantity" in request.json:
        quantity = request.json.get("quantity")
        if "item:edit_quantity" not in user["access"]:
            error["error"] = "unauthorized access"
        elif quantity == item["quantity"]:
            error["error"] = "No changes were made"
        if not isinstance(quantity, int) or quantity < 0:
            error["quantity"] = "Please enter a valid number"

    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    cur.execute("""
        UPDATE item
        SET status= %s, slug = %s, date_created= %s, name = %s, tags= %s,
        price = %s, price_old = %s,
        information= %s, variation= %s, quantity= %s
        WHERE key = %s RETURNING *;
    """, (
        status, slug, date_created, name, tags,
        Decimal(price), Decimal(price_old),
        information, Json(variation), quantity,
        item["key"]
    ))
    item = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="edited item",
        entity_key=item["key"],
        entity_type="item",
        misc=request.json
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "item": item_schema(item)
    })


@bp.delete("/item/<key>")
def delete(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    password = request.json.get("password")

    error = None
    if "item:edit_status" not in user["access"]:
        error = "unauthorized access"
    elif not password:
        error = "This field is required"
    elif not check_password_hash(user["password"], password):
        error = "Incorrect password"
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": error
        })

    cur.execute('SELECT * FROM item WHERE key = %s;', (key,))
    item = cur.fetchone()
    if not item:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute("""
        DELETE FROM item WHERE key = %s;
    """, (item["key"],))

    for x in item["files"]:
        storage.delete(x, "item")

    log(
        cur=cur,
        user_key=user["key"],
        action="deleted item",
        entity_key=item["key"],
        entity_type="item"
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
