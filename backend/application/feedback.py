from flask import Blueprint, jsonify, request
from .tools import token_to_user, now
from .schema import item_schema, feedback_schema
from .database import database, query
from uuid import uuid4
from math import ceil

bp = Blueprint("feedback", __name__)


@bp.get("/feedback/<user_key>/<item_key>")
def get_feedbacks(user_key, item_key):
    db = database()

    item = query({"type": "item", "slug": item_key}, db=db)
    if not item:
        item = query({"type": "item", "key": item_key}, db=db)
    if not item:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    has_feedback = False
    has_purchased = False
    feedbacks = []
    for x in db:
        if x["type"] == "feedback" and x["item"] == item["key"]:
            feedbacks.append(x)
            if x["user"] == user_key:
                has_feedback = True
                has_purchased = True

        elif (
            not has_purchased
            and x["type"] == "order"
            and x["user"] == user_key
            and x["status"] == "delivered"
        ):
            for y in x["items"]:
                if y["item"] == item["key"]:
                    has_purchased = True
                    break

    sort = request.args["sort"] if "sort" in request.args else "latest"
    page_no = int(request.args["page_no"]) if "page_no" in request.args else 1
    size = int(request.args["size"]) if "size" in request.args else 24

    if sort == "latest":
        sort = "date"
    feedbacks = sorted(feedbacks, key=lambda d: d[sort], reverse=True)

    total_page = ceil(len(feedbacks) / size)
    start = (page_no - 1) * size
    stop = start + size
    feedbacks = feedbacks[start: stop]

    return jsonify({
        "status": 200,
        "item": item_schema(item, db),
        "feedbacks": [feedback_schema(x, db) for x in feedbacks],
        "give_feedback": has_purchased and not has_feedback,
        "total_page": total_page,
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

    return get_feedbacks(user["key"], item["key"])
