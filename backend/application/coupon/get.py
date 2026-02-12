from math import ceil

from flask import Blueprint, jsonify, request

from ..postgres import db_close, db_open
from ..tools import get_session

bp = Blueprint("coupon_get", __name__)


for_list = ['order', 'delivery']
value_unit_list = ['flat', 'percent']
threshold_unit_list = ['order']


def coupon_schema(x, access):
    x["note"] = ""

    if x["benefit"]["value_unit"] == 'percent':
        x["note"] += f'<span class="bold">{x["benefit"]["value"]}%</span>'
    elif x["benefit"]["value_unit"] == 'flat':
        x["note"] += f'<span class="bold">₦{x[
            "benefit"]["value"]:,}</span>'

    x["note"] += " discount on"

    if x["benefit"]["for"] == 'delivery':
        x["note"] += f' <span class="bold">{x[
            "benefit"]["for"]} fee</span>'
    elif x["benefit"]["for"] == 'order':
        x["note"] += f' <span class="bold">{x[
            "benefit"]["for"]}</span>'

    x["note"] = f'<span class="line_1">{x["note"]}</span>'

    if x["benefit"]["threshold"] > 0:
        x["note"] += f'<br/> for {x["benefit"]["threshold_unit"]} above ₦{x[
            "benefit"]["threshold"]:,}'

    if "coupon:view_code" not in access:
        x["code"] = "**********"

    return x


@bp.get("/coupon/<key>")
def get(key):
    con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute("""SELECT * FROM coupon WHERE key = %s""", (key,))
    coupon = cur.fetchone()
    if not coupon:
        db_close(con, cur)
        return jsonify({
            "status": 404,
            "error": "Oops! The item you're looking for doesn't exist"
        })

    if "coupon:view" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "coupon": coupon_schema(coupon, user["access"])
    })


@bp.get("/coupons")
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

    if "coupon:view" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    searchParams = {
        "search": "",
        "status": "created",
        "order": "latest",
        "page_no": 1,
        "page_size": 24
    }
    search = request.args.get("search", searchParams["search"]).strip()
    status = request.args.get("status", searchParams["status"])
    order = request.args.get("order", searchParams["order"])
    page_no = int(request.args.get("page_no", searchParams["page_no"]))
    page_size = int(request.args.get("page_size", searchParams["page_size"]))

    # TODO:
    order_by = {
        'latest': 'date_created',
        'oldest': 'date_created',
        'cheap': 'value',
        'costly': 'value',
    }
    order_dir = {
        'latest': 'DESC',
        'oldest': 'ASC',
        'cheap': 'ASC',
        'costly': 'DESC',
    }

    cur.execute(f"""
        SELECT * FROM coupon
        WHERE status = %s AND (%s = '' OR key::TEXT ILIKE %s)
        ORDER BY {order_by[order]} {order_dir[order]}
        LIMIT %s OFFSET %s;
    """, (status, search, f"%{search}%", page_size, (page_no - 1) * page_size))
    coupons = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM coupon")
    total_page = cur.fetchone()["count"]

    if close_conn:
        db_close(con, cur)
    return jsonify({
        "status": 200,
        "coupons": [coupon_schema(x, user["access"]) for x in coupons],
        "total_page": ceil(total_page / page_size),
        "order_by": list(order_by.keys()),
        "for": for_list,
        "value_unit": value_unit_list,
        "threshold_unit": threshold_unit_list,
        "searchParams": searchParams,
        "_status": ['created', 'used', 'expired']
    })
