from flask import Blueprint, jsonify, request
from .tools import token_to_user
from .storage import storage
from .log import log_template
from PIL import Image
from math import ceil
from .postgres import db_close, db_open
from datetime import datetime
from uuid import uuid4
import json

bp = Blueprint("advert", __name__)


dimensions = ["300x300", "300x600", "600x300", "900x300"]
ad_space = ['home_1', 'home_2', 'home_3', 'shop', 'save']


# def advert_schema(advert):
#     item = query({"type": "item", "key": advert["item"]}, db=db)

#     def get_url(dim):
#         if advert['photos'][dim]:
#             return f"{request.host_url}photos/{advert['photos'][dim]}"
#         return None

#     return {
#         "key": advert["key"],
#         "item": {
#             "slug": item["slug"],
#             "name": item["name"],
#             "photo": f"{request.host_url}photos/{item['photos'][0]}",
#         },
#         "photos": {
#             "300x300": get_url('300x300'),
#             "300x600": get_url('300x600'),
#             "600x300": get_url('600x300'),
#             "900x300": get_url('900x300')
#         },
#         "places": advert["places"]
#     }


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
        SELECT * FROM item WHERE slug = %s or key = %s;
    """, (item_key,))
    item = cur.fetchone()

    cur.execute("""
        INSERT INTO advert (key)
        VALUES (%s)
        ON CONFLICT (key) DO NOTHING;

        SELECT * FROM advert WHERE key = %s;
    """, (item["key"], item["key"]))
    advert = cur.fetchone()

    if not item or 'files' not in request.files:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = ""
    log_misc = ""
    for x in request.files.getlist("files"):
        media, format = x.content_type.split("/")
        dim = Image.open(x).size
        dim = f"{dim[0]}x{dim[1]}"

        err = ""
        if media != "image" or format in ['svg+xml', 'x-icon']:
            err = f"{x.filename} => invalid file"
        elif dim not in dimensions:
            err = f"{x.filename} => invalid dimension"
        elif advert[f"photo_{dim}"]:
            err = f"{x.filename} => already picked"

        if err:
            error = f"{error}, {err}" if error else err
        else:
            filename = storage(x)
            temp = f"{dim}: {filename}"
            log_misc = f"{log_misc}, {temp}" if log_misc else temp
            cur.execute("""
                UPDATE advert
                SET photo_%s = %s
                WHERE key = %s
                RETURNING *;
            """, (dim, filename, item["key"]))
            advert = cur.fetchone()

    if not log_misc:
        return jsonify({
            "status": 400,
            "error": error if not error else "no file"
        })

    cur.execute(log_template, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "added_photo",
        advert["key"],
        "advert",
        200,
        json.dumps({"photo": log_misc})
    ))

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "advert": advert,
        # "advert": advert_schema(advert),
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
        SELECT * FROM item WHERE slug = %s or key = %s;
    """, (item_key, item_key))
    item = cur.fetchone()

    cur.execute("""
        SELECT * FROM advert WHERE key = %s;
    """, (item["key"],))
    advert = cur.fetchone()

    if not item:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if advert:
        cur.execute(log_template, (
            uuid4().hex,
            datetime.now(),
            user["key"],
            "viewed",
            advert["key"],
            "advert",
            200,
            None
        ))

    db_close(con, cur)

    return jsonify({
        "status": 200,
        # "advert": advert_schema(advert) if advert else None,
        "advert": advert,
        "ad_space": ad_space
    })


@bp.get("/advert")
def get_all_advert(placement=""):
    con, cur = db_open()

    page_no = int(request.args["page_no"]) if "page_no" in request.args else 1
    page_size = int(request.args["size"]) if "size" in request.args else 24
    place = request.args["status"] if "status" in request.args else placement

    cur.execute("""
        SELECT *, COUNT(*) OVER() AS total_items
        FROM advert
        WHERE %s = ANY(placement)
        LIMIT %s OFFSET %s;
    """, (
        place,
        page_size,
        (page_no - 1) * page_size
    ))
    adverts = cur.fetchall()

    db_close(con, cur)

    return jsonify({
        "status": 200,
        # "adverts": [advert_schema(x) for x in adverts],
        "adverts": adverts,
        "ad_space": ad_space,
        "total_page": ceil(adverts[0]["total_items"] / page_size) if adverts else 0
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
        SELECT * FROM item WHERE slug = %s or key = %s;
    """, (item_key,))
    item = cur.fetchone()

    cur.execute("""
        SELECT * FROM advert WHERE key = %s;
    """, (item["key"], item["key"]))
    advert = cur.fetchone()

    if (
        not item
        or not advert
        or "photo" not in request.json
        or not request.json["photo"]
        or "size" not in request.json
        or not request.json["size"]
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    dim = request.json["size"]

    if (
        dim not in dimensions or
        request.json["photo"].split("/")[-1] != advert[f"photos_{dim}"]
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    storage(advert[f"photos_{dim}"], delete=True)

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

    cur.execute(log_template, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "deleted_photo",
        advert["key"],
        "advert",
        200,
        json.dumps({f"{request.json['size']}: {request.json['photo']}"})
    ))

    db_close(con, cur)

    return jsonify({
        "status": 200,
        # "advert": advert_schema(advert) if advert else None,
        "advert": advert,
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
        SELECT * FROM item WHERE slug = %s or key = %s;
    """, (item_key,))
    item = cur.fetchone()

    cur.execute("""
        SELECT * FROM advert WHERE key = %s;
    """, (item["key"], item["key"]))
    advert = cur.fetchone()

    if not item or not advert:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    log_misc = ""
    for x in dimensions:
        if advert[f"photos_{x}"]:
            temp = f"{x}: {advert[f'photos_{x}']}"
            log_misc = f"{log_misc}, {temp}" if log_misc else temp
            storage(advert[f"photos_{x}"], delete=True)

    cur.execute(log_template, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "deleted_photo",
        advert["key"],
        "advert",
        200,
        json.dumps({"photo": log_misc})
    ))

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "advert": None
    })


@bp.put("/advert/<item_key>")
def placement(item_key):
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
        SELECT * FROM item WHERE slug = %s or key = %s;
    """, (item_key,))
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
        or "places" not in request.json
        or type(request.json["places"]) is not list
        or not all(y in ad_space for y in request.json["places"])
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    for x in dimensions:
        if not advert[f"photos_{x}"]:
            return jsonify({
                "status": 400,
                "error": "invalid request"
            })

    cur.execute(log_template, (
        uuid4().hex,
        datetime.now(),
        user["key"],
        "changed_placement",
        advert["key"],
        "advert",
        200,
        json.dumps({
            "from": advert["places"],
            "to": request.json["places"]
        })
    ))

    cur.execute("""
        UPDATE advert
        SET placement = %s
        WHERE key = %s
        RETURNING *;
    """, (request.json["places"], item["key"],))
    advert = cur.fetchone()

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "advert": advert
        # "advert": advert_schema(advert)
    })
