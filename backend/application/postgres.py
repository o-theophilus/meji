from flask import Blueprint
import os
import psycopg2
import psycopg2.extras


bp = Blueprint("postgres", __name__)


user_table = """CREATE TABLE IF NOT EXISTS "user" (
    key CHAR(32) PRIMARY KEY,
    version CHAR(32) NOT NULL,
    status VARCHAR(20) DEFAULT 'anonymous' NOT NULL,

    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(100),
    password VARCHAR(200) NOT NULL,

    line VARCHAR(100),
    country VARCHAR(100),
    state VARCHAR(100),
    local_area VARCHAR(100),
    postal_code VARCHAR(100),

    photo VARCHAR(50),
    account_balance FLOAT DEFAULT 0,
    permissions TEXT[] DEFAULT ARRAY[]::TEXT[],
    login BOOLEAN DEFAULT FALSE,

    setting_theme VARCHAR(20) DEFAULT 'light',
    setting_item_view VARCHAR(20) DEFAULT 'grid'
);"""


item_table = """CREATE TABLE IF NOT EXISTS item (
    key CHAR(32) PRIMARY KEY,
    status VARCHAR(20) DEFAULT 'draft' NOT NULL,

    name VARCHAR(100) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    price FLOAT DEFAULT 0 NOT NULL,
    show_discount VARCHAR(32) DEFAULT 'true',
    information TEXT,
    photos TEXT[] DEFAULT ARRAY[]::TEXT[],
    tags TEXT[] DEFAULT ARRAY[]::TEXT[],
    variation JSONB DEFAULT '{}'::JSONB,

    available_quantity INT DEFAULT 0
);"""


save_table = """CREATE TABLE IF NOT EXISTS save (
    key CHAR(32) PRIMARY KEY,

    user_key CHAR(32) NOT NULL,
    item_key CHAR(32) NOT NULL,

    FOREIGN KEY (user_key) REFERENCES "user"(key),
    FOREIGN KEY (item_key) REFERENCES item(key)
);"""


order_table = """CREATE TABLE IF NOT EXISTS "order" (
    key CHAR(32) PRIMARY KEY,
    version CHAR(32) NOT NULL,
    user_key CHAR(32) NOT NULL,
    status VARCHAR(20) DEFAULT 'cart' NOT NULL,

    delivery_date TIMESTAMP,

    name VARCHAR(100),
    phone VARCHAR(100),
    line VARCHAR(100),
    country VARCHAR(100),
    state VARCHAR(100),
    local_area VARCHAR(100),
    postal_code VARCHAR(100),

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


feedback_table = """CREATE TABLE IF NOT EXISTS feedback (
    key CHAR(32) PRIMARY KEY,

    user_key CHAR(32) NOT NULL,
    item_key CHAR(32) NOT NULL,

    rating INT DEFAULT 0,
    review TEXT,

    FOREIGN KEY (user_key) REFERENCES "user"(key) ON DELETE CASCADE,
    FOREIGN KEY (item_key) REFERENCES item(key)
);"""


advert_table = """CREATE TABLE IF NOT EXISTS advert (
    key CHAR(32) PRIMARY KEY,

    spaces TEXT[] DEFAULT ARRAY[]::TEXT[],
    photo_300x300 VARCHAR(50),
    photo_300x600 VARCHAR(50),
    photo_600x300 VARCHAR(50),
    photo_900x300 VARCHAR(50),

    FOREIGN KEY (key) REFERENCES item(key) ON DELETE CASCADE
);"""


voucher_table = """CREATE TABLE IF NOT EXISTS voucher (
    key CHAR(32) PRIMARY KEY,
    version CHAR(32) NOT NULL,
    batch CHAR(32),
    status VARCHAR(20) DEFAULT 'created' NOT NULL,

    pin VARCHAR(10) NOT NULL,
    value FLOAT DEFAULT 0,
    validity TIMESTAMP
);"""


log_table = """CREATE TABLE IF NOT EXISTS log (
    key CHAR(32) PRIMARY KEY,
    date TIMESTAMP NOT NULL,
    user_key CHAR(32) NOT NULL,
    action VARCHAR(20) NOT NULL,
    entity_key TEXT,
    entity_type VARCHAR(100) NOT NULL,
    status INT DEFAULT 200,
    misc JSONB DEFAULT '{}'::JSONB,

    FOREIGN KEY (user_key) REFERENCES "user"(key)
);"""


otp_table = """CREATE TABLE IF NOT EXISTS otp (
    key CHAR(32) PRIMARY KEY,

    user_key CHAR(32) NOT NULL,
    pin VARCHAR(10) NOT NULL,
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
