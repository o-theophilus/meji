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
            "error": "unauthorised access"
        })

    database(
        log_template(
            user["key"],
            "view_item",
            item["key"],
            "item"
        ))

    user_views = query({
        "type": "log",
        "user": user["key"],
        "action": "view_item"
    }, many=True, db=db)

    user_views = sorted(user_views, key=lambda d: d["date"], reverse=True)

    recently = []
    picked = []
    for row in user_views:
        _item = query({"type": "item", "key": row["entity"]}, db=db)
        if (
            _item
            and _item["key"] not in picked
            and _item["key"] != item["key"]
            and _item["status"] == "live"
        ):
            recently.append(item_schema(_item, db))
            picked.append(_item["key"])

        if len(recently) >= 6:
            break

    return jsonify({
        "status": 200,
        "item": item_schema(item, db),
        "recently_viewed": recently
        # "Similar Items",
        # "Customers who viewed this also viewed",
        # "You may also like",
    })


def item_master(
    db=[],
    status="live",
    search="",
    tag="",
    sort="latest",
    page_no=1,
    size=24,
):

    items = []
    for x in db:
        if x["type"] != "item":
            continue
        if status and x["status"] != status:
            continue
        if search and not re.search(search, x["name"], re.IGNORECASE):
            continue
        if tag:
            _tag, logic = tag.split("$:")
            _tag = _tag.split(",")

            if logic == "true":
                if not all(y in x["tags"] for y in _tag):
                    continue
            elif not any(y in _tag for y in x["tags"]):
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

    return {
        "items": [item_schema(item, db) for item in items],
        "total_page": total_page
    }


@ bp.get("/home")
def home():
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

    group = [
        {
            "name": "New Arrivals",
            "sort": "latest"
        },
        {
            "name": "Offers",
            "sort": "discount"
        }
    ]

    return jsonify({
        "status": 200,
        "ads": ads,
        "tags": all_tags(db).json["tags"],
        "group": [
            {
                "name": x["name"],
                "sort": x["sort"],
                "items": item_master(
                    size=6,
                    sort=x["sort"],
                    db=db
                )["items"]
            } for x in group

        ]
    })


@bp.get("/shop")
def shop():
    db = database()
    user = token_to_user(db)

    return jsonify({
        "status": 200,
        "tags": all_tags(db).json["tags"],
        **item_master(
            db=db,
            status=request.args["status"] if (
                "status" in request.args
                and request.args["status"]
                and user
                and "admin" in user["roles"]
            ) else "live",
            search=request.args[
                "search"] if "search" in request.args else "",
            tag=request.args[
                "tag"] if "tag" in request.args else "",
            sort=request.args[
                "sort"] if "sort" in request.args else "latest",
            page_no=int(request.args[
                "page_no"]) if "page_no" in request.args else 1,
        )
    })
