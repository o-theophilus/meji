from flask import Blueprint, jsonify, request
from PIL import Image
from psycopg2.extras import Json
from ...tools import get_session
from ...storage import storage
from ...postgres import db_open, db_close
from ...log import log
from .get import advert_schema, sizes, spaces

bp = Blueprint("advert", __name__)


@bp.post("/advert/<key>")
def add_photo(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "item:advert" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute("""SELECT * FROM item WHERE key = %s;""", (key,))
    if not cur.fetchone() or 'files' not in request.files:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("""SELECT * FROM advert WHERE key = %s;""", (key,))
    advert = cur.fetchone()
    if not advert:
        cur.execute("""
            INSERT INTO advert (key) VALUES (%s) RETURNING *;
        """, (key,))
        advert = cur.fetchone()

        log(
            cur=cur,
            user_key=user["key"],
            action="created",
            entity_key=advert["key"],
            entity_type="advert"
        )

    error = ""
    new_pick = []
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
        elif dim in new_pick:
            err = f"{x.filename} => slot picked"

        if err:
            error = f"{error}, {err}" if error else err
        else:
            new_pick.append(dim)
            files.append(x)

    if files == []:
        if not error:
            error = "no file"
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": error
        })

    old_photo = advert["photo"]
    for x in files:
        dim = Image.open(x).size
        dim = f"{dim[0]}x{dim[1]}"
        filename = storage.save(x, "item_advert")
        advert["photo"][dim] = filename

    cur.execute("""
        UPDATE advert SET photo = %s
        WHERE key = %s RETURNING *;
    """, (Json(advert["photo"]), advert["key"]))
    advert = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action=f"added advert photo{'s' if files != [] else ''}",
        entity_key=advert["key"],
        entity_type="advert",
        misc={"from": old_photo, "to": advert["photo"]}
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "advert": advert_schema(advert),
        "error": error
    })


@bp.delete("/advert/photo/<key>")
def delete_photo(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "item:advert" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    to_delete = request.json.get("to_delete")

    cur.execute("""SELECT * FROM item WHERE key = %s;""", (key, ))
    item = cur.fetchone()
    cur.execute("""SELECT * FROM advert WHERE key = %s;""", (key,))
    advert = cur.fetchone()

    if (
        not item
        or not advert
        or type(to_delete) is not list
        or to_delete == []
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    old_photo = advert["photo"]
    for x in to_delete:
        if x in advert["photo"]:
            storage.delete(advert["photo"][x], "item_advert")
            del advert["photo"][x]

    if advert["photo"] != {}:
        cur.execute("""
            UPDATE advert SET photo = %s WHERE key = %s RETURNING *;
        """, (Json(advert["photo"]), advert["key"],))
        advert = cur.fetchone()

        log(
            cur=cur,
            user_key=user["key"],
            action="deleted photo",
            entity_key=advert["key"],
            entity_type="advert",
            misc={"from": old_photo, "to": advert["photo"]}
        )
    else:
        cur.execute("""
            DELETE FROM advert WHERE WHERE key = %s;
        """, (advert["key"],))

        log(
            cur=cur,
            user_key=user["key"],
            action="deleted advert",
            entity_key=advert["key"],
            entity_type="advert"
        )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "advert": advert_schema(advert) if advert["photo"] != {} else None
    })


@bp.put("/advert/<key>")
def ad_spaces(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "item:advert" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    space = request.json.get("space")

    cur.execute("""SELECT * FROM item WHERE key = %s;""", (key,))
    item = cur.fetchone()
    cur.execute("""SELECT * FROM advert WHERE key = %s;""", (key,))
    advert = cur.fetchone()

    if (
        not item
        or not advert
        or type(space) is not list
        or not all(y in spaces for y in space)
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    old_soace = advert["space"]
    cur.execute("""
        UPDATE advert SET space = %s
        WHERE key = %s RETURNING *;
    """, (space, advert["key"]))
    advert = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="changed advert space",
        entity_key=advert["key"],
        entity_type="advert",
        misc={"from": old_soace, "to": advert["space"]}
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "advert": advert_schema(advert)
    })
