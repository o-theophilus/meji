# from flask import current_app
from deta import Deta
from PIL import Image, ImageOps
from io import BytesIO, IOBase
from uuid import uuid4
import os


def drive():
    name = "meji"
    # if current_app.config["DEBUG"]:
    #     name = "test"
    return Deta(os.environ["DETA_KEY"]).Drive(name)


def storage(x=None, folder="photos",
            delete=False, thumbnail=False, compress=False):
    if type(x) == str:
        if delete:
            return drive().delete(f"{folder}/{x}")

        photo = drive().get(f"{folder}/{x}")
        if thumbnail:
            temp = Image.open(BytesIO(photo.read()))
            temp = ImageOps.fit(temp, (200, 200), Image.LANCZOS)

            photo = BytesIO()
            temp.save(photo, format="JPEG")
            photo.seek(0)

        return photo

    if isinstance(x, IOBase):
        file_io = BytesIO()

        x.save(file_io)
        if compress:
            photo = Image.open(x).convert('RGBA')
            white = Image.new('RGBA', photo.size, (255, 255, 255))
            photo = Image.alpha_composite(white, photo).convert('RGB')
            photo.thumbnail((1024, 1024), Image.LANCZOS)
            photo.save(file_io, format="JPEG")

        name = f"{uuid4().hex}.jpg"
        drive().put(f"{folder}/{name}", file_io.getvalue())

        return name
