from flask import Blueprint, jsonify

from .postgres import db_close, db_open
from .tools import get_session

bp = Blueprint("dashboard", __name__)


order_status = ['created', 'processing', 'enroute', 'delivered', 'canceled']


def order_status_count(cur):
    cur.execute("""
        SELECT s.status, COUNT(o.*) AS count
        FROM unnest(%s::text[]) AS s(status)
        LEFT JOIN "order" o ON o.status = s.status
        GROUP BY s.status
        ORDER BY array_position(%s, s.status);
    """, (order_status, order_status))

    return cur.fetchall()


@bp.get("/dashboard")
def dashboard():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    # user = session["user"]

    orders = order_status_count(cur)

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "orders": orders,
    })
