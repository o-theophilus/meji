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
        ALTER TABLE "order" DROP COLUMN coupons;
        DROP TABLE IF EXISTS app CASCADE;
        DROP TABLE IF EXISTS coupon CASCADE;
        CREATE TABLE IF NOT EXISTS coupon (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            date_created TIMESTAMPTZ DEFAULT now(),
            order_key UUID REFERENCES "order"(key) ON DELETE NO ACTION,
            status TEXT NOT NULL DEFAULT 'created',
            valid_from TIMESTAMPTZ,
            valid_until TIMESTAMPTZ,
            code TEXT UNIQUE NOT NULL,
            benefit JSONB DEFAULT '{}'::JSONB
        );
    """)

    # cur.execute("""
    #     ALTER TABLE item
    #     ALTER COLUMN quantity SET DEFAULT 10;
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
