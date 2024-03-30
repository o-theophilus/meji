from flask import Blueprint, jsonify, request
from .tools import reserved_words, token_to_user, item_schema
import re
from uuid import uuid4
from .storage import storage
from .postgres import db_close, db_open
from datetime import datetime
import json

bp = Blueprint("item", __name__)


@bp.post("/item")
def add():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "item:add" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    if "name" not in request.json or not request.json["name"]:
        return jsonify({
            "status": 400,
            "error": "this field is required"
        })

    slug = re.sub('-+', '-', re.sub(
        '[^a-zA-Z0-9]', '-', request.json["name"].lower()))
    cur.execute('SELECT * FROM item WHERE slug = %s;', (slug,))
    item = cur.fetchone()
    if item or slug in reserved_words:
        slug = f"{slug}-{str(uuid4().hex)[:10]}"

    cur.execute("""
            INSERT INTO item (key, version, name, slug)
            VALUES (%s, %s, %s, %s)
            RETURNING *;
        """, (
        uuid4().hex,
        uuid4().hex,
        request.json["name"],
        slug
    ))
    item = cur.fetchone()
    item["ratings"] = []

    cur.execute("""
        INSERT INTO log (
            key, date, user_key, action, entity_key, entity_type
        ) VALUES (%s, %s, %s, %s, %s, %s);
    """, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "created",
        item["key"],
        "item"
    ))

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "item": item_schema(item)
    })


@bp.put("/item/<key>")
def edit(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    cur.execute('SELECT * FROM item WHERE key = %s;', (key,))
    item = cur.fetchone()
    if not item:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = {}

    if "status" in request.json:
        if "item:edit_status" not in user["roles"]:
            error["status"] = "unauthorized access"
        elif (
            not request.json["status"]
            or request.json["status"] not in ['live', 'draft', 'delete']
        ):
            error["status"] = "invalid request"
        elif request.json["status"] == "live" and len(item["photos"]) == 0:
            error["status"] = "add photo"
        elif request.json["status"] == "live" and not item["price"]:
            error["status"] = "add price"
        else:
            cur.execute("""
                    UPDATE item
                    SET status = %s
                    WHERE key = %s;
                """, (
                request.json["status"],
                item["key"]
            ))

    if "name" in request.json:
        if "item:edit_name" not in user["roles"]:
            error["name"] = "unauthorized access"
        elif not request.json["name"]:
            error["name"] = "this field is required"
        else:
            slug = re.sub('-+', '-', re.sub(
                '[^a-zA-Z0-9]', '-', request.json["name"].lower()))
            cur.execute('SELECT * FROM item WHERE slug = %s;', (slug,))
            slug_in_use = cur.fetchone()
            if ((slug_in_use and slug_in_use['key'] != item["key"])
                    or slug in reserved_words):
                slug = f"{slug}-{str(uuid4().hex)[:10]}"

            cur.execute("""
                    UPDATE item
                    SET name = %s, slug = %s
                    WHERE key = %s;
                """, (
                request.json["name"],
                slug,
                item["key"]
            ))

    if "tags" in request.json:
        if "item:edit_tag" not in user["roles"]:
            error["tag"] = "unauthorized access"
        elif type(request.json["tags"]) is not list:
            error["tags"] = "this field is required"
        else:
            cur.execute("""
                    UPDATE item
                    SET tags = %s
                    WHERE key = %s;
                """, (
                request.json["tags"],
                item["key"]
            ))

    if "price" in request.json:
        if not request.json["price"]:
            request.json["price"] = 0

        if "item:edit_price" not in user["roles"]:
            error["price"] = "unauthorized access"
        elif request.json["price"]:
            if (
                type(request.json["price"]) not in [int, float]
                or request.json["price"] < 0
            ):
                error["price"] = "please enter a valid price"
            else:
                cur.execute("""
                        UPDATE item
                        SET price = %s
                        WHERE key = %s;
                    """, (
                    request.json["price"],
                    item["key"]
                ))
                item["price"] = request.json["price"]

        elif item["status"] == "live":
            cur.execute("""
                    UPDATE item
                    SET status = %s
                    WHERE key = %s;
                """, (
                "draft",
                item["key"]
            ))

    if item["old_price"] > 0 and item["price"] >= item["old_price"]:
        cur.execute("""
            UPDATE item
            SET old_price = 0
            WHERE key = %s;
        """, (item["key"],))

    if "old_price" in request.json:
        if not request.json["old_price"]:
            request.json["old_price"] = 0

        if "item:edit_price" not in user["roles"]:
            error["price"] = "unauthorized access"

        elif item["price"]:
            if (
                type(request.json["old_price"]) not in [int, float]
                or request.json["old_price"] < 0
            ):
                error["old_price"] = "please enter a valid price"
            elif (
                request.json["old_price"] > 0
                and request.json["old_price"] <= item["price"]
            ):
                error["old_price"] = 'old price should be greater than price'
            else:
                cur.execute("""
                        UPDATE item
                        SET old_price = %s
                        WHERE key = %s;
                    """, (
                    request.json["old_price"],
                    item["key"]
                ))

    if "info" in request.json:
        if "item:edit_info" not in user["roles"]:
            error["info"] = "unauthorized access"
        else:
            cur.execute("""
                    UPDATE item
                    SET information = %s
                    WHERE key = %s;
                """, (
                request.json["information"],
                item["key"]
            ))

    if "variation" in request.json:
        if "item:edit_variation" not in user["roles"]:
            error["variation"] = "unauthorized access"
        elif type(request.json["variation"]) is not dict:
            error["variation"] = "this field is required"
        else:
            variation = request.json["variation"]
            for key in variation:
                if (
                    type(variation[key]) is not list
                    or len(variation[key]) == 0
                ):
                    del variation[key]

            cur.execute("""
                    UPDATE item
                    SET variation = %s
                    WHERE key = %s;
                """, (
                variation,
                item["key"]
            ))

    if error != {}:
        return jsonify({
            "status": 400,
            **error
        })

    cur.execute("""
        SELECT item.*,
            CASE
                WHEN COUNT(feedback.*) = 0 THEN ARRAY[]::integer[]
                ELSE ARRAY_AGG(feedback.rating)
            END AS ratings
        FROM item
        LEFT JOIN feedback ON item.key = feedback.item_key
        WHERE item.key = %s
        GROUP BY item.key;
    """, (key,))
    item = cur.fetchone()

    cur.execute("""
        INSERT INTO log (
            key, date, user_key, action, entity_key, entity_type, misc
        ) VALUES (%s, %s, %s, %s, %s, %s, %s);
    """, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "edited",
        item["key"],
        "item",
        json.dumps(request.json)
    ))

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "item": item_schema(item)
    })


@bp.post("/item/photo/<key>")
def add_photos(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "item:edit_photo" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute('SELECT * FROM item WHERE key = %s;', (key,))
    item = cur.fetchone()
    if 'files' not in request.files or not item:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = ""
    files = []
    for x in request.files.getlist("files"):
        media, format = x.content_type.split("/")

        err = ""
        if media != "image" or format in ['svg+xml', 'x-icon']:
            err = f"{x.filename} => invalid file"
        elif len(files) + len(item["photos"]) >= 10:
            err = f"{x.filename} => excess file"

        if err:
            error = f"{error}, {err}" if error else err
        else:
            files.append(x)

    if files == []:
        if not error:
            error = "no file"
        return jsonify({
            "status": 400,
            "error": error
        })

    file_names = []
    for x in files:
        filename = storage(x)
        file_names.append(filename)

    cur.execute("""
            UPDATE item
            SET photos = %s
            WHERE key = %s;
        """, (
        item["photos"] + file_names,
        item["key"]
    ))

    cur.execute("""
        SELECT item.*,
            CASE
                WHEN COUNT(feedback.*) = 0 THEN ARRAY[]::integer[]
                ELSE ARRAY_AGG(feedback.rating)
            END AS ratings
        FROM item
        LEFT JOIN feedback ON item.key = feedback.item_key
        WHERE item.key = %s
        GROUP BY item.key;
    """, (key,))
    item = cur.fetchone()

    cur.execute("""
        INSERT INTO log (
            key, date, user_key, action, entity_key, entity_type, misc
        ) VALUES (%s, %s, %s, %s, %s, %s, %s);
    """, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "added_photo",
        item["key"],
        "item",
        json.dumps({
            "added": ", ".join(file_names),
            "error": error
        })
    ))

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "item": item_schema(item),
        "error": error
    })


@bp.put("/item/photo/<key>")
def order_photo(key):

    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "item:edit_photo" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute('SELECT * FROM item WHERE key = %s;', (key,))
    item = cur.fetchone()
    if (
        not item
        or "photos" not in request.json
        or type(request.json["photos"]) is not list
        or set(item["photos"]) != set(
            [p.split("/")[-1] for p in request.json["photos"]])
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    in_photos = [p.split("/")[-1] for p in request.json["photos"]]

    cur.execute("""
    INSERT INTO log (
            key, date, user_key, action, entity_key, entity_type, misc
        ) VALUES (%s, %s, %s, %s, %s, %s, %s);
    """, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "arranged_photo",
        item["key"],
        "item",
        json.dumps({
            "from": item["photos"],
            "to": in_photos
        })
    ))

    cur.execute("""
            UPDATE item
            SET photos = %s
            WHERE key = %s;
        """, (
        in_photos,
        item["key"]
    ))

    cur.execute("""
        SELECT item.*,
            CASE
                WHEN COUNT(feedback.*) = 0 THEN ARRAY[]::integer[]
                ELSE ARRAY_AGG(feedback.rating)
            END AS ratings
        FROM item
        LEFT JOIN feedback ON item.key = feedback.item_key
        WHERE item.key = %s
        GROUP BY item.key;
    """, (key,))
    item = cur.fetchone()

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "item": item_schema(item)
    })


@bp.delete("/item/photo/<key>")
def delete_photo(key):

    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "item:edit_photo" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute('SELECT * FROM item WHERE key = %s;', (key,))
    item = cur.fetchone()
    if (
        not item
        or "active_photo" not in request.json
        or not request.json["active_photo"]
        or request.json["active_photo"].split("/")[-1] not in item["photos"]
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    file_name = request.json["active_photo"].split("/")[-1]

    storage(file_name, delete=True)

    item["photos"].remove(file_name)
    cur.execute("""
            UPDATE item
            SET photos = %s
            WHERE key = %s;
        """, (
        item["photos"],
        item["key"]
    ))

    if len(item["photos"]) == 0 and item["status"] == "live":
        cur.execute("""
                UPDATE item
                SET status = %s
                WHERE key = %s;
            """, (
            "draft",
            item["key"]
        ))

    cur.execute("""
        SELECT item.*,
            CASE
                WHEN COUNT(feedback.*) = 0 THEN ARRAY[]::integer[]
                ELSE ARRAY_AGG(feedback.rating)
            END AS ratings
        FROM item
        LEFT JOIN feedback ON item.key = feedback.item_key
        WHERE item.key = %s
        GROUP BY item.key;
    """, (key,))
    item = cur.fetchone()

    cur.execute("""
        INSERT INTO log (
            key, date, user_key, action, entity_key, entity_type, misc
        ) VALUES (%s, %s, %s, %s, %s, %s, %s);
    """, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "deleted_photo",
        item["key"],
        "item",
        json.dumps({"photo": file_name})
    ))

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "item": item_schema(item)
    })
