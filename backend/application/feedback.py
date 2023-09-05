from flask import Blueprint, jsonify, request
from .tools import token_to_user, now
from .schema import item_schema, feedback_schema
from .database import database, query
from uuid import uuid4

bp = Blueprint("feedback", __name__)


@bp.get("/feedback/<slug>")
def get_feedbacks(slug):
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    item = query({"type": "item", "slug": slug}, db=db)
    if not item:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    feedbacks = query({"type": "feedback", "item": item["key"]}, True, db=db)

    return jsonify({
        "status": 200,
        "item": item_schema(item, db),
        "feedbacks": [feedback_schema(x, db) for x in feedbacks]
    })


@bp.post("/feedback/<key>")
def add_feedback(key):
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    error = {}
    if "rating" not in request.json or not request.json["rating"]:
        error["rating"] = "this field is required"
    elif request.json["rating"] not in range(1, 6):
        error["rating"] = "invalid ratinng"
    if "review" not in request.json or not request.json["review"]:
        error["review"] = "This field is reqired"

    if error != {}:
        return jsonify({
            "status": 400,
            **error
        })

    item = query({"type": "item", "key": key}, db=db)
    if not item:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    fb = query({"type": "feedback", "user": user["key"],
                "item": item["key"]}, db=db)
    if fb:
        fb["rating"] = request.json["rating"]
        fb["review"] = request.json["review"]
        fb["date"] = now()
    else:
        fb = {
            "key": uuid4().hex,
            "type": "feedback",
            "user": user["key"],
            "item": item["key"],
            "rating": request.json["rating"],
            "review": request.json["review"],
            "date": now(),
        }
    database(fb)

    return jsonify({
        "status": 200,
        "feedback": feedback_schema(fb, db)
    })
