from flask import Blueprint, jsonify, request
from math import ceil
from ..tools import get_session
from ..postgres import db_close, db_open

bp = Blueprint("report_get", __name__)


@bp.get("/reports")
def get_many():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "report:view" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    searchParams = {
        "search": "",
        "type": "",
        "order": "latest",
        "page_no": 1,
        "page_size": 24
    }
    search = request.args.get("search", searchParams["search"]).strip()
    _type = request.args.get("status", searchParams["status"]).strip()
    order = request.args.get("order", searchParams["order"]).strip()
    page_no = int(request.args.get("page_no", searchParams["page_no"]))
    page_size = int(request.args.get("page_size", searchParams["page_size"]))

    order_by = {
        'latest': 'date_created',
        'oldest': 'date_created'
    }
    order_dir = {
        'latest': 'DESC',
        'oldest': 'ASC'
    }

    cur.execute(f"""
        SELECT
            report.key,
            report.date_created,
            report.comment,
            report.tags,
            report.entity_type,
            report.entity_key,

            jsonb_build_object(
                'name', "user".name,
                'username', "user".username,
                'photo', "user".photo
            ) AS reporter,

            jsonb_build_object(
                'name', COALESCE(user_1.name, user_2.name),
                'username', COALESCE(user_1.username, user_2.username),
                'photo', COALESCE(user_1.photo, user_2.photo)
            ) AS "user",

            jsonb_build_object(
                'date_created', review.date_created,
                'comment', review.comment,
                'item_key', review.item_key
            ) AS user_comment,

            COUNT(*) OVER() AS _count

        FROM report
        LEFT JOIN "user" ON report.user_key = "user".key
        LEFT JOIN "user" user_1 ON report.entity_key = user_1.key
            AND report.entity_type = 'user'

        LEFT JOIN review ON report.entity_key = review.key
            AND report.entity_type = 'comment'
        LEFT JOIN "user" user_2 ON review.user_key = user_2.key
            AND report.entity_type = 'comment'

        WHERE
            (%s = '' OR CONCAT_WS(', ',
                report.key, report.comment, report.tags, report.entity_key,
                "user".key, "user".name, "user".username, "user".email
            ) ILIKE %s)
            AND (%s = '' OR report.entity_type = %s)
        ORDER BY {order_by[order]} {order_dir[order]}
        LIMIT %s OFFSET %s;
    """, (
        search, f"%{search}%",
        _type, _type,
        page_size, (page_no - 1) * page_size
    ))
    items = cur.fetchall()

    for x in items:
        x["reporter"]["photo"] = (
            f"{request.host_url}file/{x['reporter']['photo']}"
            if x["reporter"]["photo"] else None
        )
        x["user"]["photo"] = (
            f"{request.host_url}file/{x['user']['photo']}"
            if x["user"]["photo"] else None
        )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "items": items,
        "order_by": list(order_by.keys()),
        "_type": ["user", "comment"],
        "_status": ["unresolved", "resolved"],
        "total_page": ceil(items[0]["_count"] / page_size
                           ) if items else 0
    })
