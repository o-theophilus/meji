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

    has_feedback = False
    for x in feedbacks:
        if x["user"] == user["key"]:
            has_feedback = True
            break

    has_purchased = False
    if has_feedback:
        has_purchased = True
    else:
        for x in db:
            if x["type"] == "order" and x["user"] == user["key"]:
                for y in x["items"]:
                    if y["item"] == item["key"]:
                        has_purchased = True
                        break
            if has_purchased:
                break

    return jsonify({
        "status": 200,
        "item": item_schema(item, db),
        "feedbacks": [feedback_schema(x, db) for x in feedbacks],
        "has_purchased": has_purchased,
        "has_feedback": has_feedback
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
        error["rating"] = "invalid rating"
    if "review" not in request.json or not request.json["review"]:
        error["review"] = "This field is required"

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

    has_purchased = False
    for x in db:
        if x["type"] == "order" and x["user"] == user["key"]:
            for y in x["items"]:
                if y["item"] == item["key"]:
                    has_purchased = True
                    break
        if has_purchased:
            break

    if not has_purchased:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    feedback = query({"type": "feedback", "user": user["key"],
                      "item": item["key"]}, db=db)
    if feedback:
        feedback["rating"] = request.json["rating"]
        feedback["review"] = request.json["review"]
        feedback["date"] = now()
    else:
        feedback = {
            "key": uuid4().hex,
            "type": "feedback",
            "user": user["key"],
            "item": item["key"],
            "rating": request.json["rating"],
            "review": request.json["review"],
            "date": now(),
        }
    database(feedback)

    return jsonify({
        "status": 200,
        "feedback": feedback_schema(feedback, db)
    })
