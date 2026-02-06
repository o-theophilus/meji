from flask import Blueprint, jsonify
from .postgres import db_open, db_close
# import os


bp = Blueprint("fix", __name__)


# @bp.get("/fix")
def quick_fix():
    con, cur = db_open()

    # cur.execute("""
    #     DROP TABLE IF EXISTS cart_item CASCADE;
    # """)
    cur.execute("""
        DROP TABLE IF EXISTS app CASCADE;
    """)
    # cur.execute("""
    #     ALTER TABLE item
    #     ALTER COLUMN quantity SET DEFAULT 10;
    # """)

    # cur.execute("""
    #     ALTER TABLE item
    #     ADD COLUMN specification JSONB DEFAULT '{}'::JSONB;
    # """)

    # cur.execute("""
    #     UPDATE "user" SET access=%s WHERE email = %s;
    # """, (
    #     [f"{x}:{y[0]}" for x in access_pass for y in access_pass[x]],
    #     os.environ["MAIL_USERNAME"]
    # ))

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
