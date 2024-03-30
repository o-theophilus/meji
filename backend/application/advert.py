from flask import Blueprint, jsonify, request
from .tools import token_to_user
from .storage import storage
from PIL import Image
from math import ceil
from .postgres import db_close, db_open
from datetime import datetime
from uuid import uuid4
import json

bp = Blueprint("advert", __name__)


sizes = ["300x300", "300x600", "600x300", "900x300"]
spaces = ['home_1', 'home_2', 'home_3', 'shop', 'save']


def advert_schema(advert):
    for x in sizes:
        n = f"photo_{x}"
        if advert[n]:
            advert[n] = f"{request.host_url}photo/{advert[n]}"
    return advert


def null_advert(key):
    return {
        "key": key,
        "spaces": [],
        "photo_300x300": None,
        "photo_300x600": None,
        "photo_600x300": None,
        "photo_900x300": None
    }


@bp.post("/advert/<item_key>")
def add_photo(item_key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "item:advert" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute("""
        SELECT * FROM item WHERE slug = %s OR key = %s;
    """, (item_key, item_key))
    item = cur.fetchone()

    if not item or 'files' not in request.files:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("""
        SELECT * FROM advert WHERE key = %s;
    """, (item["key"],))
    advert = cur.fetchone()
    if not advert:
        cur.execute("""
            INSERT INTO advert (key) VALUES (%s) RETURNING *;
        """, (item["key"],))
        advert = cur.fetchone()

    error = ""
    log_misc = ""
    new_pick = []

    for x in request.files.getlist("files"):
        media, format = x.content_type.split("/")
        dim = Image.open(x).size
        dim = f"{dim[0]}x{dim[1]}"

        err = ""
        if media != "image" or format in ['svg+xml', 'x-icon']:
            err = f"{x.filename} => invalid file"
        elif dim not in sizes:
            err = f"{x.filename} => invalid dimension"
        elif advert[f"photo_{dim}"]:
            err = f"{x.filename} => slot occupied"
        elif dim in new_pick:
            err = f"{x.filename} => slot picked"

        if err:
            error = f"{error}, {err}" if error else err
        else:
            filename = storage(x)
            temp = f"{dim}: {filename}"
            log_misc = f"{log_misc}, {temp}" if log_misc else temp
            new_pick.append(dim)

            cur.execute("""
                UPDATE advert
                SET photo_{} = %s
                WHERE key = %s;
            """.format(dim), (filename, item["key"]))

    if not log_misc:
        return jsonify({
            "status": 400,
            "error": error if not error else "no file"
        })

    cur.execute("""
        INSERT INTO log (
            key, date, user_key, action, entity_key, entity_type, misc
        ) VALUES (%s, %s, %s, %s, %s, %s, %s);
    """, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "added_photo",
        advert["key"],
        "advert",
        json.dumps({"photo": log_misc})
    ))

    cur.execute("""
        SELECT *
        FROM advert
        WHERE key = %s;
    """, (item["key"],))
    advert = cur.fetchone()

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "advert": advert_schema(advert),
        "error": error
    })


@bp.get("/advert/<item_key>")
def get(item_key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "item:advert" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute("""
        SELECT * FROM item WHERE slug = %s OR key = %s;
    """, (item_key, item_key))
    item = cur.fetchone()
    if not item:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("""
        SELECT * FROM advert WHERE key = %s;
    """, (item["key"],))
    advert = cur.fetchone()

    if advert:
        cur.execute("""
            INSERT INTO log (
                key, date, user_key, action, entity_key, entity_type
            ) VALUES (%s, %s, %s, %s, %s, %s);
        """, (
            uuid4().hex,
            datetime.now(),
            user["key"],
            "viewed",
            advert["key"],
            "advert"
        ))

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "advert": advert_schema(advert) if advert else null_advert(
            item["key"]),
        "item": item,
        "spaces": spaces,
        "sizes": sizes
    })


# TODO: if item.status not live
@bp.get("/advert")
def get_all_advert(space="", is_ready=False):
    con, cur = db_open()

    page_no = int(request.args["page_no"]) if "page_no" in request.args else 1
    page_size = int(request.args["size"]) if "size" in request.args else 24
    space = request.args["status"] if "status" in request.args else space

    ready = ""
    if is_ready:
        for x in sizes:
            ready = f"{ready} AND photo_{x} IS NOT NULL"

    cur.execute("""
        SELECT
            advert.*,
            item.name AS name,
            item.slug AS slug,
            COALESCE(item.photos[1], NULL) AS photo,
            COUNT(*) OVER() AS total_items
        FROM advert
        LEFT JOIN item ON advert.key = item.key
        WHERE %s = '' OR %s = ANY(spaces) {}
        LIMIT %s OFFSET %s;
    """.format(ready), (
        space, space,
        page_size,
        (page_no - 1) * page_size
    ))
    adverts = cur.fetchall()

    for x in adverts:
        x["photo"] = f"{request.host_url}photo/{x['photo']}"

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "adverts": [advert_schema(x) for x in adverts],
        "spaces": spaces,
        "sizes": sizes,
        "total_page": ceil(adverts[0][
            "total_items"] / page_size) if adverts else 0
    })


@bp.delete("/advert/photo/<item_key>")
def delete_photo(item_key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "item:advert" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute("""
        SELECT * FROM item WHERE slug = %s OR key = %s;
    """, (item_key, item_key))
    item = cur.fetchone()

    cur.execute("""
        SELECT * FROM advert WHERE key = %s;
    """, (item["key"],))
    advert = cur.fetchone()

    if (
        not item
        or not advert
        or "size" not in request.json
        or not request.json["size"]
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    dim = request.json["size"]
    photo = advert[f"photo_{dim}"]

    if (
        dim not in sizes or not photo
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    storage(photo, delete=True)

    cur.execute(f"""
        UPDATE advert SET photo_{dim} = NULL
        WHERE key = %s;

        DELETE FROM advert
        WHERE
            photo_300X300 IS NULL
            AND photo_300X600 IS NULL
            AND photo_600X300 IS NULL
            AND photo_900X300 IS NULL;
    """, (item["key"],))

    cur.execute("SELECT * FROM advert WHERE key = %s;", (item["key"],))
    advert = cur.fetchone()

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
        "advert",
        json.dumps({"photo": f"{photo} ({dim})"})
    ))

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "advert": advert_schema(advert) if advert else null_advert(
            item["key"])
    })


@bp.delete("/advert/<item_key>")
def delete(item_key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "item:advert" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute("""
        SELECT * FROM item WHERE slug = %s OR key = %s;
    """, (item_key, item_key))
    item = cur.fetchone()

    cur.execute("""
        SELECT * FROM advert WHERE key = %s;
    """, (item["key"],))
    advert = cur.fetchone()

    if not item or not advert:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    log_misc = ""
    for x in sizes:
        if advert[f"photo_{x}"]:
            temp = f"{x}: {advert[f'photo_{x}']}"
            log_misc = f"{log_misc}, {temp}" if log_misc else temp
            storage(advert[f"photo_{x}"], delete=True)

    cur.execute("""
        DELETE FROM advert WHERE key = %s;
    """, (advert["key"],))

    cur.execute("""
        INSERT INTO log (
            key, date, user_key, action, entity_key, entity_type, misc
        ) VALUES (%s, %s, %s, %s, %s, %s, %s);
    """, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "deleted_photo",
        advert["key"],
        "advert",
        json.dumps({"photo": log_misc})
    ))

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "advert": null_advert(item["key"])
    })


@bp.put("/advert/<item_key>")
def ad_spaces(item_key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "item:advert" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute("""
        SELECT * FROM item WHERE slug = %s OR key = %s;
    """, (item_key, item_key))
    item = cur.fetchone()

    cur.execute("""
        INSERT INTO advert (key)
        VALUES (%s)
        ON CONFLICT (key) DO NOTHING;

        SELECT * FROM advert WHERE key = %s;
    """, (item["key"], item["key"]))
    advert = cur.fetchone()

    if (
        not item
        or not advert
        or "spaces" not in request.json
        or type(request.json["spaces"]) is not list
        or not all(y in spaces for y in request.json["spaces"])
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if [x for x in sizes if advert[f"photo_{x}"]] == []:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("""
        INSERT INTO log (
            key, date, user_key, action, entity_key, entity_type, misc
        ) VALUES (%s, %s, %s, %s, %s, %s, %s);
    """, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "changed_spaces",
        advert["key"],
        "advert",
        json.dumps({
            "from": advert["spaces"],
            "to": request.json["spaces"]
        })
    ))

    cur.execute("""
        UPDATE advert
        SET spaces = %s
        WHERE key = %s
        RETURNING *;
    """, (request.json["spaces"], item["key"],))
    advert = cur.fetchone()

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "advert": advert_schema(advert)
    })
