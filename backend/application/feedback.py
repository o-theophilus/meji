from flask import Blueprint, jsonify, request
from .tools import token_to_user, now
from .schema import item_schema
from .database import database, query

bp = Blueprint("feedback", __name__)


@bp.get("/feedback/<key>")
def user_feedback_for_item(key):
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    item = query("item", "slug", key, db)
    if not item:
        return jsonify({
            "status": 400,
            "message": "invalid request"
        })

    my_feedback = None
    for feedback in item["feedbacks"]:
        if feedback["user"] == user["key"]:
            my_feedback = feedback
            break

    i_have_gotten = None
    for row in db:
        if (
            row["type"] == "order"
            and row["user"] == user["key"]
            and row["status"] == "delivered"
        ):
            for _item in row["cart"]:
                if _item["key"] == item["key"]:
                    i_have_gotten = _item
                    break

            if i_have_gotten:
                break

    return jsonify({
        "status": 200,
        "message": "successful",
        "db": {
            "item": item_schema(item, db),
            "give_feedback": i_have_gotten and not my_feedback,
            # "my_feedback": {
            #     "rating": my_feedback.rating if my_feedback else 0,
            #     "review": my_feedback.review if my_feedback else ""
            # }
        }
    })


@bp.post("/feedback/<key>")
def post(key):
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    error = {}
    if "rating" not in request.json or not request.json["rating"]:
        error["rating"] = "This field is required"
    elif request.json["rating"] not in range(1, 6):
        error["rating"] = "invalid ratinng"

    if "review" not in request.json or not request.json["review"]:
        error["review"] = "This field is reqired"

    if error != {}:
        return jsonify({
            "status": 201,
            "message": error
        })

    item = query("item", "key", key, db)
    if not item:
        return jsonify({
            "status": 400,
            "message": "invalid request"
        })

    has_feedback = None
    for feedback in item["feedbacks"]:
        if feedback["user"] == user["key"]:
            has_feedback = True
            feedback["rating"] = request.json["rating"]
            feedback["review"] = request.json["review"]
            break

    if not has_feedback:
        feedback = {
            "user": user["key"],
            "rating": request.json["rating"],
            "review": request.json["review"],
            "date": now(),
        }
        item["feedbacks"].append(feedback)

    item = database(item)

    return jsonify({
        "status": 200,
        "message": "successful",
        "db": {
            "item": item_schema(item, db)
        }
    })
