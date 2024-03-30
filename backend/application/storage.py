from flask import Blueprint, send_file, jsonify, request
from deta import Deta
from PIL import Image, ImageOps
from io import BytesIO
from uuid import uuid4
import os
from werkzeug.datastructures import FileStorage
from .tools import token_to_user
from .postgres import db_close, db_open


bp = Blueprint("storage", __name__)

sizes = ["300x300", "300x600", "600x300", "900x300"]


def drive():
    name = "live"
    return Deta(os.environ["DETA_KEY"]).Drive(name)


def storage(
    x=None,
    folder="photos",
    delete=False,
    thumbnail=False,
):
    if type(x) is str:
        if delete:
            return drive().delete(f"{folder}/{x}")

        photo = drive().get(f"{folder}/{x}")
        photo = Image.open(BytesIO(photo.read()))
        if thumbnail:
            size = int(thumbnail)
            photo = ImageOps.fit(photo, (size, size), Image.LANCZOS)
        file_io = BytesIO()
        photo.save(file_io, format="JPEG")
        file_io.seek(0)

        return file_io

    if isinstance(x, FileStorage):
        photo = Image.open(x).convert('RGBA')
        white = Image.new('RGBA', photo.size, (255, 255, 255))
        photo = Image.alpha_composite(white, photo).convert('RGB')

        if thumbnail:
            photo.thumbnail((1024, 1024), Image.LANCZOS)

        file_io = BytesIO()
        photo.save(file_io, format="JPEG")

        name = f"{uuid4().hex}.jpg"
        drive().put(f"{folder}/{name}", file_io.getvalue())

        return name


@bp.get("/photo/<key>")
@bp.get("/photo/<key>/<thumbnail>")
def get_photo(key, thumbnail=False):
    photo = storage(key, thumbnail=thumbnail)
    return send_file(photo, mimetype="image/jpg")


@bp.get("/photo/error")
def photo_error():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "admin:manage_photo" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute("""
        SELECT photo
        FROM "user";
    """)
    users_photo = cur.fetchall()
    users_photo = [x["photo"] for x in users_photo if x["photo"]]

    cur.execute("""
        SELECT photos
        FROM item;
    """)
    temp = cur.fetchall()
    items_photos = []
    for x in temp:
        if x["photos"] != []:
            items_photos += x["photos"]

    cur.execute("""
        SELECT *
        FROM advert;
    """)
    temp = cur.fetchall()
    adverts_photos = []
    for x in temp:
        for y in sizes:
            if x[f"photo_{y}"]:
                adverts_photos.append(x[f"photo_{y}"])

    all_used_photos = users_photo + items_photos + adverts_photos
    paths = drive().list()["names"]
    all_stored_photos = [x.split('/')[1] for x in paths]

    cur.execute("""
        SELECT "user".key, "user".name
        FROM "user"
        WHERE
            photo IS NOT NULL
            AND photo != ANY(%s);
    """, (all_stored_photos,))
    _users = cur.fetchall()

    cur.execute("""
        SELECT item.key, item.name
        FROM item
        WHERE NOT ARRAY[%s] @> photos;
    """, (all_stored_photos,))
    _items = cur.fetchall()

    cur.execute("""
        SELECT advert.key, item.name
        FROM advert
        LEFT JOIN item ON advert.key = item.key
        WHERE
            (
                photo_300x300 IS NOT NULL
                AND NOT photo_300x300 = ANY(%s)
            ) OR (
                photo_300x600 IS NOT NULL
                AND NOT photo_300x600 = ANY(%s)
            ) OR (
                photo_600x300 IS NOT NULL
                AND NOT photo_600x300 = ANY(%s)
            ) OR (
                photo_900x300 IS NOT NULL
                AND NOT photo_900x300 = ANY(%s)
            );
    """, (
        all_stored_photos, all_stored_photos,
        all_stored_photos, all_stored_photos
    ))
    _adverts = cur.fetchall()

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "unused": [f"{request.host_url}photo/{x}"
                   for x in all_stored_photos if x not in all_used_photos],
        "users": _users,
        "items": _items,
        "adverts": _adverts
    })


@bp.delete("/photo/error")
def delete_photo():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "admin:manage_photo" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    if (
        "photos" not in request.json
        or type(request.json["photos"]) is not list
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    for x in request.json["photos"]:
        pass
        storage(x.split("/")[-1], delete=True)

    db_close(con, cur)

    return jsonify({
        "status": 200
    })
