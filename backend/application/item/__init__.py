import re
from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from flask import Blueprint, jsonify, request
from psycopg2.extras import Json
from werkzeug.security import check_password_hash

from ..cart.delivery import get_areas
from ..log import log
from ..postgres import db_close, db_open
from ..tools import get_session, item_schema, reserved_words
from ..user.get import get_user_like
from .get import get_comments, get_items

bp = Blueprint("item", __name__)


@bp.post("/items")
def add_item():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "item.add" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 403,
            "error": "unauthorized access"
        })

    name = ' '.join(request.json.get("name", "").strip().split())

    error = {}
    if not name:
        error["name"] = "This field is required"
    elif len(name) > 100:
        error["name"] = "This field cannot exceed 100 characters"
    if error:
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
        INSERT INTO item (name, slug, metadata)
        VALUES (%s, %s, %s) RETURNING *;
    """, (name, slug,
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

    log(
        cur=cur,
        user_key=user["key"],
        action="created item",
        entity_type="item",
        entity_key=item["key"],
    )

    items = get_items(cur)

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "item": item_schema(item),
        "items": items.json["items"],
        "total_page": items.json["total_page"]
    })


@bp.put("/items/<key>")
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
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

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

    log(
        cur=cur,
        user_key=user["key"],
        action="edited item",
        entity_type="item",
        entity_key=item["key"],
        misc=request.json
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "item": item_schema(item)
    })


@bp.delete("/items/<key>")
def delete(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    password = request.json.get("password")

    error = None
    if "item.edit_status" not in user["access"]:
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

    log(
        cur=cur,
        user_key=user["key"],
        action="deleted item",
        entity_type="item",
        entity_key=item["key"],
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/items/<key>/like")
def like(key):
    con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute("""SELECT * FROM item WHERE key = %s;""", (key,))
    item = cur.fetchone()
    if not item:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute("""
        SELECT * FROM "like" WHERE user_key = %s AND item_key = %s;
    """, (user["key"], item["key"]))
    user_reaction = cur.fetchone()

    if not user_reaction:
        cur.execute("""
            INSERT INTO "like" (user_key, item_key)
            VALUES (%s, %s);
        """, (user["key"], item["key"]))
    else:
        cur.execute("""DELETE FROM "like" WHERE key = %s;""", (
            user_reaction["key"],))

    log(
        cur=cur,
        user_key=user["key"],
        action=f"{'un' if user_reaction else ''}like item",
        entity_type="item",
        entity_key=item["key"],
    )

    likes = get_user_like(cur, user["key"])

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "likes": likes
    })


@bp.post("/items/<key>/comments")
def add_comment(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute("""
        SELECT * FROM item WHERE slug = %s OR key = %s;
    """, (key, key))
    item = cur.fetchone()
    if not item:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    parent_key = request.json.get("parent_key")
    if parent_key:
        if "comment.reply" not in user["access"]:
            db_close(con, cur)
            return jsonify({
                "status": 403,
                "error": "unauthorized access"
            })

        cur.execute("SELECT * FROM comment WHERE key = %s;", (parent_key,))
        if not cur.fetchone():
            db_close(con, cur)
            return jsonify({
                "status": 400,
                "error": "Invalid request"
            })

    cur.execute("""
        WITH purchase_check AS (
            SELECT EXISTS (
                SELECT 1
                FROM "order" o
                LEFT JOIN order_item oi ON o.key = oi.order_key
                LEFT JOIN item_version iv ON oi.item_version_key = iv.key
                WHERE
                    o.user_key = %s
                    AND o.status = 'delivered'
                    AND iv.item_key = %s
            ) AS has_purchased
        ),

        comment_check AS (
            SELECT EXISTS (
                SELECT 1
                FROM comment
                WHERE
                    comment.user_key = %s
                    AND comment.item_key = %s
                    AND comment.parent_key IS NULL
            ) AS has_commented
        )

        SELECT
            purchase_check.has_purchased,
            purchase_check.has_purchased AND NOT comment_check.has_commented
                AS can_comment
        FROM purchase_check, comment_check
    """, (user["key"], item["key"], user["key"], item["key"]))
    user_comment_info = cur.fetchone()

    if not user_comment_info["can_comment"]:
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    rating = request.json.get("rating", 0)
    comment = request.json.get("comment", "").strip()
    error = {}
    if rating not in [1, 2, 3, 4, 5]:
        error["rating"] = "This field is required"

    if not comment:
        error["comment"] = "This field is required"
    elif len(comment) > 500:
        error["comment"] = "This field cannot exceed 500 characters"
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    cur.execute("""
        INSERT INTO comment (user_key, item_key, rating,
            comment, parent_key)
        VALUES (%s, %s, %s, %s, %s) RETURNING *;
    """, (user["key"], item["key"], rating, comment, parent_key))
    comment = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="added comment",
        entity_type="item",
        entity_key=item["key"],
        misc={
            "comment_key": comment["key"]
        }
    )

    comments = get_comments(item["key"], cur=cur)
    db_close(con, cur)
    return comments
