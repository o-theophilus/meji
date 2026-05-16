import os

from flask import Blueprint, jsonify
from psycopg2.extras import Json
from .postgres import db_close, db_open
from .tools import access_pass

bp = Blueprint("fix", __name__)


# @bp.get("/fix")
def quick_fix():
    con, cur = db_open()

    cur.execute("""
        UPDATE item
        SET metadata = %s
    ;""", (
        Json({
            "length": 0,
            "breadth": 0,
            "height": 0,
            "weight": 0,
            "area": "ijanikin",
            "prep_time": 7
        }),
    ))

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
