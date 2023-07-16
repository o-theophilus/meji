from flask import Blueprint, jsonify
from .database import database


bp = Blueprint("tag", __name__)


@bp.get("/tags")
def all_tags(db=None):
    if not db:
        db = database()

    tags = []
    for row in db:
        if row["type"] == "item":
            tags += row["tags"]

    tags = list(set(tags))

    return jsonify({
        "status": 200,
        "tags": tags
    })
