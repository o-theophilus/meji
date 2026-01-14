from flask import Blueprint, jsonify
from .postgres import db_open, db_close


bp = Blueprint("fix", __name__)


@bp.get("/fix")
def quick_fix():
    con, cur = db_open()

    # cur.execute("""
    #     ALTER TABLE "order"
    #     RENAME COLUMN modifiers TO coupons;
    # """)

    # cur.execute("""
    #     ALTER TABLE "user"
    #     DROP COLUMN date_updated;
    # """)

    # cur.execute("""
    #     ALTER TABLE item
    #     ADD COLUMN specification JSONB DEFAULT '{}'::JSONB;
    # """)

    cur.execute("""
        DROP TABLE IF EXISTS item_snap CASCADE;
        DROP TABLE IF EXISTS coupon CASCADE;

        CREATE TABLE IF NOT EXISTS item_snap (
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

            item_key UUID NOT NULL REFERENCES item(key) ON DELETE NO ACTION,
            order_key UUID NOT NULL REFERENCES "order"(key) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS coupon (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            date_created TIMESTAMPTZ DEFAULT now(),
            date_updated TIMESTAMPTZ DEFAULT now(),
            status TEXT NOT NULL DEFAULT 'created',
            pin TEXT NOT NULL,
            value JSONB DEFAULT '{}'::JSONB,
            validity TIMESTAMPTZ,
            order_key UUID REFERENCES "order"(key) ON DELETE NO ACTION
        );
    """)

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
