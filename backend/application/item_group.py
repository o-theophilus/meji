from flask import Blueprint, jsonify
from .schema import item_schema
from .database import database, query
import re

bp = Blueprint("item_group", __name__)


@bp.get("/recently_viewed/<user>/<item>")
def recently_viewed(user, item):
    db = database()

    user_views = query({
        "type": "log",
        "user": user,
        "action": "view_item"
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
