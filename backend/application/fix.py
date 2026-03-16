import os

from flask import Blueprint, jsonify

from .postgres import db_close, db_open
from .tools import access_pass

bp = Blueprint("fix", __name__)


@bp.get("/fix")
def quick_fix():
    # TODO: live
    con, cur = db_open()

    cur.execute("""
        DROP TABLE IF EXISTS item_version CASCADE;
        DROP TABLE IF EXISTS item_snap CASCADE;
        DROP TABLE IF EXISTS order_item CASCADE;
        DROP TABLE IF EXISTS "order" CASCADE;

        CREATE TABLE IF NOT EXISTS "order" (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            status TEXT NOT NULL DEFAULT 'cart',
            date_created TIMESTAMPTZ DEFAULT now(),
            user_key UUID NOT NULL REFERENCES "user"(key) ON DELETE CASCADE,
            receiver JSONB DEFAULT '{}'::JSONB,
            order_cost DECIMAL DEFAULT 0,
            delivery_cost DECIMAL DEFAULT 0,
            payment DECIMAL DEFAULT 0,
            payment_reference TEXT,
            timeline JSONB DEFAULT '{}'::JSONB
        );

        CREATE TABLE IF NOT EXISTS item_version (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            status TEXT NOT NULL DEFAULT 'draft',
            date_created TIMESTAMPTZ DEFAULT now(),
            slug TEXT NOT NULL,
            name TEXT NOT NULL,
            tags TEXT[] DEFAULT '{}'::TEXT[],
            price DECIMAL DEFAULT 0,
            price_old DECIMAL DEFAULT 0,
            information TEXT,
            specification JSONB DEFAULT '{}'::JSONB,
            files TEXT[] DEFAULT '{}'::TEXT[],
            variation JSONB DEFAULT '{}'::JSONB,
            quantity INT DEFAULT 0,
            item_key UUID REFERENCES item(key) ON DELETE SET NULL
        );

        CREATE TABLE IF NOT EXISTS order_item (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            date_created TIMESTAMPTZ DEFAULT now(),
            order_key UUID NOT NULL REFERENCES "order"(key) ON DELETE CASCADE,
            item_key UUID REFERENCES item(key) ON DELETE CASCADE,
            item_version_key UUID REFERENCES item_version(key)
                ON DELETE CASCADE,
            variation JSONB DEFAULT '{}'::JSONB,
            quantity INT DEFAULT 0,
            UNIQUE (order_key, item_key, variation)
        );
    """)

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
