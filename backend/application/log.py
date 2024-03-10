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

    user_keys = []
    if user_id != "all":

        cur.execute("""
            SELECT key
            FROM "user"
            WHERE key ILIKE %s OR name ILIKE %s OR email ILIKE %s;
        """, (
            f"%{user_id}%",
            f"%{user_id}%",
            f"%{user_id}%"
        ))
        user_keys = [x['key'] for x in cur.fetchall()]

    entity_keys = []
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
            table_columns = [x[0] for x in cur.fetchall()]

            search_columns = set(['key', 'name', 'email']
                                 ).intersection(set(table_columns))

            cur.execute(f"""
                SELECT key
                FROM "{entity_type}"
                WHERE {' OR '.join(f"{x} ILIKE %s" for x in search_columns)};
            """, tuple(
                [f'%{entity_id}%' for _ in range(len(search_columns))]
            ))

            entity_keys = [x['key'] for x in cur.fetchall()]

    cur.execute("""
        SELECT *, COUNT(*) OVER() AS total_items
        FROM (
            SELECT *
            FROM log
            WHERE
                (%s = 'all' OR user_key ILIKE %s OR %s = '{}'
                    OR user_key IN %s)
                AND (%s = 'all' OR entity_key ILIKE %s OR %s = '{}'
                    OR entity_key IN %s)
                AND (%s = 'all' OR entity_type = %s)
                AND (%s = 'all' OR action = %s)
            ORDER BY date DESC
        ) AS subquery
        LIMIT %s OFFSET %s;
    """, (
        user_id,
        f"%{user_id}%",
        user_keys,
        user_keys,

        entity_id,
        f"%{entity_id}%",
        entity_keys,
        entity_keys,

        entity_type,
        entity_type,
        user_action,
        user_action,

        page_size,
        (page_no - 1) * page_size
    ))

    logs = cur.fetchall()

    total_page = 0
    if logs:
        total_page = ceil(logs[0][-1] / page_size)

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "logs": [log_schema(x) for x in logs],
        "total_page": total_page
    })
