from flask import Blueprint, jsonify
from .postgres import db_open, db_close


bp = Blueprint("fix", __name__)


# @bp.get("/fix")
def quick_fix():
    con, cur = db_open()

    # cur.execute("""
    #     ALTER TABLE session ADD COLUMN remember BOOL DEFAULT FALSE;
    # """)
    # cur.execute("""
    #     DELETE FROM app;
    # """)

    cur.execute("""
        DROP TABLE IF EXISTS "order" CASCADE;

        CREATE TABLE IF NOT EXISTS "order" (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            status TEXT NOT NULL DEFAULT 'cart',
            date_created TIMESTAMPTZ DEFAULT now(),
            date_updated TIMESTAMPTZ DEFAULT now(),
            user_key UUID NOT NULL REFERENCES "user"(key),
            reciever JSONB DEFAULT '{}'::JSONB,
            cost_delivery FLOAT DEFAULT 1500,
            cost_items FLOAT DEFAULT 0,
            pay_account FLOAT DEFAULT 0,
            pay_user FLOAT DEFAULT 0,
            pay_reference TEXT,
            delivery_date TIMESTAMPTZ
        );
    """)

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
