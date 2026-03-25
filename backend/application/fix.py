import os

from flask import Blueprint, jsonify

from .postgres import db_close, db_open
from .tools import access_pass

bp = Blueprint("fix", __name__)


@bp.get("/fix")
def quick_fix():
    con, cur = db_open()

    cur.execute("""
        DROP TABLE IF EXISTS review CASCADE;
        DROP TABLE IF EXISTS coupon CASCADE;

        CREATE TABLE IF NOT EXISTS comment (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            date_created TIMESTAMPTZ DEFAULT now(),
            user_key UUID NOT NULL REFERENCES "user"(key) ON DELETE CASCADE,
            entity_type TEXT NOT NULL, -- blog, item
            entity_key UUID NOT NULL,
            parent_key UUID REFERENCES comment(key) ON DELETE CASCADE,
            comment TEXT NOT NULL,
            rating INT DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS blog (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            status TEXT NOT NULL DEFAULT 'draft',
            date_created TIMESTAMPTZ DEFAULT now(),
            author_key UUID NOT NULL REFERENCES "user"(key),
            title TEXT NOT NULL,
            slug TEXT UNIQUE NOT NULL,
            content TEXT,
            description TEXT,
            photo TEXT,
            files TEXT[] DEFAULT '{}'::TEXT[],
            tags TEXT[] DEFAULT '{}'::TEXT[],
            featured INT DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS model (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            status TEXT NOT NULL DEFAULT 'draft',
            date_created TIMESTAMPTZ DEFAULT now(),
            slug TEXT UNIQUE NOT NULL,
            url TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            information TEXT,
            photo TEXT
        );

        CREATE TABLE IF NOT EXISTS coupon (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            date_created TIMESTAMPTZ DEFAULT now(),
            order_key UUID UNIQUE REFERENCES "order"(key) ON DELETE SET NULL,
            status TEXT NOT NULL DEFAULT 'inactive',
            valid_from TIMESTAMPTZ,
            valid_until TIMESTAMPTZ,
            code TEXT UNIQUE NOT NULL,
            benefit JSONB DEFAULT '{}'::JSONB
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
