from flask import Blueprint, jsonify
import os
import psycopg2
from psycopg2.extras import Json, RealDictCursor


bp = Blueprint("postgres", __name__)


def db_open():
    con = psycopg2.connect(os.environ["DATABASE_URI"])
    cur = con.cursor(cursor_factory=RealDictCursor)
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
        DROP TABLE IF EXISTS item_snap CASCADE;
        DROP TABLE IF EXISTS coupon CASCADE;

        CREATE TABLE IF NOT EXISTS "user" (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            status TEXT NOT NULL DEFAULT 'anonymous',
            date_created TIMESTAMPTZ DEFAULT now(),
            access TEXT[] DEFAULT '{}'::TEXT[],
            theme TEXT NOT NULL DEFAULT 'system',
            item_view TEXT NOT NULL DEFAULT 'grid',
            name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            phone TEXT,
            address JSONB DEFAULT '{}'::JSONB,
            photo TEXT
        );

        CREATE TABLE IF NOT EXISTS session (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            date_created TIMESTAMPTZ DEFAULT now(),
            date_updated TIMESTAMPTZ DEFAULT now(),
            user_key UUID NOT NULL REFERENCES "user"(key) ON DELETE CASCADE,
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
            user_key UUID NOT NULL REFERENCES "user"(key) ON DELETE CASCADE,
            pin TEXT NOT NULL,
            email TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS report (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            date_created TIMESTAMPTZ DEFAULT now(),
            user_key UUID NOT NULL REFERENCES "user"(key) ON DELETE CASCADE,
            entity_key UUID NOT NULL,
            entity_type TEXT NOT NULL,
            comment TEXT NOT NULL,
            tags TEXT[] DEFAULT '{}'::TEXT[]
        );

        CREATE TABLE IF NOT EXISTS block (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            date_created TIMESTAMPTZ DEFAULT now(),
            admin_key UUID NOT NULL REFERENCES "user"(key) ON DELETE CASCADE,
            user_key UUID NOT NULL REFERENCES "user"(key) ON DELETE CASCADE,
            comment TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS item (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            status TEXT NOT NULL DEFAULT 'draft',
            date_created TIMESTAMPTZ DEFAULT now(),
            slug TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            tags TEXT[] DEFAULT '{}'::TEXT[],
            price DECIMAL DEFAULT 0,
            price_old DECIMAL DEFAULT 0,
            information TEXT,
            specification JSONB DEFAULT '{}'::JSONB,
            files TEXT[] DEFAULT '{}'::TEXT[],
            variation JSONB DEFAULT '{}'::JSONB,
            quantity INT DEFAULT 10
        );

        CREATE TABLE IF NOT EXISTS advert (
            key UUID PRIMARY KEY REFERENCES item(key) ON DELETE CASCADE,
            space TEXT[] DEFAULT '{}'::TEXT[],
            photo JSONB DEFAULT '{}'::JSONB
        );

        CREATE TABLE IF NOT EXISTS review (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            date_created TIMESTAMPTZ DEFAULT now(),
            user_key UUID NOT NULL REFERENCES "user"(key) ON DELETE CASCADE,
            item_key UUID NOT NULL REFERENCES item(key) ON DELETE CASCADE,
            parent_key UUID REFERENCES review(key) ON DELETE CASCADE,
            comment TEXT NOT NULL,
            rating INT DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS "like" (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            date_created TIMESTAMPTZ DEFAULT now(),
            user_key UUID NOT NULL REFERENCES "user"(key) ON DELETE CASCADE,
            item_key UUID REFERENCES item(key) ON DELETE CASCADE,
            review_key UUID REFERENCES review(key) ON DELETE CASCADE,
            reaction TEXT NOT NULL,
            CHECK (
                (item_key IS NOT NULL AND review_key IS NULL) OR
                (item_key IS NULL AND review_key IS NOT NULL)
            )
        );

        CREATE TABLE IF NOT EXISTS "order" (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            status TEXT NOT NULL DEFAULT 'cart',
            date_created TIMESTAMPTZ DEFAULT now(),
            user_key UUID NOT NULL REFERENCES "user"(key) ON DELETE CASCADE,
            receiver JSONB DEFAULT '{}'::JSONB,
            cost_items DECIMAL DEFAULT 0,
            cost_delivery DECIMAL DEFAULT 1500,
            pay_user DECIMAL DEFAULT 0,
            pay_reference TEXT,
            coupons TEXT[] DEFAULT '{}'::TEXT[],
            timeline JSONB DEFAULT '{}'::JSONB
        );

        CREATE TABLE IF NOT EXISTS order_item (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            date_created TIMESTAMPTZ DEFAULT now(),
            order_key UUID NOT NULL REFERENCES "order"(key) ON DELETE CASCADE,
            item_key UUID NOT NULL REFERENCES item(key) ON DELETE CASCADE,
            variation JSONB DEFAULT '{}'::JSONB,
            quantity INT DEFAULT 0,
            price DECIMAL DEFAULT 0
        );

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


def copy_db():
    def copy_table(from_cur, to_cur, table_name):
        from_cur.execute(f"""SELECT * FROM "{table_name}";""")
        data = from_cur.fetchall()

        if not data:
            return

        columns = list(data[0].keys())

        values_list = []
        for row in data:
            values = []
            for column in columns:
                if type(row[column]) is dict:
                    row[column] = Json(row[column])
                values.append(row[column])
            values_list.append(tuple(values))

        to_cur.executemany(f"""
            INSERT INTO "{table_name}"({', '.join(columns)})
            VALUES ({', '.join(['%s'] * len(columns))});
        """, values_list)

    from_con = psycopg2.connect(os.environ["ONLINE_DB"])
    from_cur = from_con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    to_con = psycopg2.connect(os.environ["LOCAL_DB"])
    to_cur = to_con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    copy_table(from_cur, to_cur, "user")
    copy_table(from_cur, to_cur, "post")
    copy_table(from_cur, to_cur, "comment")
    copy_table(from_cur, to_cur, "report")
    copy_table(from_cur, to_cur, "block")
    copy_table(from_cur, to_cur, "like")
    copy_table(from_cur, to_cur, "code")
    copy_table(from_cur, to_cur, "log")
    copy_table(from_cur, to_cur, "session")

    from_con.commit()
    from_cur.close()
    from_con.close()
    to_con.commit()
    to_cur.close()
    to_con.close()

    return jsonify({
        "status": 200
    })
