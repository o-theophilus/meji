import os

from flask import Blueprint, jsonify

from .postgres import db_close, db_open
from .tools import access_pass

bp = Blueprint("fix", __name__)


# @bp.get("/fix")
def quick_fix():
    con, cur = db_open()

    cur.execute("""
        DROP TABLE IF EXISTS report;

        CREATE TABLE IF NOT EXISTS report (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            status TEXT NOT NULL DEFAULT 'active',
            date_created TIMESTAMPTZ DEFAULT now(),
            reporter_key UUID NOT NULL REFERENCES "user"(key)
                ON DELETE SET NULL,
            reporter_comment TEXT NOT NULL,
            tags TEXT[] DEFAULT '{}'::TEXT[],
            date_resolved TIMESTAMPTZ,
            resolver_key UUID REFERENCES "user"(key) ON DELETE SET NULL,
            resolver_comment TEXT,
            reported_user_key UUID REFERENCES "user"(key) ON DELETE CASCADE,
            reported_review_key UUID REFERENCES review(key) ON DELETE CASCADE
        );
    """)

    # cur.execute("""
    #     DROP TABLE IF EXISTS item_snap;
    #     DROP TABLE IF EXISTS coupon;
    #     DROP TABLE IF EXISTS item_like;
    #     DROP TABLE IF EXISTS review_like;
    #     DROP TABLE IF EXISTS order_item;
    #     DROP TABLE IF EXISTS "order";

    #     CREATE TABLE IF NOT EXISTS "order" (
    #         key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    #         status TEXT NOT NULL DEFAULT 'cart',
    #         date_created TIMESTAMPTZ DEFAULT now(),
    #         user_key UUID NOT NULL REFERENCES "user"(key) ON DELETE CASCADE,
    #         receiver JSONB DEFAULT '{}'::JSONB,
    #         order_cost DECIMAL DEFAULT 0,
    #         delivery_cost DECIMAL DEFAULT 0,
    #         payment DECIMAL DEFAULT 0,
    #         payment_reference TEXT,
    #         timeline JSONB DEFAULT '{}'::JSONB
    #     );

    #     CREATE TABLE IF NOT EXISTS item_like (
    #         key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    #         date_created TIMESTAMPTZ DEFAULT now(),
    #         user_key UUID NOT NULL REFERENCES "user"(key) ON DELETE CASCADE,
    #         item_key UUID NOT NULL REFERENCES item(key) ON DELETE CASCADE,
    #         UNIQUE (user_key, item_key)
    #     );

    #     CREATE TABLE IF NOT EXISTS review_like (
    #         key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    #         date_created TIMESTAMPTZ DEFAULT now(),
    #         user_key UUID NOT NULL REFERENCES "user"(key) ON DELETE CASCADE,
    #         review_key UUID NOT NULL REFERENCES review(key)
    #               ON DELETE CASCADE,
    #         UNIQUE (user_key, review_key),
    #         reaction TEXT NOT NULL
    #     );

    #     CREATE TABLE IF NOT EXISTS coupon (
    #         key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    #         date_created TIMESTAMPTZ DEFAULT now(),
    #         order_key UUID REFERENCES "order"(key) ON DELETE SET NULL,
    #         status TEXT NOT NULL DEFAULT 'inactive',
    #         valid_from TIMESTAMPTZ,
    #         valid_until TIMESTAMPTZ,
    #         code TEXT UNIQUE NOT NULL,
    #         benefit JSONB DEFAULT '{}'::JSONB,
    #         UNIQUE (order_key)
    #     );

    #     CREATE TABLE IF NOT EXISTS order_item (
    #         key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    #         date_created TIMESTAMPTZ DEFAULT now(),
    #         order_key UUID NOT NULL REFERENCES "order"(key)
    #               ON DELETE CASCADE,
    #         item_key UUID NOT NULL REFERENCES item(key) ON DELETE CASCADE,
    #         variation JSONB DEFAULT '{}'::JSONB,
    #         quantity INT DEFAULT 0,
    #         price DECIMAL DEFAULT 0,
    #         UNIQUE (order_key, item_key, variation)
    #     );

    #     CREATE TABLE IF NOT EXISTS item_snap (
    #         key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    #         status TEXT NOT NULL DEFAULT 'draft',
    #         date_created TIMESTAMPTZ DEFAULT now(),
    #         slug TEXT NOT NULL,
    #         name TEXT NOT NULL,
    #         tags TEXT[] DEFAULT '{}'::TEXT[],
    #         price DECIMAL DEFAULT 0,
    #         price_old DECIMAL DEFAULT 0,
    #         information TEXT,
    #         specification JSONB DEFAULT '{}'::JSONB,
    #         files TEXT[] DEFAULT '{}'::TEXT[],
    #         variation JSONB DEFAULT '{}'::JSONB,
    #         quantity INT DEFAULT 0,

    #         item_key UUID NOT NULL REFERENCES item(key) ON DELETE SET NULL,
    #         order_key UUID NOT NULL REFERENCES "order"(key) ON DELETE CASCADE
    #     );
    # """)

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


def fix_access():
    con, cur = db_open()

    cur.execute("""
        UPDATE "user" SET access=%s WHERE email = %s;
    """, (
        [f"{x}:{y[0]}" for x in access_pass for y in access_pass[x]],
        os.environ["MAIL_USERNAME"]
    ))

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
