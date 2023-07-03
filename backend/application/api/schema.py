from flask import request
# from .photo import photo_url
from .database import query
from .tools import now
from werkzeug.security import generate_password_hash
from uuid import uuid4


def user_schema(user, db):
    user["saves"] = sorted(user["saves"], key=lambda d: d["date"])

    user["cart"] = sorted(user["cart"], key=lambda d: d["date"])
    cart = []
    for _cart in user["cart"]:
        item = query("item", "key", _cart["key"], db)
        if item:
            item = item_schema(item, db)
            item["variation"] = _cart["variation"]
            item["quantity"] = _cart["quantity"]
            cart.append(item)

    photo = None
    if user["photo"]:
        photo = f"{request.host_url}/{user['photo']}"

    return {
        "key": user["key"],

        "name": user["name"],
        "email": user["email"],
        "phone": user["phone"],
        "address": user["address"],
        "photo": photo,

        "acc_balance": user["acc_balance"],

        "setting": user["setting"],
        "roles": user["roles"] if "roles" in user else [],
        "status": user["status"],
        "login": user["login"],

        "saves": [save["key"] for save in user["saves"]],
        "cart": cart,
    }


def item_schema(item, db):
    categories = []

    for row in db:
        if row["type"] == "category" and item["key"] in row["items"]:
            categories.append(row)
    categories = sorted(categories, key=lambda d: d["order"])
    categories = [category["name"] for category in categories]

    photos = sorted(item["photos"], key=lambda d: d["order"])
    photos = [
        f"{request.host_url}/photos/{x['key']}" for x in photos]

    feedbacks = []
    user_keys = [x["user_key"] for x in item["feedbacks"]]
    for row in db:
        if row["type"] == "user" and row["key"] in user_keys:
            for feedback in item["feedbacks"]:
                if feedback["user_key"] == row["key"]:
                    photo = None
                    if row["photo"]:
                        photo = f"{request.host_url}/{row['photo']}"

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

    thumbnail = None
    if item["photos"] != []:
        f"{request.host_url}/{item['photos'][0]['key']}"

    return {
        "key": item["key"],

        "date_c": item["date_c"],
        "date_u": item["date_u"],

        "alias": item["alias"],
        "name": item["name"],
        "price": item["price"],
        "old_price": item["old_price"],
        "desc": item["desc"],
        "spec": item["spec"],

        "variation_options": item["variation_options"],

        "photos": photos,
        "thumbnail": thumbnail,
        "status": item["status"],

        "categories": categories,
        "feedbacks": feedbacks,
    }


def order_schema(order, db):
    items = []
    for cart in order["cart"]:
        item = db.get("item", "key", cart["key"], db)
        if item:
            item = item_schema(item, db)
            items.append({
                "alias": item["alias"],
                # "key": item["key"],
                "name": item["name"],
                "price": item["price"],
                "photo": item["photos"][0] if "photos" in item and len(
                    item["photos"]) >= 1 else "",
                "variation": cart["variation"],
                "quantity": cart["quantity"],
            })

    date = f"{now(4).split('T')[0]}T10:00"
    test = "delivery_date" in order
    order["delivery_date"] = order["delivery_date"] if test else date

    return {
        "key": order["key"],
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


def category_schema(category):
    return {
        "key": category["key"],
        "name": category["name"],
        "icon": category["icon"],
        "count": len(category["items"])
    }


def user_template(
        name,
        email,
        password
):
    return {
        "key": uuid4().hex,
        "v": uuid4().hex,
        "type": "user",
        "date_c": now(),
        "date_u": now(),
        "status": "anon",

        "name": name,
        "email": email,
        "phone": None,
        "password": generate_password_hash(
            password,
            method="scrypt"
        ),
        "address": {
            "line": None,
            "country": None,
            "state": None,
            "local_area": None,
            "postal_code": None,
        },
        "photo": None,
        "acc_balance": 0,
        "saves": [],
        "cart": [],
        "roles": [],  # admin, supplier,
        "login": False,
        "setting": {
            "item_view": "grid",
            "theme": "light"
        },
    }


def item_template(
    name,
    alias,
    price,
    old_price,
    desc,
    spec
):
    return {
        "key": uuid4().hex,
        "v": uuid4().hex,
        "type": "item",
        "status": "draft",
        "date_c": now(),
        "date_u": now(),

        "name": name,
        "alias": alias,
        "price": price,
        "old_price": old_price,
        "desc": desc,
        "spec": spec,
        "photos": [],
        "ads": {},

        "available_quantity": 0,
        "variation_options": {},
        "feedbacks": [],
    }


def log_template(
    for_,
    user,
    entity,
    action,
    status=None,
    note=None,
):
    return {
        "key": uuid4().hex,
        "date": now(),
        "type": "log",

        "for": for_,
        "user_key": user,
        "entity_key": entity,
        "action": action,
        "status": status,
        "note": note
    }
