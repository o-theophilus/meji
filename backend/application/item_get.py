from flask import Blueprint, jsonify, request
from .tools import token_to_user
from .schema import item_schema
from .log import log_template
from math import ceil
from .database import database, query
import re

bp = Blueprint("item_get", __name__)


@bp.get("/tags")
def all_tags(db=None):
    if not db:
        db = database()

    tags = []
    for x in db:
        if x["type"] == "item" and x["status"] == "live":
            tags += x["tags"]

    tags_count = []
    unique_tags = []
    for x in tags:
        if x not in unique_tags:
            unique_tags.append(x)
            tags_count.append({
                "tag":  x,
                "count":  tags.count(x)
            })

    tags_count = sorted(tags_count, key=lambda d: d["count"], reverse=True)

    return jsonify({
        "status": 200,
        "tags": [x["tag"] for x in tags_count]
    })


@bp.get("/item/<key>")
def get(key):
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    item = query({"type": "item", "slug": key}, db=db)
    if not item:
        item = query({"type": "item", "key": key}, db=db)
    if not item:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if item["status"] != "live" and "admin" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    database(
        log_template(
            user["key"],
            "viewed",
            item["key"],
            "item"
        ))

    return jsonify({
        "status": 200,
        "item": item_schema(item, db),
    })


@bp.get("/shop")
def shop(
    db=None,
    status="live",
    search="",
    tag="",
    sort="latest",
    page_no=1,
    size=12  # 24
):
    if not db:
        db = database()
    user = token_to_user(db)

    if "status" in request.args and user and "admin" in user["roles"]:
        status = request.args["status"]
    if "search" in request.args:
        search = request.args["search"]
    if "tag" in request.args:
        tag = request.args["tag"]
    if "sort" in request.args:
        sort = request.args["sort"]
    if "page_no" in request.args:
        page_no = int(request.args["page_no"])
    if "size" in request.args:
        size = int(request.args["size"])

    multiply = False
    if tag[-2:] == ":x":
        multiply = True
        tag = tag[:-2]
    tags = tag.split(",")
    tags = [] if not tags[0] else tags

    items = []
    for x in db:
        if x["type"] != "item":
            continue
        if status and x["status"] != status:
            continue
        if search and not re.search(search, x["name"], re.IGNORECASE):
            continue
        if tag:
            if multiply:
                if not all(y in x["tags"] for y in tags):
                    continue
            elif not any(y in tags for y in x["tags"]):
                continue

        items.append(x)

    reverse = sort in ["latest", "name (z-a)", "expensive", "discount",
                       "rating"]

    fit = []
    if sort in ["latest", "oldest"]:
        sort = "date_c"
    elif sort in ["name (a-z)", "name (z-a)"]:
        sort = "name"
    elif sort in ["cheap", "expensive"]:
        sort = "price"
    elif sort == "discount":
        for x in items:
            x["discount"] = 0
            if x["old_price"]:
                x["discount"] = (
                    x["old_price"] - x["price"]) * 100 / x["old_price"]
                fit.append(x)
        items = fit
    elif sort == "rating":
        for x in items:
            x["rating"] = 0
            count = 0
            for y in db:
                if y["type"] == "feedback" and y["item"] == x["key"]:
                    x["rating"] += y["rating"]
                    count += 1
            if x["rating"] > 0 and count > 0:
                x["rating"] = x["rating"]/count
                fit.append(x)
        items = fit

    items = sorted(items, key=lambda d: d[sort].lower() if isinstance(
        d[sort], str) else d[sort], reverse=reverse)

    total_page = ceil(len(items) / size)
    start = (page_no - 1) * size
    stop = start + size
    items = items[start: stop]

    return jsonify({
        "status": 200,
        "items": [item_schema(item, db) for item in items],
        "total_page": total_page
    })


@bp.get("/recently_viewed/<user_key>/<item_key>")
def recently_viewed(user_key, item_key):
    db = database()

    logs = query({
        "type": "log",
        "user": user_key,
        "action": "viewed",
        "entity_type": "item"
    }, many=True, db=db)

    logs = sorted(logs, key=lambda d: d["date"], reverse=True)

    items = []
    unique_keys = []
    for x in logs:
        item = query({"type": "item", "key": x["entity"]}, db=db)
        if (
            item
            and item["key"] not in unique_keys
            and item["key"] != item_key
            and item["status"] == "live"
        ):
            items.append(item_schema(item, db))
            unique_keys.append(item["key"])

        if len(items) >= 8:
            break

    return jsonify({
        "status": 200,
        "items": items
        # "You may also like",
    })


@bp.get("/similar_items/<key>")
def similar_items(key):
    db = database()

    item = query({"type": "item", "slug": key}, db=db)
    if not item:
        item = query({"type": "item", "key": key}, db=db)
    if not item:
        return jsonify({
            "status": 200,
            "items": []
        })

    def get_keywords(x):
        tags = [*x["tags"], *re.split(r'\s+', x["name"].lower())]
        return list(set(tags))

    item_keywords = get_keywords(item)

    items = []
    for x in db:
        if x["type"] == "item" and x["key"] != item["key"]:
            x_keywords = get_keywords(x)
            x_keywords = [x for x in x_keywords if x in item_keywords]

            items.append({
                "item": x,
                "count": len(x_keywords)
            })

    items = sorted(items, key=lambda d: d["count"], reverse=True)

    return jsonify({
        "status": 200,
        "items": [item_schema(x["item"], db) for x in items[:8]]
    })


@bp.get("/customer_view/<user_key>/<item_key>")
def customer_view(user_key, item_key):
    db = database()

    logs = []
    for x in db:
        if (
            x["type"] == "log"
            and x["user"] != user_key
            and x["action"] == "viewed"
            and x["entity_type"] == "item"
        ):
            logs.append(x)

    logs = sorted(logs, key=lambda d: d["date"], reverse=True)

    next_viewed_keys = []
    while logs != []:
        first_user_logs = []
        other_users_logs = []

        for x in logs:
            if x["user"] == logs[0]["user"]:
                first_user_logs.append(x)
            else:
                other_users_logs.append(x)
        logs = other_users_logs

        prev_item_key = None
        for x in first_user_logs:
            if (
                prev_item_key
                and prev_item_key == item_key
                and x["entity"] != item_key
            ):
                next_viewed_keys.append(x["entity"])
            prev_item_key = x["entity"]

    items = []
    unique_keys = []
    for x in next_viewed_keys:
        if x not in unique_keys:
            unique_keys.append(x)
            items.append({
                "item":  query({"type": "item", "key": x}, db=db),
                "count":  next_viewed_keys.count(x)
            })

    items = sorted(items, key=lambda d: d["count"], reverse=True)

    return jsonify({
        "status": 200,
        "items": [item_schema(x["item"], db) for x in items[:8]]
    })
