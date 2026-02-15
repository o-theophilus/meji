# import os

from flask import Blueprint, jsonify

from .postgres import db_close, db_open

# from .tools import access_pass

bp = Blueprint("fix", __name__)


# @bp.get("/fix")
def quick_fix():
    con, cur = db_open()

    # cur.execute("""
    #     DROP TABLE IF EXISTS cart_item CASCADE;
    # """)

    cur.execute("""
        ALTER TABLE "order" RENAME COLUMN cost_items TO order_cost;
        ALTER TABLE "order" RENAME COLUMN cost_delivery TO delivery_cost;
        ALTER TABLE "order" RENAME COLUMN pay_user TO payment;
        ALTER TABLE "order" RENAME COLUMN pay_reference TO payment_reference;
    """)

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
