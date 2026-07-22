from math import ceil

from flask import Blueprint, request

from ..cart.delivery import get_areas
from ..comment.get import many_items
from ..tools import item_schema, session
from .get_group import (customer_view, recently_viewed, recommended,
                        similar_items)

bp = Blueprint("item_get", __name__)


@bp.get("/items/<key>")
@session(False)
def get(cur, user, key):
    if "v" in request.args:
        cur.execute("""
            SELECT item_version.*, item.slug AS item_slug,
                to_jsonb(item) AS latest
            FROM item_version
            LEFT JOIN item on item_version.item_key = item.key
            WHERE item_version.key::TEXT = %s;
        """, (key,))
        item = cur.fetchone()
        if item and item["item_slug"]:
            item["latest"] = item_schema(item["latest"])
            del item["item_key"]

    else:
        cur.execute("""
            SELECT * FROM item WHERE slug = %s OR key::TEXT = %s;
        """, (key, key))
        item = cur.fetchone()

    if not item:
        return {
            "error": "Oops! The item you're looking for doesn't exist"
        }, 404

    if (
        item["status"] != "active"
        and "item.add" not in user["access"]
        and "item.edit_status" not in user["access"]
    ):
        return {
            "error": "unauthorized access"
        }, 403

    return {
        "item": item_schema(item),
        "areas": get_areas()
    }, 200


def get_many(cur, user,  _order="latest", _tag="", _page_size=24):
    order_by = {
        'latest': 'item.date_created',
        'oldest': 'item.date_created',
        'name (a-z)': 'item.name',
        'name (z-a)': 'item.name',
        'cheap': 'item.price',
        'costly': 'item.price',
        'discount': 'discount',
        'rating': 'rating'
    }
    order_dir = {
        'latest': 'DESC',
        'oldest': 'ASC',
        'name (a-z)': 'ASC',
        'name (z-a)': 'DESC',
        'cheap': 'ASC',
        'costly': 'DESC',
        'discount': 'DESC',
        'rating': 'DESC',
    }

    searchParams = {
        "search": "",
        "status": "active",
        "tag": _tag,
        "order": _order,
        "page_no": 1,
        "page_size": _page_size
    }
    search = request.args.get("search", searchParams["search"]).strip()
    status = request.args.get("status", searchParams["status"])
    tag = request.args.get("tag", searchParams["tag"])
    order = request.args.get("order", searchParams["order"])
    page_no = int(request.args.get("page_no", searchParams["page_no"]))
    page_size = int(request.args.get("page_size", searchParams["page_size"]))
    page_size = min(page_size, 100)

    if (
        "item.edit_status" not in user["access"]
        or "item.add" not in user["access"]
    ):
        status = "active"

    params = [status, search, f"%{search}%"]

    op = "&&"
    tag_query = ""
    if tag[-4:] == ":all":
        op = "@>"
        tag = tag[:-4]
    tags = tag.split(",") if tag else []
    if tags != []:
        tag_query = f"AND cardinality(item.tags) > 0 AND item.tags {op} %s"
        params.append([x.lower() for x in tags])

    params.append(page_size)
    params.append((page_no - 1) * page_size)

    cur.execute(f"""
        WITH rating AS (
            SELECT
                comment.item_key AS key,
                AVG(comment.rating) as rating
            FROM comment
            WHERE comment.item_key IS NOT NULL AND comment.parent_key IS NULL
            GROUP BY comment.item_key
        )

        SELECT item.*,
            CASE
                WHEN item.price = 0 OR item.price_old = 0 THEN 0
                ELSE ((item.price_old - item.price) * 100) / item.price_old
            END AS discount,
            COALESCE(rating.rating, 0) AS rating,
            COUNT(*) OVER() AS _count
        FROM item
        LEFT JOIN rating ON item.key = rating.key
        WHERE
            item.status = %s
            AND (%s = '' OR item.name ILIKE %s) {tag_query}
        ORDER BY {order_by[order]} {order_dir[order]}, item.key DESC
        LIMIT %s OFFSET %s;
    """, params)
    items = cur.fetchall()

    return {
        "items": [item_schema(x) for x in items],
        "total_page": ceil(items[0]["_count"] / page_size) if items else 0,
        "order_by": list(order_by.keys()),
        "searchParams": searchParams,
        "status": ['active', 'draft']
    }


@bp.get("/items")
@session(False)
def get_items(cur, user):
    return get_many(cur, user), 200


@bp.get("/items/<key>/after")
@session(False)
def after_get(cur, user, key):
    cur.execute("""SELECT * FROM item WHERE key = %s;""", (key,))
    if not cur.fetchone():
        return {
            "error": "invalid request"
        }, 404

    item_group = []
    _similar_items = similar_items(cur, key)
    if _similar_items:
        item_group.append({
            "name": "Similar Items",
            "items": _similar_items,
            "style": "grid",
            "open": True
        })

    _recently_viewed = recently_viewed(cur, user["key"], key)
    if _recently_viewed:
        item_group.append({
            "name": "Recently Viewed",
            "items": _recently_viewed,
            "style": "line",
            "open": True
        })

    _customer_view = customer_view(cur, user["key"], key)
    if _customer_view:
        item_group.append({
            "name": "Customers who viewed this also viewed",
            "items": _customer_view,
            "style": "line",
            "open": True
        })

    _recommended = recommended(cur, user["key"], key)
    if _recommended:
        item_group.append({
            "name": "You may also like",
            "items": _recommended,
            "style": "line",
            "open": True
        })

    return {
        "comments": many_items(cur, key, user["key"], 3),
        "item_group": item_group
    }, 200


@bp.get("/items/home")
@session(False)
def home_page(cur, user,):
    return {
        "new_arrivals": get_many(cur, user, "latest", _page_size=8)['items'],
        "discount": get_many(cur, user, "discount", _page_size=8)['items'],
        "tag": get_many(
            cur, user, "latest", _tag="hot pick 🔥", _page_size=8)['items'],
    }, 200
