from flask import request
from .database import query
from .tools import now
from uuid import uuid4
import json


def user_schema(user, db):
    saves = query({"type": "save", "user": user["key"]}, True, db=db)
    _cart = query({
        "type": "cart",
        "key": f"{user['key']}_cart",
        "user": user["key"]}, db=db)

    cart = []
    if _cart:
        for x in _cart["items"]:
            variation = json.dumps(x['variation'], separators=(',', ':'))
            cart.append(f"{x['key']}_{variation}")
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

        "saves": [x["item"] for x in saves],
        "cart": cart
    }


def item_schema(item, db):
    photos = [f"{request.host_url}photos/{x}" for x in item["photos"]]

    rating = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for x in db:
        if x["type"] == "feedback" and x["item"] == item["key"]:
            rating[x["rating"]] += 1

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
        "rating": rating
    }


def order_schema(order, db):
    items = []

    for x in order["items"]:
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
        "user": order["user"],
        "receiver": order["receiver"],

        "items": items,

        "status": order["status"],
        "delivery_date": order["delivery_date"],

        "transaction": order["transaction"],
    }


def feedback_schema(fb, db):
    user = query({"type": "user", "key": fb["user"]}, db=db)

    return {
        "key": fb["key"],
        "user": {
            "key": user["key"],
            "name": user["name"],
            "photo": user["photo"],
        },
        "rating": fb["rating"],
        "review": fb["review"],
        "date": fb["date"],
    }


def log_schema(log, db):

    key = log["entity"]
    _type = log["entity_type"]

    if log["entity_type"] == "auth":
        log["entity_type"] = None
        log["entity"] = None

    elif log["entity_type"] == "cart":
        if log["action"] in ['added_to', 'removed_from',
                             'changed_quantity']:
            _type = "item"
            key = log["misc"]["key"]
            del log["misc"]["key"]
        else:
            log["entity"] = None

    elif log["entity_type"] == "advert":
        _type = "item"
        key = log["entity"].split("_")[0]

    user = {
        "name": "Deleted User" if log["user"] != "meji" else "Meji",
        "email": None
    }
    entity = None
    for x in db:
        if x["type"] == "user" and x["key"] == log["user"]:
            user = x

        elif log["entity"] and x["type"] == _type and x["key"] == key:
            entity = x

    return {
        "key": log["key"],
        "date": log["date"],
        "user": {
            "key": user["email"],
            "name": user["name"]
        },
        "action": log["action"],
        "entity": {
            "key": entity["slug"] if (
                entity and entity["type"] == "item"
            ) else log["entity"],
            "type": log["entity_type"],
            "name": entity["name"] if (
                entity and 'name' in entity
            ) else log["entity"],
        },
        "status": log["status"],
        "misc": log["misc"]
    }


def advert_schema(advert, db):
    item = query({"type": "item", "key": advert["item"]}, db=db)

    def get_url(dim):
        if advert['photos'][dim]:
            return f"{request.host_url}photos/{advert['photos'][dim]}"
        return None

    return {
        "key": advert["key"],
        "item": {
            "slug": item["slug"],
            "name": item["name"],
            "photo": f"{request.host_url}photos/{item['photos'][0]}",
        },
        "photos": {
            "300x300": get_url('300x300'),
            "300x600": get_url('300x600'),
            "600x300": get_url('600x300'),
            "900x300": get_url('900x300')
        },
        "places": advert["places"]
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
