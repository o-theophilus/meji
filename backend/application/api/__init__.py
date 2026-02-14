import os
import re

from flask import Blueprint, jsonify, request

from ..log import log
from ..postgres import db_close, db_open
from ..storage import storage
from ..tools import send_mail

bp = Blueprint("api", __name__)


@bp.get("/cron")
def cron():
    con, cur = db_open()

    cur.execute("""
        SELECT key FROM "user" WHERE email = %s;
    """, (os.environ["MAIL_USERNAME"],))
    user = cur.fetchone()

    cur.execute("""
        DELETE FROM session
        WHERE (
                remember = FALSE
                AND date_updated <= NOW() - INTERVAL '3 days'
            ) OR (
                remember = TRUE
                AND date_updated <= NOW() - INTERVAL '14 days'
            )
        RETURNING key;
    """)
    sessions = cur.fetchall()

    cur.execute("""
        DELETE FROM "user"
        WHERE status = 'anonymous'
            AND date_created <= NOW() - INTERVAL '30 days'
        RETURNING key, photo;
    """)
    users = cur.fetchall()
    for x in users:
        storage.delete(x["photo"], "user")

    log(
        cur=cur,
        user_key=user["key"],
        action="app maintenance",
        entity_key="app",
        entity_type="app",
        misc={
            "deleted_sessions": [x["key"] for x in sessions],
            "deleted_users": [x["key"] for x in users],
        }
    )

    cur.execute("""
        WITH expired AS (
            UPDATE coupon SET status = 'expired'
            WHERE valid_until < NOW() AND status = 'active'
            RETURNING key
        )
        INSERT INTO log (user_key, action, entity_key, entity_type)
        SELECT %s, 'expired coupon', key, 'coupon'
        FROM expired;
    """, (user["key"],))

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/contact")
def footer_send_email():

    email_template = request.json.get("email_template")
    name = request.json.get("name")
    email = request.json.get("email")
    message = request.json.get("message")

    if not email_template:
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    error = {}
    if not name:
        error["name"] = "This field is required"
    elif len(name) > 100:
        error["name"] = "This field cannot exceed 100 characters"

    if not email:
        error["email"] = "This field is required"
    elif not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
        error["email"] = "Invalid email address"
    elif len(email) > 255:
        error["email"] = "This field cannot exceed 255 characters"

    if not message:
        error["message"] = "This field is required"
    if error:
        return jsonify({
            "status": 400,
            **error
        })

    message = email_template.format(
        name=name, email=email, message=message)

    send_mail(
        os.environ["MAIL_USERNAME"],
        f"{name} from Meji.ng",
        message
    )

    return jsonify({
        "status": 200
    })
