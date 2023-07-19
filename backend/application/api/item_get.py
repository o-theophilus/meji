from flask import Blueprint, jsonify, request
from .tools import token_to_user
from .schema import item_schema, log_template
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


@bp.get("/item/<slug>")
def item_info(slug):
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    item = query({"type": "item", "slug": slug}, db=db)
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
    sort=["date", "dsc"],
    page_no=1,
    size=24,
):

    items = []
    for row in db:
        if row["type"] != "item":
            continue
        if status and row["status"] != status:
            continue
        if search and not re.search(search, row["name"], re.IGNORECASE):
            continue
        if tag and tag not in row["tags"]:
            continue
        items.append(row)

    if sort[0] == "date":
        sort[0] = "date_c"
    elif sort[0] == "discount":
        for item in items:
            item["discount"] = 0
            if item["old_price"]:
                item["discount"] = (
                    item["old_price"] - item["price"]
                ) * 100 / item["old_price"]

    items = sorted(
        items, key=lambda d: d[sort[0]], reverse=sort[1] == "dsc")

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

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

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
            "sort": ["date", "dsc"]
        },
        {
            "name": "Offers",
            "sort": ["discount", "dsc"]
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
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    return jsonify({
        "status": 200,
        "tags": all_tags(db).json["tags"],
        **item_master(
            db=db,
            status=request.args["status"] if (
                "status" in request.args
                and request.args["status"]
                and "admin" in user["roles"]
            ) else "live",
            search=request.args[
                "search"] if "search" in request.args else "",
            tag=request.args[
                "tag"] if "tag" in request.args else "",
            sort=request.args["sort"].split(
                ',') if "sort" in request.args else ["date", "dsc"],
            page_no=int(request.args[
                "page_no"]) if "page_no" in request.args else 1,
        )
    })
