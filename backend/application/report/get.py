from math import ceil

from flask import Blueprint, jsonify, request

from ..postgres import db_close, db_open
from ..tools import get_session

bp = Blueprint("report_get", __name__)


@bp.get("/reports")
def get_many(cur=None):
    close_conn = not cur
    if not cur:
        con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        if close_conn:
            db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "report.view" not in user["access"]:
        if close_conn:
            db_close(con, cur)
        return jsonify({
            "status": 403,
            "error": "unauthorized access"
        })

    order_by = {
        'latest': 'report.date_created',
        'oldest': 'report.date_created'
    }

    order_dir = {
        'latest': 'DESC',
        'oldest': 'ASC'
    }

    searchParams = {
        "search": "",
        "status": "active",
        "type": "all",
        "order": "latest",
        "page_no": 1,
        "page_size": 24
    }
    search = request.args.get("search", searchParams["search"]).strip()
    _type = request.args.get("type", searchParams["type"])
    status = request.args.get("status", searchParams["status"])
    order = request.args.get("order", searchParams["order"])
    page_no = int(request.args.get("page_no", searchParams["page_no"]))
    page_size = int(request.args.get("page_size", searchParams["page_size"]))
    page_size = min(page_size, 100)

    cur.execute(f"""
        SELECT
            report.key,
            report.status,
            report.resolver_key,
            report.entity_key,
            report.entity_type,

            jsonb_build_object(
                'date_created', report.date_created,
                'comment', report.reporter_comment,
                'tags', report.tags,
                'user', jsonb_build_object(
                    'name', reporter.name,
                    'username', reporter.username,
                    'photo', reporter.photo
                )
            ) AS reporter,

            jsonb_build_object(
                'date_created', report.date_resolved,
                'comment', report.resolver_comment,
                'user', jsonb_build_object(
                    'name', resolver.name,
                    'username', resolver.username,
                    'photo', resolver.photo
                )
            ) AS resolver,

            jsonb_build_object(
                'user', jsonb_build_object(
                    'name', ru.name,
                    'username', ru.username,
                    'photo', ru.photo,
                    'blocked', block.user_key IS NOT NULL
                )
            ) AS reported_user,

            jsonb_build_object(
                'date_created', rr.date_created,
                'comment', rr.comment,
                'user', jsonb_build_object(
                    'name', rr_user.name,
                    'username', rr_user.username,
                    'photo', rr_user.photo
                )
            ) AS reported_review

        FROM report
        LEFT JOIN "user" reporter ON report.reporter_key = reporter.key
        LEFT JOIN "user" resolver ON report.resolver_key = resolver.key
        LEFT JOIN "user" ru ON report.entity_key = ru.key
            AND report.entity_type = 'user'
        LEFT JOIN block ON ru.key = block.user_key
        LEFT JOIN review rr ON report.entity_key = rr.key
            AND report.entity_type = 'review'
        LEFT JOIN "user" rr_user ON rr.user_key = rr_user.key

        WHERE
            report.status = %s
            AND (
                %s = 'all' OR report.entity_type = %s
            )
            AND (%s = '' OR CONCAT_WS(', ',
                report.key, report.reporter_comment, report.tags::text,
                report.reporter_key, report.entity_key
            ) ILIKE %s)
        ORDER BY {order_by[order]} {order_dir[order]}, report.key DESC
        LIMIT %s OFFSET %s;
    """, (
        status,
        _type, _type,
        search, f"%{search}%",
        page_size, (page_no - 1) * page_size
    ))
    reports = cur.fetchall()

    url = f"{request.host_url}photo/user/"
    for x in reports:
        if x["reporter"]["user"]["photo"]:
            x["reporter"]["user"]["photo"] = f"{url}{x[
                'reporter']['user']['photo']}"

        if x["resolver_key"]:
            if x["resolver"]["user"]["photo"]:
                x["resolver"]["user"]["photo"] = f"{url}{x[
                    'resolver']['user']['photo']}"
        else:
            del x["resolver_key"]
            del x["resolver"]

        if x["entity_type"] == "user":
            if x["reported_user"]["user"]["photo"]:
                x["reported_user"]["user"]["photo"] = f"{url}{x[
                    'reported_user']['user']['photo']}"
        else:
            del x["reported_user"]

        if x["entity_type"] == "review":
            if x["reported_review"]["user"]["photo"]:
                x["reported_review"]["user"]["photo"] = f"{url}{x[
                    'reported_review']['user']['photo']}"
        else:
            del x["reported_review"]

    cur.execute("""
        SELECT COUNT(*) FROM report
        WHERE
            report.status = %s
            AND (
                %s = 'all' OR report.entity_type = %s
            )
            AND (%s = '' OR CONCAT_WS(', ',
                report.key, report.reporter_comment, report.tags::text,
                report.reporter_key, report.entity_key
            ) ILIKE %s);
    """, (
        status,
        _type, _type,
        search, f"%{search}%",
    ))
    total_page = cur.fetchone()["count"]

    if close_conn:
        db_close(con, cur)
    return jsonify({
        "status": 200,
        "reports": reports,
        "order_by": list(order_by.keys()),
        "_status": ["active", "resolved", "dismissed"],
        "type": ["all", "user", "review"],
        "total_page": ceil(total_page / page_size),
        "searchParams": searchParams
    })
