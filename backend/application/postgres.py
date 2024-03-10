from flask import Blueprint, jsonify
import os
import psycopg2
import psycopg2.extras
# import sqlite3


bp = Blueprint("postgres", __name__)


item_table = """CREATE TABLE IF NOT EXISTS item (
    key CHAR(32) PRIMARY KEY,
    version CHAR(32) NOT NULL,
    status VARCHAR(20) DEFAULT 'draft' NOT NULL,

    name VARCHAR(100) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    price FLOAT DEFAULT 0,
    old_price FLOAT DEFAULT 0,
    information TEXT,
    photos TEXT[] DEFAULT ARRAY[]::TEXT[],
    tags TEXT[] DEFAULT ARRAY[]::TEXT[],
    adverts JSONB DEFAULT '{}'::JSONB,
    variation JSONB DEFAULT '{}'::JSONB,

    available_quantity INT DEFAULT 0,
);"""

# "status": anonymous, signed_up, confirmed
user_table = """CREATE TABLE IF NOT EXISTS "user" (
    key CHAR(32) PRIMARY KEY,
    version CHAR(32) NOT NULL,
    status VARCHAR(20) DEFAULT 'anonymous' NOT NULL,

    name VARCHAR(100) DEFAULT 'anonymous',
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(100),
    password VARCHAR(200) NOT NULL,

    address_line VARCHAR(100),
    address_country VARCHAR(100),
    address_state VARCHAR(100),
    address_local_area VARCHAR(100),
    address_postal_code VARCHAR(100),

    photo VARCHAR(36),
    account_balance FLOAT DEFAULT 0,
    roles TEXT[] DEFAULT ARRAY[]::TEXT[],
    login BOOLEAN DEFAULT FALSE,

    setting_theme VARCHAR(20) DEFAULT 'light',
    setting_item_view VARCHAR(20) DEFAULT 'grid'
);"""

log_table = """CREATE TABLE IF NOT EXISTS log (
    key CHAR(32) PRIMARY KEY,
    date TIMESTAMP NOT NULL,
    user_key CHAR(32) NOT NULL,
    action VARCHAR(20) NOT NULL,
    entity_key CHAR(32),
    entity_type VARCHAR(20),
    status INT DEFAULT 200,
    misc JSONB DEFAULT '{}'::JSONB,

    FOREIGN KEY (user_key) REFERENCES "user"(key)
);"""
# FOREIGN KEY (user_key) REFERENCES "user"(key) ON DELETE CASCADE

# "status": inactive, active, used, deleted, expired
voucher_table = """CREATE TABLE IF NOT EXISTS voucher (
    key CHAR(32) PRIMARY KEY,
    version CHAR(32) NOT NULL,
    batch CHAR(32),
    status VARCHAR(20) DEFAULT 'inactive' NOT NULL,

    code VARCHAR(10) NOT NULL,
    value FLOAT DEFAULT 0,
    validity TIMESTAMP
);"""

otp_table = """CREATE TABLE IF NOT EXISTS otp (
    key CHAR(32) PRIMARY KEY,
    date TIMESTAMP NOT NULL,

    user_key CHAR(32) NOT NULL,
    code VARCHAR(10) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,

    FOREIGN KEY (user_key) REFERENCES "user"(key)
);"""


def db_open():
    con = psycopg2.connect(os.environ["DATABASE_URI"])
    cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return con, cur


def db_close(con, cur):
    con.commit()
    cur.close()
    con.close()


def query_run(query, data=None, many=False):
    con = psycopg2.connect(os.environ["DATABASE_URI"])
    cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    out = []

    try:
        cur.execute(query, data)
        out = cur.fetchall()
    except psycopg2.Error as e:
        print("Error occurred:", e)

    con.commit()
    cur.close()
    con.close()

    out = [dict(x) for x in out]
    if many:
        return out
    return out[0] if out != [] else None


@bp.post("/create_tables")
def create_tables():

    query_run(
        f"""
        DROP TABLE IF EXISTS "user";
        DROP TABLE IF EXISTS log;
        {user_table};
        {log_table};
        """
    )

    return jsonify({
        "status": 200,
        "message": "successful",
    })
