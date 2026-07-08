from flask import Blueprint, request
from PIL import Image
from psycopg2.extras import Json

from ...storage import storage
from ...tools import log, rate_limit, session
from .get import advert_schema, sizes, spaces

bp = Blueprint("advert", __name__)


@bp.post("/items/<key>/advert")
@session(True)
@rate_limit(20, 1)
@log("item")
def add_photo(cur, user, key):
    if "item.advert" not in user["access"]:
        return {
            "status": 403,
            "error": "unauthorized access"
        }, 403

    cur.execute("""SELECT * FROM item WHERE key = %s;""", (key,))
    item = cur.fetchone()
    if not item:
        return {
            "status": 404,
            "error": "invalid request"
        }, 404

    if 'files' not in request.files:
        return {
            "status": 422,
            "error": "invalid request"
        }, 422

    cur.execute("""SELECT * FROM advert WHERE key = %s;""", (key,))
    advert = cur.fetchone()
    if not advert:
        cur.execute("""
            INSERT INTO advert (key) VALUES (%s) RETURNING *;
        """, (key,))
        advert = cur.fetchone()

    error = ""
    picked_dimension = []
    files = []

    for x in request.files.getlist("files"):
        dim = Image.open(x).size
        dim = f"{dim[0]}x{dim[1]}"
        err = ""

        if x.content_type not in ['image/jpeg', 'image/png']:
            err = f"{x.filename} => invalid file"
        elif dim not in sizes:
            err = f"{x.filename} => invalid dimension"
        elif dim in advert["photo"]:
            err = f"{x.filename} => slot occupied"
        elif dim in picked_dimension:
            err = f"{x.filename} => slot picked"

        if err:
            error = f"{error}, {err}" if error else err
        else:
            picked_dimension.append(dim)
            files.append(x)

    if files == []:
        if not error:
            error = "no file"
        return {
            "status": 422,
            "error": error
        }, 422

    old_photo = advert["photo"]
    for x in files:
        dim = Image.open(x).size
        dim = f"{dim[0]}x{dim[1]}"
        filename = storage.save(x, item["name"], "item_advert")
        advert["photo"][dim] = filename

    cur.execute("""
        UPDATE advert SET photo = %s
        WHERE key = %s RETURNING *;
    """, (Json(advert["photo"]), advert["key"]))
    advert = cur.fetchone()

    out = {
        "status": 200,
        "advert": advert_schema(advert),
        "log": {
            "entity_key": advert["key"],
            "misc": {
                "from": old_photo,
                "to": advert["photo"]
            }

        }
    }

    if error:
        out["error"] = error

    return out, 200


@bp.put("/items/<key>/advert")
@session(True)
@rate_limit(20, 1)
@log("item")
def set_photo(cur, user, key):
    if "item.advert" not in user["access"]:
        return {
            "status": 403,
            "error": "unauthorized access"
        }, 403

    cur.execute("""SELECT * FROM item WHERE key = %s;""", (key, ))
    item = cur.fetchone()
    cur.execute("""SELECT * FROM advert WHERE key = %s;""", (key,))
    advert = cur.fetchone()
    if not item or not advert:
        return {
            "status": 404,
            "error": "invalid request"
        }, 404

    photo_selected = request.json.get("photo_selected")
    spaces_selected = request.json.get("spaces_selected")
    if (
        type(photo_selected) is not list
        or type(spaces_selected) is not list
        or not all(y in sizes for y in photo_selected)
        or not all(y in spaces for y in spaces_selected)
    ):
        return {
            "status": 422,
            "error": "invalid request"
        }, 422

    new_advert_photo = {}
    for key, val in advert["photo"].items():
        if key not in photo_selected:
            storage.delete(advert["photo"][key], "item_advert")
        else:
            new_advert_photo[key] = val

    misc = {
        "from photo": advert["photo"],
        "to photo": {},
        "from space": advert["space"],
        "to space": {},
    }

    if new_advert_photo == {}:
        cur.execute("""
            DELETE FROM advert WHERE WHERE key = %s;
        """, (advert["key"],))
        advert = None
    else:
        cur.execute("""
            UPDATE advert SET photo = %s, space = %s
            WHERE key = %s RETURNING *;
        """, (Json(new_advert_photo), spaces_selected, advert["key"],))
        advert = cur.fetchone()

        misc["to photo"] = advert["photo"]
        misc["to space"] = advert["space"]

    return {
        "status": 200,
        "advert": advert_schema(advert) if advert else None,
        "log": {
            "entity_key": advert["key"],
            "misc": misc
        }
    }, 200
