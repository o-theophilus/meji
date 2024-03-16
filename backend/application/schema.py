from flask import request
from .tools import now


def user_schema(user, saves=[], cart=[]):
    return {
        "key": user["key"],

        "name": user["name"],
        "email": user["email"],
        "phone": user["phone"],
        "address": {
            "line": user["address_line"],
            "country": user["address_country"],
            "state": user["address_state"],
            "local_area": user["address_local_area"],
            "postal_code": user["address_postal_code"]
        },
        "photo": (f"{request.host_url}photos/{user['photo']}"
                  if user["photo"] else None),

        "account_balance": user["account_balance"],

        "setting": {
            "theme": user["setting_theme"],
            "item_view": user["setting_item_view"]
        },
        "roles": user["roles"],
        "status": user["status"],
        "login": user["login"],

        "saves": saves,
        "cart": cart
    }


def item_schema(item):
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

        "photos": [f"{request.host_url}photos/{x}" for x in item["photos"]],
        "status": item["status"],

        "tags": item["tags"],
        "ratings": item["ratings"]
    }


def order_schema(order):
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


def feedback_schema(fb):
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


def log_schema(log):

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
        "name": None if log["user"] != "meji" else "Meji",
        "email": log["user"] if log["user"] != "meji" else None
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


def advert_schema(advert):
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
