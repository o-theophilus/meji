from flask import Blueprint, jsonify, request
from .tools import token_to_user
from .storage import storage
from PIL import Image
from math import ceil
from .postgres import db_close, db_open
from .log import log

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

    if "item:advert" not in user["permissions"]:
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

        log(
            cur=cur,
            user_key=user["key"],
            action="created",
            entity_key=advert["key"],
            entity_type="advert"
        )

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

    log(
        cur=cur,
        user_key=user["key"],
        action="added_photo",
        entity_key=advert["key"],
        entity_type="advert",
        misc={"photo": log_misc}
    )

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

    if "item:advert" not in user["permissions"]:
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

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "advert": advert_schema(advert) if advert else null_advert(
            item["key"]),
        "item": item,
        "spaces": spaces,
        "sizes": sizes
    })


@bp.get("/advert")
def get_many(status="", space=""):
    con, cur = db_open()

    page_no = int(request.args["page_no"]) if "page_no" in request.args else 1
    page_size = int(request.args["size"]) if "size" in request.args else 24
    space = request.args["space"] if "space" in request.args else space
    order = request.args["order"] if "order" in request.args else "latest"

    ready = ""
    if status == "live":
        for x in sizes:
            ready = f"{ready} AND photo_{x} IS NOT NULL"

    order_by = {
        'latest': 'log.date',
        'oldest': 'log.date',
        'name (a-z)': 'item.name',
        'name (z-a)': 'item.name'
    }

    order_dir = {
        'latest': 'DESC',
        'oldest': 'ASC',
        'name (a-z)': 'ASC',
        'name (z-a)': 'DESC'
    }

    print(space)

    cur.execute("""
        SELECT
            DISTINCT ON (advert.key)
            advert.*,
            item.name,
            item.slug,
            item.status,
            COALESCE(item.photos[1], NULL) AS photo,
            COUNT(*) OVER() AS total_items
        FROM advert
        LEFT JOIN item ON advert.key = item.key
        LEFT JOIN log ON advert.key = log.entity_key
        WHERE (
                %s = '' OR item.status = %s
            ) AND (
                %s = '' OR %s = ANY(spaces)
            ) {}
            AND log.action = 'created'
            AND log.entity_type = 'advert'
        ORDER BY advert.key, {} {}
        LIMIT %s OFFSET %s;
    """.format(ready, order_by[order], order_dir[order]), (
        status, status,
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
        "order_by": list(order_by.keys()),
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

    if "item:advert" not in user["permissions"]:
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
        WHERE key = %s
        RETURNING *;
    """, (item["key"],))
    advert = cur.fetchone()

    has_photo = False
    for x in sizes:
        if advert[f"photo_{x}"]:
            has_photo = True
            break

    if not has_photo:
        cur.execute("""
            DELETE FROM advert
            WHERE WHERE key = %s;
        """, (advert["key"],))

        log(
            cur=cur,
            user_key=user["key"],
            action="deleted",
            entity_key=advert["key"],
            entity_type="advert"
        )

    log(
        cur=cur,
        user_key=user["key"],
        action="deleted_photo",
        entity_key=advert["key"],
        entity_type="advert",
        misc={"photo": f"{photo} ({dim})"}
    )

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "advert": advert_schema(advert) if has_photo else null_advert(
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

    if "item:advert" not in user["permissions"]:
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

    log(
        cur=cur,
        user_key=user["key"],
        action="deleted_photo",
        entity_key=advert["key"],
        entity_type="advert",
        misc={"photo": log_misc}
    )
    log(
        cur=cur,
        user_key=user["key"],
        action="deleted",
        entity_key=advert["key"],
        entity_type="advert"
    )

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

    if "item:advert" not in user["permissions"]:
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

    log(
        cur=cur,
        user_key=user["key"],
        action="changed_spaces",
        entity_key=advert["key"],
        entity_type="advert",
        misc={
            "from": advert["spaces"],
            "to": request.json["spaces"]
        }
    )

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
