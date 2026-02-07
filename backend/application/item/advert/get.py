from flask import Blueprint, jsonify, request
from math import ceil
from ...tools import get_session
from ...postgres import db_open, db_close

bp = Blueprint("advert_get", __name__)


sizes = ["300x300", "300x600", "600x300", "900x300"]
spaces = ['home_1', 'home_2', 'home_3', 'shop', 'save']


def advert_schema(advert):
    for key, val in advert["photo"].items():
        advert["photo"][key] = f"{request.host_url}photo/item_advert/{val}"
    return advert


@bp.get("/advert/<key>")
def get(key):
    con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "item:advert" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute("""SELECT * FROM advert WHERE key = %s;""", (key,))
    advert = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "advert": advert_schema(advert) if advert else advert,
        "spaces": spaces,
        "sizes": sizes
    })


@bp.get("/adverts")
@bp.get("/advert_display")
def get_many(cur=None):
    close_conn = not cur
    if not cur:
        con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        if close_conn:
            db_close(con, cur)
        return jsonify(session)
    user = session["user"]

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

    order_by = {
        'name (a-z)': 'item.name',
        'name (z-a)': 'item.name'
    }

    order_dir = {
        'name (a-z)': 'ASC',
        'name (z-a)': 'DESC'
    }

    status = "active"
    if request.path == "/advert" and "item:advert" in user["access"]:
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
        ORDER BY advert.key, {order_by[order]} {order_dir[order]}
        LIMIT %s OFFSET %s;
    """, (
        space, space,
        search, f"%{search}%",
        status, status,
        page_size, (page_no - 1) * page_size
    ))
    adverts = cur.fetchall()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "adverts": [advert_schema(x) for x in adverts],
        "order_by": list(order_by.keys()),
        "spaces": ["all", *spaces],
        "sizes": sizes,
        "searchParams": searchParams,
        "total_page": ceil(adverts[0][
            "total_items"] / page_size) if adverts else 0
    })
