from math import ceil

from flask import Blueprint, request

from ...tools import session

bp = Blueprint("advert_get", __name__)


sizes = ["300x300", "300x600", "600x300", "900x300"]
spaces = ['home_1', 'home_2', 'home_3', 'shop', 'save']


def advert_schema(advert):
    for key, val in advert["photo"].items():
        advert["photo"][key] = f"{request.host_url}photo/item_advert/{val}"
    return advert


@bp.get("/items/<key>/advert")
@session(True)
def get(cur, user, key):
    if "item.advert" not in user["access"]:
        return {
            "status": 403,
            "error": "unauthorized access"
        }, 403

    cur.execute("""SELECT * FROM advert WHERE key = %s;""", (key,))
    advert = cur.fetchone()

    return {
        "status": 200,
        "advert": advert_schema(advert) if advert else None,
        "spaces": spaces,
        "sizes": sizes
    }, 200


@bp.get("/adverts")
@bp.get("/advert_display")
@session(False)
def many(cur, user):
    order_by = {
        'name (a-z)': 'item.name',
        'name (z-a)': 'item.name'
    }

    order_dir = {
        'name (a-z)': 'ASC',
        'name (z-a)': 'DESC'
    }

    searchParams = {
        "search": "",
        "space": "all",
        "order": "name (a-z)",
        "page_no": 1,
        "page_size": 24
    }
    search = request.args.get("search", searchParams["search"]).strip()
    space = request.args.get("space", searchParams["space"])
    order = request.args.get("order", searchParams["order"])
    page_no = int(request.args.get("page_no", searchParams["page_no"]))
    page_size = int(request.args.get("page_size", searchParams["page_size"]))
    page_size = min(page_size, 100)

    status = "active"
    if request.path == "/advert" and "item.advert" in user["access"]:
        status = ""

    cur.execute(f"""
        SELECT
            advert.*, item.name, item.slug, item.status,
            COUNT(*) OVER() AS total_items
        FROM advert
        LEFT JOIN item ON advert.key = item.key
        WHERE
            (%s = 'all' OR %s = ANY(advert.space))
            AND (%s = '' OR item.name ILIKE %s)
            AND (%s = '' OR item.status = %s)
        ORDER BY {order_by[order]} {order_dir[order]}, advert.key DESC
        LIMIT %s OFFSET %s;
    """, (
        space, space,
        search, f"%{search}%",
        status, status,
        page_size, (page_no - 1) * page_size
    ))
    adverts = cur.fetchall()

    return {
        "status": 200,
        "adverts": [advert_schema(x) for x in adverts],
        "order_by": list(order_by.keys()),
        "spaces": ["all", *spaces],
        "sizes": sizes,
        "searchParams": searchParams,
        "total_page": ceil(adverts[0][
            "total_items"] / page_size) if adverts else 0
    }, 200
