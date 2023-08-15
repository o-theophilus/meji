from flask import request
from .database import query
from .tools import now
from uuid import uuid4


def user_schema(user, db):
    user["saves"] = sorted(user["saves"], key=lambda d: d["date"])

    user["cart"] = sorted(user["cart"], key=lambda d: d["date"])
    cart = []
    for x in user["cart"]:
        item = query({"type": "item", "key": x["key"]}, db=db)
        if item:
            item = item_schema(item, db)
            item["variation"] = x["variation"]
            item["quantity"] = x["quantity"]
            cart.append(item)

    return {
        "key": user["key"],

        "name": user["name"],
        "email": user["email"],
        "phone": user["phone"],
        "address": user["address"],
        "photo": (f"{request.host_url}photos/{user['photo']}"
                  if user["photo"] else None),

        "acc_balance": user["acc_balance"],

        "setting": user["setting"],
        "roles": user["roles"] if "roles" in user else [],
        "status": user["status"],
        "login": user["login"],

        "saves": [x["key"] for x in user["saves"]],
        "cart": cart,
    }


def item_schema(item, db):
    photos = [f"{request.host_url}photos/{x}" for x in item["photos"]]

    feedbacks = []
    user_keys = [x["user_key"] for x in item["feedbacks"]]
    for row in db:
        if row["type"] == "user" and row["key"] in user_keys:
            for feedback in item["feedbacks"]:
                if feedback["user_key"] == row["key"]:
                    photo = None
                    if row["photo"]:
                        photo = f"{request.host_url}photos/{row['photo']}"

                    feedbacks.append({
                        "user_key": row["key"],
                        "photo": photo,
                        "name": row["name"],
                        "rating": feedback["rating"],
                        "review": feedback["review"],
                        "date":  feedback[
                            "date"] if "date" in feedback else "10-01-01",
                    })
                    user_keys = [x for x in user_keys if x != row["key"]]
                    break

            if user_keys == []:
                break

    return {
        "key": item["key"],

        "date_c": item["date_c"],
        "date_u": item["date_u"],

        "slug": item["slug"],
        "name": item["name"],
        "price": item["price"],
        "old_price": item["old_price"],
        "info": item["info"],

        "variation": item["variation"],

        "photos": photos,
        "status": item["status"],

        "tags": item["tags"],
        "feedbacks": feedbacks,
    }


def order_schema(order, db):
    items = []
    for x in order["cart"]:
        item = query({"type": "item", "key": x["key"]}, db=db)
        if item:
            items.append({
                "slug": item["slug"],
                "name": item["name"],
                "price": item["price"],
                "photo": (f"{request.host_url}photos/{item['photos'][0]}"
                          if len(item["photos"]) >= 1 else ""),
                "variation": x["variation"],
                "quantity": x["quantity"],
            })

    if "delivery_date" not in order:
        order["delivery_date"] = f"{now(4).split('T')[0]}T10:00"

    return {
        "key": order["key"],
        "user_key": order["user_key"],
        "recipient": order["recipient"],

        "items": items,

        "status": order["status"],
        "delivery_date": order["delivery_date"],

        "info": order["info"],
    }


def feedback_schema(fb):
    # user = db("user").get(fb["user_key"])
    # temp["user"] = user_schema(user, db)
    return {
        "key": fb["key"],
        "rating": fb["rating"],
        "review": fb["review"],
        "date": fb["date_c"],
    }


def log_template(
    user,
    action,
    entity,
    status=200,
    misc=None,
):
    return {
        "key": uuid4().hex,
        "date": now(),
        "type": "log",

        "user": user,
        "action": action,
        "entity": entity,
        "status": status,
        "misc": misc
    }


def otp_template(
    user,
    entity,
    otp,
):
    return {
        "key": uuid4().hex,
        "date": now(),
        "type": "otp",

        "user": user,
        "entity": entity,
        "otp": otp,
    }
