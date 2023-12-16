from flask import Blueprint, jsonify
import os
import psycopg2
import psycopg2.extras
# import sqlite3


bp = Blueprint("postgres", __name__)


user_table = """CREATE TABLE IF NOT EXISTS "user" (
    key CHAR(32) PRIMARY KEY,
    version CHAR(32) NOT NULL,
    date_created TIMESTAMP NOT NULL,
    date_updated TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'anonymous',

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
    FOREIGN KEY (user_key) REFERENCES "user"(key) ON DELETE CASCADE
);"""


def query_run(query, many=False):
    con = psycopg2.connect(os.environ["DATABASE_URI"])
    cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    # con = sqlite3.connect(
    # os.environ["DATABASE_URI"], check_same_thread=False)
    # cur = con.cursor()

    out = []

    def inner(inp):
        ret = []
        data = []
        if type(inp) is tuple and len(inp) == 2:
            data = inp[1]
            inp = inp[0]

        cur.execute(inp, data)

        try:
            one = cur.fetchone()
            # print("============> ", one)
            if one:
                ret.append(one)
            ret += cur.fetchall()
            # print("============> ", cur.fetchall())
        except psycopg2.Error as e:
            print("Error occurred:", e)

        return ret

    if type(query) is list:
        for q in query:
            out += inner(q)
    else:
        out += inner(query)

    con.commit()
    cur.close()
    con.close()

    # out = [dict(x) for x in out]
    if many:
        return out
    return out[0] if out != [] else None


@bp.post("/create_tables")
def create_tables():

    query_run([
        """
        DROP TABLE IF EXISTS "user";
        DROP TABLE IF EXISTS log;
        """,
        user_table,
        log_table
    ])

    return jsonify({
        "status": 200,
        "message": "successful",
    })


@bp.post("/pgs")
def pgs():

    # query_run(user_template())

    return jsonify({
        "status": 200,
        "message": "successful",
    })
