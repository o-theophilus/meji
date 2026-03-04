import os

from flask import Blueprint, jsonify

from .postgres import db_close, db_open
from .tools import access_pass
from psycopg2.extras import Json

bp = Blueprint("fix", __name__)


@bp.get("/fix")
def quick_fix():
    con, cur = db_open()

    cur.execute("""
        DROP TABLE IF EXISTS ""like"";

        CREATE TABLE IF NOT EXISTS item_like (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            date_created TIMESTAMPTZ DEFAULT now(),
            user_key UUID NOT NULL REFERENCES "user"(key) ON DELETE CASCADE,
            item_key UUID REFERENCES item(key) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS review_like (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            date_created TIMESTAMPTZ DEFAULT now(),
            user_key UUID NOT NULL REFERENCES "user"(key) ON DELETE CASCADE,
            review_key UUID REFERENCES review(key) ON DELETE CASCADE,
            reaction TEXT NOT NULL
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
        [f"{x}:{y[0]}" for x in access_pass for y in access_pass[x]],
        os.environ["MAIL_USERNAME"]
    ))

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
