from flask import Blueprint, jsonify, request
from .tools import token_to_user
from .schema import item_schema, log_template
from math import ceil
from .database import database, query
from .tag import all_tags
import re

bp = Blueprint("item_get", __name__)


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
    # make sure item is live

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
    order=["date", "dsc"],
    page_no=1,
    size=24,
):

    print(status)
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

    if order[0] == "date":
        order[0] = "date_c"
    elif order[0] == "discount":
        for item in items:
            item["discount"] = 0
            if item["old_price"]:
                item["discount"] = (item["old_price"] -
                                    item["price"]) * 100 / item["old_price"]

    items = sorted(
        items, key=lambda d: d[order[0]], reverse=order[1] == "dsc")

    total_page = ceil(len(items) / size)

    start = (page_no - 1) * size
    stop = start + size
    items = items[start: stop]

    return jsonify({
        "status": 200,
        "items": [item_schema(item, db) for item in items],
        "total_page": total_page
    })


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
    for row in db:
        if "ads" in row:
            if (
                row["type"] == "item"
                and row["ads"] != {}
                and "home" in row["ads"]["placement"]
            ):
                ads.append({
                    "name": row["name"],
                    "slug": row["slug"],
                    "ads": {
                        f'{"xxx"}/{row["ads"]["300x300"]}',
                        f'{"xxx"}/{row["ads"]["300x600"]}',
                        f'{"xxx"}/{row["ads"]["600x300"]}',
                        f'{"xxx"}/{row["ads"]["900x300"]}'
                    }
                })

    return jsonify({
        "status": 200,
        "ads": ads,
        "tags": all_tags(db).json["tags"],
        "group": [
            #     "name": "Featured",
            #     "name": "Recommended",
            {
                "name": "New Arrivals",
                "query": {"order": ["date",  "dsc"]},
                "items": item_master(size=6, order=[
                    "date", "dsc"], db=db).json["items"]
            },
            {
                "name": "Offers",
                "query": {"order": ["discount",  "dsc"]},
                "items": item_master(size=6, order=[
                    "discount", "dsc"], db=db).json["items"]
            },
        ],
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

    out = item_master(
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
        order=request.args["order"].split(
            ',') if "order" in request.args else ["date", "dsc"],
        page_no=int(request.args[
            "page_no"]) if "page_no" in request.args else 1,
    ).json

    out["tags"] = all_tags(db).json["tags"]
    return out
