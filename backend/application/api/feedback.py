from flask import Blueprint, jsonify, request
from .tools import token_to_user, now
from .schema import item_schema
from .database import database

bp = Blueprint("feedback", __name__)


@bp.get("/feedback/<key>")
def user_feedback_for_item(key):
    data = database()

    user = token_to_user(data)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    item = query("item", "alias", key, data)
    if not item:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    my_feedback = None
    for feedback in item["feedbacks"]:
        if feedback["user_key"] == user["key"]:
            my_feedback = feedback
            break

    i_have_gotten = None
    for row in db:
        if (
            row["type"] == "order"
            and row["user_key"] == user["key"]
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
        "data": {
            "item": item_schema(item, data),
            "give_feedback": i_have_gotten and not my_feedback,
            # "my_feedback": {
            #     "rating": my_feedback.rating if my_feedback else 0,
            #     "review": my_feedback.review if my_feedback else ""
            # }
        }
    })


@bp.post("/feedback/<key>")
def post(key):
    data = database()

    user = token_to_user(data)
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

    item = query("item", "key", key, data)
    if not item:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    has_feedback = None
    for feedback in item["feedbacks"]:
        if feedback["user_key"] == user["key"]:
            has_feedback = True
            feedback["rating"] = request.json["rating"]
            feedback["review"] = request.json["review"]
            break

    if not has_feedback:
        feedback = {
            "user_key": user["key"],
            "rating": request.json["rating"],
            "review": request.json["review"],
            "date": now(),
        }
        item["feedbacks"].append(feedback)

    item = database(item)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "item": item_schema(item, data)
        }
    })
