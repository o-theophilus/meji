import os

from flask import Blueprint, jsonify

from .postgres import db_close, db_open
from .tools import access_pass

bp = Blueprint("fix", __name__)


# @bp.get("/fix")
def quick_fix():
    con, cur = db_open()

    cur.execute("""
        DELETE FROM log
        WHERE entity_type = 'page' AND action = '/3dhub'
    ;""")
    cur.execute("""
        DELETE FROM log
        WHERE entity_type = 'page' AND action = '/@omni'
    ;""")
    cur.execute("""
        UPDATE log
        SET action = '/orders'
        WHERE entity_type = 'page' AND action = '/order'
    ;""")
    cur.execute("""
        UPDATE log
        SET entity_type = 'blog', action = 'viewed blog'
        WHERE entity_type = 'post' AND action = 'viewed'
    ;""")

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


def fix_access():
    con, cur = db_open()

    cur.execute("""
        UPDATE "user" SET access=%s WHERE email = %s;
    """, (
        [f"{x}.{y[0]}" for x in access_pass for y in access_pass[x]],
        os.environ["MAIL_USERNAME"]
    ))

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
