from flask import Blueprint, jsonify
from .postgres import db_open, db_close


bp = Blueprint("fix", __name__)


# @bp.get("/fix")
def quick_fix():
    con, cur = db_open()

    # cur.execute("""
    #     ALTER TABLE session ADD COLUMN remember BOOL DEFAULT FALSE;
    # """)
    # cur.execute("""
    #     DELETE FROM app;
    # """)

    cur.execute("""
        DROP TABLE IF EXISTS feedback CASCADE;

        CREATE TABLE IF NOT EXISTS review (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            date_created TIMESTAMPTZ DEFAULT now(),
            user_key UUID NOT NULL REFERENCES "user"(key),
            item_key UUID NOT NULL REFERENCES item(key),
            parent_key UUID REFERENCES review(key),
            comment TEXT NOT NULL,
            rating INT DEFAULT 0
        );
    """)

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
