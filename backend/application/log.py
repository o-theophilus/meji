from flask import Blueprint, jsonify, request
from .tools import token_to_user
from .schema import log_schema
from math import ceil
from .postgres import db_close, db_open

bp = Blueprint("log", __name__)


log_template = """
    INSERT INTO log (
        key, date, user_key, action, entity_key, entity_type, status, misc
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
"""


@bp.get("/logs")
def get():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    page_no = int(request.args["page_no"]) if "page_no" in request.args else 1
    page_size = int(
        request.args["page_size"]) if "page_size" in request.args else 24

    search = "all:all:all:all"
    if "search" in request.args:
        search = request.args["search"]

    search = search.split(":")
    if len(search) != 4:
        return jsonify({
            "status": 400,
            "error": "invalid search"
        })

    user_id, entity_type, user_action, entity_id = search

    if "log:view" not in user["roles"]:
        user_id = user["key"]

    search_columns = []
    if entity_type != "all":
        cur.execute("""
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables
                WHERE table_name = %s
            );
        """, (entity_type,))
        table_exists = cur.fetchone()[0]

        if table_exists:
            cur.execute("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = %s;
            """, (entity_type,))

            search_columns = [x[0] for x in cur.fetchall()
                              if x[0] in ['name', 'email']]

    cur.execute(f"""
        SELECT log.*,
            user.name AS user_name,
            {
                f"{entity_type}.name AS entity_name,"
                if "name" in search_columns else
                f"entity_key.key AS entity_name,"
                if search_columns != [] else ""
            }
            COUNT(*) OVER() AS total_items
        FROM (
            SELECT *
            FROM log
            LEFT JOIN "user" ON log.user_key = user.key
            {
                f'''
                LEFT JOIN '{entity_type}' ON log.entity_key = {entity_type}.key
                '''
                if search_columns != [] else ""
            }
            WHERE
                (%s = 'all' OR CONCAT_WS(', ',
                    log.key, user.name, user.email) ILIKE %s)
                AND (%s = 'all' OR log.entity_type = %s)
                AND (%s = 'all' OR log.action = %s)
            {
                f'''
                AND (
                    {entity_id} = 'all' OR CONCAT_WS(', ',
                    log.key, {', '.join([f"{entity_type}.{x}"
                    for x in search_columns])}) ILIKE %{entity_id}%)
                )
                '''
                if search_columns != [] else ""
            }
        ) AS subquery
        ORDER BY date DESC
        LIMIT %s OFFSET %s;
    """, (
        user_id, f"%{user_id}%",
        entity_type, entity_type,
        user_action, user_action,

        page_size,
        (page_no - 1) * page_size
    ))

    logs = cur.fetchall()

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "logs": [log_schema(x) for x in logs],
        "total_page": ceil(logs[0][-1] / page_size) if logs else 0
    })
