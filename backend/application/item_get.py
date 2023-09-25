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
    for row in db:
        if (
            row["type"] == "item"
            and row["status"] == "live"
        ):
            tags += row["tags"]

    freq = {}
    for x in tags:
        if x in freq:
            freq[x] += 1
        else:
            freq[x] = 1

    freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    tags = [x for x, _ in freq]

    return jsonify({
        "status": 200,
        "tags": tags
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
def shop():
    db = database()
    user = token_to_user(db)

    status = request.args["status"] if (
        "status" in request.args and user and "admin" in user["roles"]
    ) else "live"
    search = request.args["search"] if "search" in request.args else ""
    tag = request.args["tag"] if "tag" in request.args else ""
    sort = request.args["sort"] if "sort" in request.args else "latest"
    page_no = int(request.args["page_no"]) if "page_no" in request.args else 1
    size = int(request.args["size"]) if "size" in request.args else 24

    multiply = False
    if tag[-2:] == ":x":
        multiply = True
        tag = tag[:-2]

    items = []
    for x in db:
        if x["type"] != "item":
            continue
        if status and x["status"] != status:
            continue
        if search and not re.search(search, x["name"], re.IGNORECASE):
            continue
        if tag:
            tags = tag.split(",")
            if multiply:
                if not all(y in x["tags"] for y in tags):
                    continue
            elif not any(y in tags for y in x["tags"]):
                continue

        items.append(x)

    reverse = sort in ["latest", "name (z-a)", "expensive", "discount"]

    if sort in ["latest", "oldest"]:
        sort = "date_c"
    elif sort in ["name (a-z)", "name (z-a)"]:
        sort = "name"
    elif sort in ["cheap", "expensive"]:
        sort = "price"
    elif sort == "discount":
        temp = []
        for item in items:
            item["discount"] = 0
            if item["old_price"]:
                item["discount"] = (
                    item["old_price"] - item["price"]
                ) * 100 / item["old_price"]
                temp.append(item)
        items = temp

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


@ bp.get("/ads")
def ads():
    db = database()

    ads = []
    for x in db:
        if (
            x["type"] == "item"
            and "ads" in x
            and x["ads"] != {}
            and "home" in x["ads"]["placement"]
        ):
            ads.append({
                "name": x["name"],
                "slug": x["slug"],
                "ads": {
                    f'{"xxx"}/{x["ads"]["300x300"]}',
                    f'{"xxx"}/{x["ads"]["300x600"]}',
                    f'{"xxx"}/{x["ads"]["600x300"]}',
                    f'{"xxx"}/{x["ads"]["900x300"]}'
                }
            })

    return jsonify({
        "status": 200,
        "ads": ads,
    })


@bp.get("/recently_viewed/<user>/<item>")
def recently_viewed(user, item):
    db = database()

    user_views = query({
        "type": "log",
        "user": user,
        "action": "view"
    }, many=True, db=db)

    user_views = sorted(user_views, key=lambda d: d["date"], reverse=True)

    items = []
    picked = []
    for x in user_views:
        _item = query({"type": "item", "key": x["entity"]}, db=db)
        if (
            _item
            and _item["key"] not in picked
            and _item["key"] != item
            and _item["status"] == "live"
        ):
            items.append(item_schema(_item, db))
            picked.append(_item["key"])

        if len(items) >= 6:
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

    def get_kw(x):
        tags = [*x["tags"], *re.split(r'\s+', x["name"].lower())]
        return list(set(tags))

    item_kw = get_kw(item)

    items = []
    for x in db:
        if x["type"] == "item" and x["key"] != item["key"]:
            x_kw = get_kw(x)
            x_kw = [x for x in x_kw if x in item_kw]

            items.append({
                "item": x,
                "count": len(x_kw)
            })

    items = sorted(items, key=lambda d: d["count"], reverse=True)

    return jsonify({
        "status": 200,
        "items": [item_schema(x["item"], db) for x in items[:6]]
    })


@bp.get("/customer_view/<user>/<item>")
def customer_view(user, item):
    db = database()

    logs = []
    for x in db:
        if (
            x["type"] == "log"
            and x["user"] != user
            and x["action"] == "view_item"
        ):
            logs.append(x)

    logs = sorted(logs, key=lambda d: d["date"], reverse=True)

    next_items = []
    while logs != []:
        temp_logs = []
        user_logs = []

        for x in logs:
            if x["user"] == logs[0]["user"]:
                user_logs.append(x)
            else:
                temp_logs.append(x)
        logs = temp_logs

        prev_log = None
        for x in user_logs:
            if prev_log and prev_log == item and x["entity"] != item:
                next_items.append(x["entity"])
            prev_log = x["entity"]

    items = []
    unique = []
    for x in next_items:
        if x not in unique:
            unique.append(x)
            items.append({
                "item":  query({"type": "item", "key": x}, db=db),
                "count":  next_items.count(x)
            })

    items = sorted(items, key=lambda d: d["count"], reverse=True)

    return jsonify({
        "status": 200,
        "items": [item_schema(x["item"], db) for x in items[:6]]
    })
