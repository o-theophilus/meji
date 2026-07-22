import re
from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from flask import Blueprint, request
from psycopg2.extras import Json
from werkzeug.security import check_password_hash

from ..cart.delivery import get_areas
from ..tools import item_schema, log, rate_limit, reserved_words, session
from .get import many

bp = Blueprint("item", __name__)


@bp.post("/items")
@session(True)
@rate_limit(20, 1)
@log("item")
def add(cur, user):
    if "item.add" not in user["access"]:
        return {
            "error": "unauthorized access"
        }, 403

    name = ' '.join(request.json.get("name", "").strip().split())

    error = {}
    if not name:
        error["name"] = "This field is required"
    elif len(name) > 100:
        error["name"] = "This field cannot exceed 100 characters"
    if error:
        return {
            **error
        }, 422

    slug = re.sub('-+', '-', re.sub('[^a-zA-Z0-9]', '-', name.lower()))
    slug = slug[:100]
    cur.execute('SELECT * FROM item WHERE slug = %s;', (slug,))
    item = cur.fetchone()
    if item or slug in reserved_words:
        slug = f"{slug[:89]}-{str(uuid4().hex)[:10]}"

    cur.execute("""
        INSERT INTO item (name, slug, metadata)
        VALUES (%s, %s, %s) RETURNING *;
    """, (
        name, slug,
        Json({
            "length": 0,
            "breadth": 0,
            "height": 0,
            "weight": 0,
            "area": "igando",
            "prep_time": 7
        })
    ))
    item = cur.fetchone()

    _many = many(cur, user)

    return {
        "item": item_schema(item),
        "items": _many["items"],
        "total_page": _many["total_page"],
        "log": {
            "entity_key": item["key"]
        }
    }, 200


@bp.put("/items/<key>")
@session(True)
@rate_limit(20, 1)
@log("item")
def edit(cur, user, key):
    cur.execute('SELECT * FROM item WHERE key = %s;', (key,))
    item = cur.fetchone()
    if not item:
        return {
            "error": "Invalid request"
        }, 404

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
    metadata = item["metadata"]

    if "status" in request.json:
        status = request.json.get("status")
        if "item.edit_status" not in user["access"]:
            error["status"] = "unauthorized access"
        elif not status or status not in ['active', 'draft']:
            error["status"] = "Invalid request"
        elif status == item["status"]:
            error["status"] = "No changes were made"
        elif status == "active" and item["files"] == []:
            error["status"] = "no photo"

    if "date_created" in request.json:
        date_created = request.json.get("date_created")
        if "item.edit_date" not in user["access"]:
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
        if "item.edit_name" not in user["access"]:
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
        if "item.edit_tag" not in user["access"]:
            error["tags"] = "unauthorized access"
        elif type(tags) is not list:
            error["tags"] = "This field is required"
        elif set(tags) == set(item["tags"]):
            error["tags"] = "No changes were made"

    if "price" in request.json or "price_old" in request.json:
        price = request.json.get("price", price)
        price_old = 0 if price == 0 else request.json.get(
            "price_old", price_old)

        if "item.edit_price" not in user["access"]:
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
        information = request.json.get("information", "").strip()
        if "item.edit_information" not in user["access"]:
            error["information"] = "unauthorized access"
        elif information == item["information"]:
            error["information"] = "No changes were made"
        elif len(information) > 5000:
            error["information"] = "This field cannot exceed 5000 characters"

    if "variation" in request.json:
        variation = request.json.get("variation")
        if "item.edit_variation" not in user["access"]:
            error["variation"] = "unauthorized access"
        elif type(variation) is not dict:
            error["variation"] = "This field is required"
        elif variation == item["variation"]:
            error["variation"] = "No changes were made"

    if "quantity" in request.json:
        quantity = request.json.get("quantity")
        if "item.edit_quantity" not in user["access"]:
            error["error"] = "unauthorized access"
        elif quantity == item["quantity"]:
            error["error"] = "No changes were made"
        if not isinstance(quantity, int) or quantity < 0:
            error["quantity"] = "Please enter a valid number"

    if "metadata" in request.json:
        metadata = request.json.get("metadata", {})
        if "item.edit_metadata" not in user["access"]:
            error["error"] = "unauthorized access"
        elif type(metadata) is not dict:
            error["error"] = "Invalid request"
        else:
            if (
                "length" not in metadata
                or not (
                    isinstance(metadata["length"], float)
                    or isinstance(metadata["length"], int)
                )
                or metadata["length"] < 0
            ):
                error["length"] = "Please enter a valid dimension"
            if (
                "breadth" not in metadata
                or not (
                    isinstance(metadata["breadth"], float)
                    or isinstance(metadata["breadth"], int)
                )
                or metadata["breadth"] < 0
            ):
                error["breadth"] = "Please enter a valid dimension"
            if (
                "height" not in metadata
                or not (
                    isinstance(metadata["height"], float)
                    or isinstance(metadata["height"], int)
                )
                or metadata["height"] < 0
            ):
                error["height"] = "Please enter a valid dimension"
            if (
                "weight" not in metadata
                or not (
                    isinstance(metadata["weight"], float)
                    or isinstance(metadata["weight"], int)
                )
                or metadata["weight"] < 0
            ):
                error["weight"] = "Please enter a valid dimension"
            if (
                "prep_time" not in metadata
                or not isinstance(metadata["prep_time"], int)
                or metadata["prep_time"] < 0
            ):
                error["prep_time"] = "Please enter a valid number"
            if (
                "area" in metadata
                and metadata["area"]
                and metadata["area"] not in get_areas()
            ):
                error["area"] = "Invalid selection"

    if error:
        return {
            **error
        }, 400

    cur.execute("""
        UPDATE item
        SET status= %s, slug = %s, date_created= %s, name = %s, tags= %s,
        price = %s, price_old = %s,
        information= %s, variation= %s, quantity= %s, metadata = %s
        WHERE key = %s RETURNING *;
    """, (
        status, slug, date_created, name, [x.lower() for x in tags],
        Decimal(price), Decimal(price_old),
        information, Json(variation), quantity, Json(metadata),
        item["key"]
    ))
    item = cur.fetchone()

    return {
        "item": item_schema(item),
        "log": {
            "entity_key": item["key"],
            "misc": request.json
        }
    }, 200


@bp.delete("/items/<key>")
@session(True)
@rate_limit(20, 1)
@log("item")
def delete(cur, user, key):
    if "item.edit_status" not in user["access"]:
        return {
            "error": "unauthorized access"
        }, 403

    cur.execute('SELECT * FROM item WHERE key = %s;', (key,))
    item = cur.fetchone()
    if not item:
        return {
            "error": "Invalid request"
        }, 404

    password = request.json.get("password")
    error = None
    if not password:
        error = "This field is required"
    elif not check_password_hash(user["password"], password):
        error = "Incorrect password"
    if error:
        return {
            "error": error
        }, 422

    cur.execute("""
        DELETE FROM item WHERE key = %s;
    """, (item["key"],))

    return {
        "log": {
            "entity_key": item["key"],
        }
    }, 200
