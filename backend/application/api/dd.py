# from flask import current_app
from deta import Deta
from PIL import Image, ImageOps
from io import BytesIO
from uuid import uuid4
import os


def drive():
    name = "meji"
    # if current_app.config["DEBUG"]:
    #     name = "test"
    return Deta(os.environ["DETA_KEY"]).Drive(name)


def add(file, compress=False):
    file_byte = BytesIO()

    if compress:
        file = Image.open(file).convert('RGBA')
        white = Image.new('RGBA', file.size, (255, 255, 255))
        file = Image.alpha_composite(white, file).convert('RGB')
        file.thumbnail((1024, 1024), Image.LANCZOS)

        file.save(file_byte, format="JPEG")
    else:
        file.save(file_byte)

    path = f"photos/{uuid4().hex}.jpg"
    drive().put(path, file_byte.getvalue())
    return path


def rem(path):
    return drive().delete(f"photos/{path}")


def get(path, thumbnail=False):
    photo = drive().get(path)

    if thumbnail:
        temp = Image.open(BytesIO(photo.read()))
        temp = ImageOps.fit(temp, (200, 200), Image.LANCZOS)

        photo = BytesIO()
        temp.save(photo, format="JPEG")
        photo.seek(0)

    return photo


def file_list():
    paths = drive().list()["names"]

    for x in paths:
        photo = drive().get(x)
        drive().put(f"photos/{x.split('/')[1]}", photo)
        drive().delete(x)
