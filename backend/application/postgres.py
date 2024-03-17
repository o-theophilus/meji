from flask import Blueprint, jsonify
import os
import psycopg2
import psycopg2.extras


bp = Blueprint("postgres", __name__)


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

    available_quantity INT DEFAULT 0
);"""


save_table = """CREATE TABLE IF NOT EXISTS save (
    key CHAR(32) PRIMARY KEY,
    date TIMESTAMP NOT NULL,

    user_key CHAR(32) NOT NULL,
    item_key CHAR(32) NOT NULL,

    FOREIGN KEY (user_key) REFERENCES "user"(key),
    FOREIGN KEY (item_key) REFERENCES item(key)
);"""


# "cart", 'created', 'processing', 'enroute', 'delivered'
order_table = """CREATE TABLE IF NOT EXISTS "order" (
    key CHAR(32) PRIMARY KEY,
    version CHAR(32) NOT NULL,
    user_key CHAR(32) NOT NULL,
    status VARCHAR(20) DEFAULT 'cart' NOT NULL,

    delivery_date TIMESTAMP,

    receiver_name VARCHAR(100) NOT NULL,
    receiver_phone VARCHAR(100),
    receiver_address_line VARCHAR(100),
    receiver_address_country VARCHAR(100),
    receiver_address_state VARCHAR(100),
    receiver_address_local_area VARCHAR(100),
    receiver_address_postal_code VARCHAR(100),

    cost_delivery FLOAT DEFAULT 1500,
    cost_items FLOAT DEFAULT 0,
    pay_account FLOAT DEFAULT 0,
    pay_user FLOAT DEFAULT 0,
    pay_reference VARCHAR(100),

    FOREIGN KEY (user_key) REFERENCES "user"(key)
);"""


order_item_table = """CREATE TABLE IF NOT EXISTS order_item (
    key CHAR(32) PRIMARY KEY,

    order_key CHAR(32) NOT NULL,
    item_key CHAR(32) NOT NULL,

    variation JSONB DEFAULT '{}'::JSONB,
    quantity INT DEFAULT 0,

    FOREIGN KEY (order_key) REFERENCES "order"(key) ON DELETE CASCADE,
    FOREIGN KEY (item_key) REFERENCES item(key)
);"""


# TODO: Remover version from n on financial ops
feedback_table = """CREATE TABLE IF NOT EXISTS feedback (
    key CHAR(32) PRIMARY KEY,
    version CHAR(32) NOT NULL,

    user_key CHAR(32) NOT NULL,
    item_key CHAR(32) NOT NULL,

    rating INT DEFAULT 0,
    review TEXT,

    FOREIGN KEY (user_key) REFERENCES "user"(key) ON DELETE CASCADE,
    FOREIGN KEY (item_key) REFERENCES item(key)
);"""

advert_table = """CREATE TABLE IF NOT EXISTS advert (
    key CHAR(32) PRIMARY KEY,

    placement TEXT[] DEFAULT ARRAY[]::TEXT[],
    photo_300x300 VARCHAR(36),
    photo_300x600 VARCHAR(36),
    photo_600x300 VARCHAR(36),
    photo_900x300 VARCHAR(36),

    FOREIGN KEY (key) REFERENCES item(key) ON DELETE CASCADE
);"""


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


# TODO:
# Move date to log_table
# Add [otp]->[requested] to frontend log
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


@bp.post("/create_table")
def create_table():
    con, cur = db_open()

    cur.execute(f"""
        DROP TABLE IF EXISTS "user" CASCADE;
        DROP TABLE IF EXISTS item CASCADE;
        DROP TABLE IF EXISTS save;
        DROP TABLE IF EXISTS "order" CASCADE;
        DROP TABLE IF EXISTS order_item;
        DROP TABLE IF EXISTS feedback;
        DROP TABLE IF EXISTS advert;
        DROP TABLE IF EXISTS voucher;
        DROP TABLE IF EXISTS log;
        DROP TABLE IF EXISTS otp;
        {user_table};
        {item_table};
        {save_table};
        {order_table};
        {order_item_table};
        {feedback_table};
        {advert_table};
        {voucher_table};
        {log_table};
        {otp_table};
    """)

    db_close(con, cur)

    return jsonify({
        "status": 200,
        "message": "successful",
    })
