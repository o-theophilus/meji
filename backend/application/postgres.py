from flask import Blueprint, jsonify
import os
import psycopg2
import psycopg2.extras
from werkzeug.security import generate_password_hash
from .tools import access_pass


bp = Blueprint("postgres", __name__)


def db_open():
    con = psycopg2.connect(os.environ["DATABASE_URI"])
    cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return con, cur


def db_close(con, cur):
    con.commit()
    cur.close()
    con.close()


# @bp.get("/fix")
def create_tables():
    con, cur = db_open()

    cur.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto";')
    cur.execute("""
        DROP TABLE IF EXISTS app CASCADE;
        DROP TABLE IF EXISTS "user" CASCADE;
        DROP TABLE IF EXISTS session CASCADE;
        DROP TABLE IF EXISTS log CASCADE;
        DROP TABLE IF EXISTS code CASCADE;
        DROP TABLE IF EXISTS report CASCADE;
        DROP TABLE IF EXISTS block CASCADE;
        DROP TABLE IF EXISTS item CASCADE;
        DROP TABLE IF EXISTS review CASCADE;
        DROP TABLE IF EXISTS "like" CASCADE;
        DROP TABLE IF EXISTS "order" CASCADE;
        DROP TABLE IF EXISTS order_item CASCADE;
        DROP TABLE IF EXISTS voucher CASCADE;

        CREATE TABLE IF NOT EXISTS app (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            alias TEXT UNIQUE NOT NULL,
            value JSONB DEFAULT '{}'::JSONB
        );

        CREATE TABLE IF NOT EXISTS "user" (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            status TEXT NOT NULL DEFAULT 'anonymous',
            date_created TIMESTAMPTZ DEFAULT now(),
            date_updated TIMESTAMPTZ DEFAULT now(),
            access TEXT[] DEFAULT '{}'::TEXT[],
            theme TEXT NOT NULL DEFAULT 'dark',
            item_view TEXT NOT NULL DEFAULT 'grid',
            name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            phone TEXT,
            address JSONB DEFAULT '{}'::JSONB,
            photo TEXT,
            account_balance FLOAT DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS session (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            date_created TIMESTAMPTZ DEFAULT now(),
            date_updated TIMESTAMPTZ DEFAULT now(),
            user_key UUID NOT NULL REFERENCES "user"(key),
            login TEXT NOT NULL DEFAULT 'false',
            remember BOOL NOT NULL DEFAULT FALSE
        );

        CREATE TABLE IF NOT EXISTS log (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            date_created TIMESTAMPTZ DEFAULT now(),
            user_key UUID NOT NULL,
            action TEXT NOT NULL,
            entity_key TEXT NOT NULL,
            entity_type TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT '200',
            misc JSONB DEFAULT '{}'::JSONB
        );

        CREATE TABLE IF NOT EXISTS code (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            date_created TIMESTAMPTZ DEFAULT now(),
            user_key UUID NOT NULL REFERENCES "user"(key),
            pin TEXT NOT NULL,
            email TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS report (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            date_created TIMESTAMPTZ DEFAULT now(),
            user_key UUID NOT NULL REFERENCES "user"(key),
            entity_key UUID NOT NULL,
            entity_type TEXT NOT NULL,
            comment TEXT NOT NULL,
            tags TEXT[] DEFAULT '{}'::TEXT[]
        );

        CREATE TABLE IF NOT EXISTS block (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            date_created TIMESTAMPTZ DEFAULT now(),
            admin_key UUID NOT NULL REFERENCES "user"(key),
            user_key UUID NOT NULL REFERENCES "user"(key),
            comment TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS item (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            status TEXT NOT NULL DEFAULT 'draft',
            date_created TIMESTAMPTZ DEFAULT now(),
            slug TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            tags TEXT[] DEFAULT '{}'::TEXT[],
            price FLOAT DEFAULT 0,
            price_old FLOAT DEFAULT 0,
            information TEXT,
            files TEXT[] DEFAULT '{}'::TEXT[],
            variation JSONB DEFAULT '{}'::JSONB,
            quantity INT DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS review (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            date_created TIMESTAMPTZ DEFAULT now(),
            user_key UUID NOT NULL REFERENCES "user"(key),
            item_key UUID NOT NULL REFERENCES item(key),
            parent_key UUID REFERENCES review(key),
            comment TEXT NOT NULL,
            rating INT DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS "like" (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            date_created TIMESTAMPTZ DEFAULT now(),
            user_key UUID NOT NULL REFERENCES "user"(key),
            entity_key TEXT NOT NULL,
            entity_type TEXT NOT NULL,
            reaction TEXT NOT NULL
        );

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

        CREATE TABLE IF NOT EXISTS order_item (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            date_created TIMESTAMPTZ DEFAULT now(),
            order_key UUID NOT NULL REFERENCES "order"(key),
            item_key UUID NOT NULL REFERENCES item(key),
            variation JSONB DEFAULT '{}'::JSONB,
            quantity INT DEFAULT 0,
            price FLOAT DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS voucher (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            date_created TIMESTAMPTZ DEFAULT now(),
            date_updated TIMESTAMPTZ DEFAULT now(),
            status TEXT NOT NULL DEFAULT 'created',
            pin TEXT NOT NULL,
            value FLOAT DEFAULT 0,
            validity TIMESTAMPTZ,
            usage JSONB DEFAULT '{}'::JSONB
        );
    """)

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


def copy_post_table():
    con = psycopg2.connect(os.environ["LOCAL_DB"])
    cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("SELECT * FROM post;")
    data = cur.fetchall()
    con.commit()
    cur.close()
    con.close()

    con = psycopg2.connect(os.environ["ONLINE_DB"])
    cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
            INSERT INTO "user"
            (status, name, username, email, password, access)
            VALUES (%s, %s, %s, %s, %s, %s)
        ;""", (
        "confirmed",
        "Theophilus",
        "theophilus",
        os.environ["MAIL_USERNAME"],
        generate_password_hash(
            os.environ["MAIL_PASSWORD"], method="scrypt"),
        [f"{x}:{y[0]}" for x in access_pass for y in access_pass[x]]
    ))

    for x in data:
        cur.execute("""
            INSERT INTO post(
                key,
                status,
                date_created,
                title,
                slug,
                content,
                description,
                photo,
                files,
                tags
            )
            VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (
            x["key"],
            x["status"],
            x["date_created"],
            x["title"],
            x["slug"],
            x["content"],
            x["description"],
            x["photo"],
            x["files"],
            x["tags"]
        ))

    con.commit()
    cur.close()
    con.close()

    return jsonify({
        "status": 200
    })
