from flask import Blueprint, jsonify, request
from .tools import token_to_user
from .schema import item_schema, category_schema, log_template
from math import ceil
from .database import database, query
# from .photo import photo_url
import re

bp = Blueprint("item_get", __name__)


@bp.get("/item/<alias>")
def item(alias):
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 401,
            "error": "invalid token"
        })

    item = query({"type": "item", "alias": alias}, db=db)
    if not item:
        return jsonify({
            "status": 401,
            "error": "invalid request"
        })

    ads = {}
    if "ads" in item and item["ads"] != {}:
        ads = {
            f'{"xxx"}{item["ads"]["300x300"]}',
            f'{"xxx"}{item["ads"]["300x600"]}',
            f'{"xxx"}{item["ads"]["600x300"]}',
            f'{"xxx"}{item["ads"]["900x300"]}'
        }

    categories = query({"type": "category"}, True, db)
    categories = sorted(categories, key=lambda d: d['order'])
    categories = [x["name"] for x in categories]

    return jsonify({
        "status": 200,
        "item": item_schema(item, db),
        "categories": categories,
        "ads": ads
    })


@bp.get("/item_info/<alias>")
def item_info(alias):
    db = database()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 401,
            "error": "invalid token"
        })

    item = query({"type": "item", "alias": alias}, db=db)
    if not item:
        return jsonify({
            "status": 401,
            "error": "invalid request"
        })

# ****************************************
# ****************************************
# ****************************************

    # if item["status"] == "live":

    database(
        log_template(
            "voucher",
            user["key"],
            item["key"],
            "view_item",
            200,
        ))

# ****************************************
# ****************************************
# ****************************************

    logs = []
    # logs = get_logs("user_key", user["key"], "action", "view_item", db)
    _temp = []
    _logs = []
    for row in logs:
        if row["entity_key"] not in _temp and row["entity_key"] != item["key"]:
            _temp.append(row["entity_key"])
            _logs.append(row)

    logs = sorted(_logs, key=lambda d: d["date"], reverse=True)

    recently = []
    for row in logs:
        _item = query({"type": "item", "key": row["entity_key"]}, db=db)
        if _item and _item["status"] == "live":
            recently.append(item_schema(_item, db))

    recently = {
        "name": "Recently Viewed",
        "items": recently[:6]
    }

# ****************************************
# ****************************************
# ****************************************

    #     "name": "Similar Items",
    #     "name": "Customers who viewed this also viewed",
    #     "name": "You may also like",

    return jsonify({
        "status": 200,
        "item": item_schema(item, db),
        "group": [recently]
    })


def item_master(
    db=[],
    status="live",
    search="",
    category="",
    order=["date", "dsc"],
    page_no=1,
    size=24,
):

    if category:
        category = query({"type": "category", "name": category}, db=db)

    items = []
    for row in db:
        if (
            row["type"] == "item"
            and row["status"] == status
        ):
            if search and category:
                if (
                    re.search(search, row["name"], re.IGNORECASE)
                    and row["key"] in category["items"]
                ):
                    items.append(row)
            elif search:
                if re.search(search, row["name"], re.IGNORECASE):
                    items.append(row)
            elif category:
                if row["key"] in category["items"]:
                    items.append(row)
            else:
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
            "status": 401,
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
                    "alias": row["alias"],
                    "ads": {
                        f'{"xxx"}/{row["ads"]["300x300"]}',
                        f'{"xxx"}/{row["ads"]["300x600"]}',
                        f'{"xxx"}/{row["ads"]["600x300"]}',
                        f'{"xxx"}/{row["ads"]["900x300"]}'
                    }
                })

    categories = query({"type": "category"}, True, db)
    categories = sorted(categories, key=lambda d: d['order'])
    categories = [category_schema(x) for x in categories if x["items"] != []]

    return jsonify({
        "status": 200,
        "ads": ads,
        "categories": categories,
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
            "status": 401,
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
        category=request.args[
            "category"] if "category" in request.args else "",
        order=request.args["order"].split(
            ',') if "order" in request.args else ["date", "dsc"],
        page_no=int(request.args[
            "page_no"]) if "page_no" in request.args else 1,
    ).json

    categories = query({"type": "category"}, True, db)
    categories = sorted(categories, key=lambda d: d['order'])
    categories = [category_schema(x) for x in categories if x["items"] != []]

    out["categories"] = categories
    return out
