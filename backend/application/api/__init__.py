import os
import re

from flask import Blueprint, request
from psycopg2.extras import Json

from ..postgres import db_close, db_open
from ..tools import log, rate_limit, send_mail, session

bp = Blueprint("api", __name__)


def delete_session(cur, user_key):
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
        INSERT INTO log (
            user_key, action, entity_type, misc
        ) VALUES (%s, 'api.delete_session', 'app', %s);
    """, (
        user_key,
        Json({"deleted_sessions": [x["key"] for x in sessions]})
    ))


def delete_anonymous(cur, user_key):
    cur.execute("""
        DELETE FROM "user"
        WHERE status = 'anonymous'
            AND date_created <= NOW() - INTERVAL '30 days'
        RETURNING key;
    """)
    users = cur.fetchall()

    cur.execute("""
        INSERT INTO log (
            user_key, action, entity_type, misc
        ) VALUES (%s, 'api.delete_anonymous', 'app', %s);
    """, (
        user_key,
        Json({"deleted_users": [x["key"] for x in users]})
    ))


def expire_coupon(cur, user_key):
    cur.execute("""
        UPDATE coupon SET status = 'expired'
        WHERE valid_until < NOW() AND status = 'active'
        RETURNING key;
    """)
    for coupon in cur.fetchall():
        cur.execute("""
            INSERT INTO log (
                user_key, action, entity_type, entity_key
            ) VALUES (%s, 'coupon.expire', 'coupon', %s);
        """, (user_key, coupon["key"]))


@session(True)
@rate_limit(20, 1)
@log("app")
@bp.post("/maintenance/session")
def user_delete_session(cur, user):
    if "maintenance.session" not in user["access"]:
        return {
            "error": "unauthorized access"
        }, 403

    delete_session(cur, user["key"])
    return {
    }, 200


@bp.post("/maintenance/anonymous")
@session(True)
@rate_limit(20, 1)
@log("app")
def user_delete_anonymous(cur, user):
    if "maintenance.anonymous" not in user["access"]:
        return {
            "error": "unauthorized access"
        }, 403

    delete_session(cur, user["key"])

    return {
    }, 200


@bp.post("/maintenance/coupon")
@session(True)
@rate_limit(20, 1)
@log("app")
def user_expire_coupon(cur, user):
    if "maintenance.coupon" not in user["access"]:
        return {
            "error": "unauthorized access"
        }, 403

    expire_coupon(cur, user["key"])

    return {
    }, 200


@bp.get("/cron")
def cron():
    con, cur = db_open()

    cur.execute("""
        SELECT key FROM "user" WHERE email = %s;
    """, (os.environ["MAIL_USERNAME"],))
    user = cur.fetchone()

    delete_session(cur, user["key"])
    delete_anonymous(cur, user["key"])
    expire_coupon(cur, user["key"])

    db_close(con, cur)
    return {
    }, 200


@bp.post("/contact")
@session(False)
@rate_limit(20, 1)
def footer_send_email(_cur, _user):
    email_template = request.json.get("email_template")
    name = request.json.get("name")
    email = request.json.get("email")
    message = request.json.get("message")

    if not email_template:
        return {
            "error": "Invalid request"
        }, 422

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
        return {
            **error
        }, 422

    message = email_template.format(
        name=name, email=email, message=message)

    send_mail(
        os.environ["MAIL_USERNAME"],
        f"{name} from Meji",
        message
    )

    return {
    }, 200
