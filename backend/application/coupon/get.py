from math import ceil

from flask import Blueprint, request

from ..tools import session

bp = Blueprint("coupon_get", __name__)


coupon_applies_to = ['total order', 'delivery fee']
coupon_value_unit = ['flat', 'percent']
coupon_condition_unit = ['total order']


def coupon_schema(x, access=[]):
    x["valid_from"] = x["valid_from"].strftime(
        "%Y-%m-%d") if x["valid_from"] else None
    x["valid_until"] = x["valid_until"].strftime(
        "%Y-%m-%d") if x["valid_until"] else None

    if "coupon.view_code" not in access:
        x["code"] = "**********"

    discount = ""
    if x["benefit"]["value_unit"] == 'percent':
        discount = f'<span class="bold">{x["benefit"]["value"]}%</span>'
    elif x["benefit"]["value_unit"] == 'flat':
        discount = f'<span class="bold">₦{x[
            "benefit"]["value"]:,}</span>'

    applies_to = ""
    if x["benefit"]["applies_to"] in ['delivery fee', 'total order']:
        applies_to = f' <span class="bold">{x[
            "benefit"]["applies_to"]}</span>'

    condition = ""
    if x["benefit"]["condition"] > 0:
        condition = f'<br/> for {x["benefit"]["condition_unit"]} above ₦{x[
            "benefit"]["condition"]:,}'

    x["note"] = f"<span class='line_1'>{discount}"
    x["note"] += f" discount on {applies_to}</span> {condition}"

    return x


@bp.get("/coupons/<key>")
@session(True)
def get(cur, user, key):
    cur.execute("""SELECT * FROM coupon WHERE key = %s""", (key,))
    coupon = cur.fetchone()
    if not coupon:
        return {
            "status": 404,
            "error": "Oops! The item you're looking for doesn't exist"
        }, 404

    if "coupon.view" not in user["access"]:
        return {
            "status": 403,
            "error": "unauthorized access"
        }, 403

    return {
        "status": 200,
        "coupon": coupon_schema(coupon, user["access"])
    }, 200


def many(cur):
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

    searchParams = {
        "search": "",
        "status": "active",
        "order": "latest",
        "page_no": 1,
        "page_size": 24
    }
    search = request.args.get("search", searchParams["search"]).strip()
    status = request.args.get("status", searchParams["status"])
    order = request.args.get("order", searchParams["order"])
    page_no = int(request.args.get("page_no", searchParams["page_no"]))
    page_size = int(request.args.get("page_size", searchParams["page_size"]))
    page_size = min(page_size, 100)

    cur.execute(f"""
        SELECT * FROM coupon
        WHERE
            (%s = 'all' OR status = %s)
            AND (%s = '' OR key::TEXT ILIKE %s)
        ORDER BY {order_by[order]} {order_dir[order]}, key DESC
        LIMIT %s OFFSET %s;
    """, (
        status, status,
        search, f"%{search}%",
        page_size, (page_no - 1) * page_size
    ))
    coupons = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM coupon")
    total_page = cur.fetchone()["count"]

    return {
        "status": 200,
        "coupons": [coupon_schema(x) for x in coupons],
        "total_page": ceil(total_page / page_size),
        "order_by": list(order_by.keys()),
        "applies_to": coupon_applies_to,
        "value_unit": coupon_value_unit,
        "condition_unit": coupon_condition_unit,
        "searchParams": searchParams,
        "_status": ['all', 'inactive', 'active', 'used', 'expired']
    }


@bp.get("/coupons")
@session(True)
def get_many(cur, user):
    if "coupon.view" not in user["access"]:
        return {
            "status": 403,
            "error": "unauthorized access"
        }, 403
    return many(cur), 200
