from math import ceil

from flask import Blueprint, request

from ..tools import session

bp = Blueprint("log_get", __name__)


def search_query(cur):
    cur.execute("""
        SELECT DISTINCT ON (entity_type, action) entity_type, action
        FROM log;
    """)

    actions = {"all": ["all"]}
    for x in cur.fetchall():
        if x["entity_type"] in actions:
            actions[x["entity_type"]].append(x["action"])
        else:
            actions[x["entity_type"]] = ["all", x["action"]]

    return actions


@bp.get("/logs")
@session(True)
def many(cur, user):
    searchParams = {
        "u_search": "",
        "entity_type": "all",
        "action": "all",
        "e_search": "",
        "page_no": 1,
        "page_size": 24
    }
    u_search = request.args.get("u_search", searchParams["u_search"]).strip()
    entity_type = request.args.get("entity_type", searchParams["entity_type"])
    action = request.args.get("action", searchParams["action"])
    e_search = request.args.get("e_search", searchParams["e_search"]).strip()
    page_no = int(request.args.get("page_no", searchParams["page_no"]))
    page_size = int(request.args.get("page_size", searchParams["page_size"]))
    page_size = min(page_size, 100)

    if "log.view" not in user["access"]:
        return {
            "status": 403,
            "error": "unauthorized access"
        }, 403

    if "log.view_others" not in user["access"]:
        u_search = user["key"]

    cur.execute("""
        SELECT
            log.key,
            log.date_created,
            log.status,
            log.misc,
            log.action,
            log.user_key,
            log.entity_key,

            jsonb_build_object(
                'key', "user".key,
                'username', "user".username,
                'name', "user".name
            ) AS user,

            jsonb_build_object(
                'slug', COALESCE(usr.username, item.slug, blog.slug,
                    log.entity_key),
                'type', log.entity_type,
                'name', COALESCE(usr.name, item.name, blog.title,
                    log.entity_key)
            ) AS entity,

            COUNT(*) OVER() AS _count

        FROM log
        LEFT JOIN "user" ON log.user_key = "user".key
        LEFT JOIN "user" usr ON log.entity_key = usr.key::TEXT
            AND log.entity_type = 'user'
        LEFT JOIN
            item ON log.entity_key = item.key::TEXT
            AND log.entity_type = 'item'
        LEFT JOIN
            blog ON log.entity_key = blog.key::TEXT
            AND log.entity_type = 'blog'

        WHERE
            (%s = '' OR CONCAT_WS(
                ', ', log.user_key, "user".name, "user".email
            ) ILIKE %s)
            AND (%s = 'all' OR log.entity_type = %s)
            AND (%s = 'all' OR log.action = %s)
            AND (%s = '' OR CONCAT_WS(', ',
                log.entity_key,
                usr.name, usr.username, usr.email,
                item.name, item.slug,
                blog.title, blog.slug
            ) ILIKE %s)
        ORDER BY log.date_created DESC
        LIMIT %s OFFSET %s;
    """, (
        u_search, f"%{u_search}%",
        entity_type, entity_type,
        action, action,
        e_search, f"%{e_search}%",
        page_size, (page_no - 1) * page_size
    ))
    logs = cur.fetchall()

    for x in logs:
        misc = {}
        for key,  val in x["misc"].items():
            misc[key] = str(val)
        x["misc"] = misc

        if x["action"] in ["changed theme", "logged in", "logged out"]:
            del x["entity"]
        elif x["action"] == "viewed user" and x["user_key"] == x["entity_key"]:
            x["action"] = "viewed profile"
            del x["entity"]
        elif x["entity"]["type"] == "page":
            x["action"] = "viewed page"

    return {
        "status": 200,
        "logs": logs,
        "searchParams": searchParams,
        "search_query": search_query(cur),
        "total_page": ceil(logs[0]["_count"] / page_size) if logs else 0
    }, 200
