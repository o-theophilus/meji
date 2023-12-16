from flask import Blueprint, send_file, jsonify, request
from deta import Deta
from PIL import Image, ImageOps
from io import BytesIO
from uuid import uuid4
import os
from werkzeug.datastructures import FileStorage
from .tools import token_to_user
from .database import database


bp = Blueprint("storage", __name__)


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


@bp.get("/photos/<key>")
@bp.get("/photos/<key>/<thumbnail>")
def get_photo(key, thumbnail=False):
    photo = storage(key, thumbnail=thumbnail)
    return send_file(photo, mimetype="image/jpg")


@bp.get("/photo_error")
def photo_error():
    db = database()

    user = token_to_user()
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

    stored_photos = []
    paths = drive().list()["names"]
    for x in paths:
        stored_photos.append(x.split('/')[1])

    users = []
    items = []
    adverts = []
    used_photos = []
    for x in db:

        if x["type"] == "user" and x["photo"]:
            used_photos.append(x["photo"])
            if x["photo"] not in stored_photos:
                users.append({
                    "key": x["key"],
                    "name": x["name"],
                })

        elif x["type"] == "item" and x["photos"] != []:
            used_photos += x["photos"]
            if not all(y in stored_photos for y in x["photos"]):
                items.append({
                    "key": x["key"],
                    "name": x["name"],
                })

        elif x["type"] == "advert":
            x["photos"] = [y for y in x["photos"].values() if y is not None]
            if x["photos"] != []:
                used_photos += x["photos"]
                if not all(y in stored_photos for y in x["photos"]):
                    adverts.append({
                        "key": x["item"],
                        "name": x["key"],
                    })

    unused = [f"{request.host_url}photos/{x}"
              for x in stored_photos if x not in used_photos]

    return jsonify({
        "status": 200,
        "unused": unused,
        "users": users,
        "items": items,
        "adverts": adverts,
    })


@bp.delete("/photo_error")
def delete_photo():
    db = database()

    user = token_to_user()
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

    return jsonify({
        "status": 200
    })
