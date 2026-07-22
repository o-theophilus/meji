import os
import re

from flask import Blueprint, request

from ..tools import (check_code, generate_code, log, rate_limit, send_mail,
                     session, user_schema)

bp = Blueprint("user_email", __name__)


@bp.post("/user/email/1")
@session(True)
@rate_limit(20, 1)
def email_1_old_email(cur, user):
    if user["email"] == os.environ["MAIL_USERNAME"]:
        return {
            "error": "Invalid request"
        }, 403

    email_template = request.json.get("email_template")
    if not email_template:
        return {
            "error": "Invalid request"
        }, 422

    send_mail(
        user["email"],
        "Email Change Confirmation - Code",
        email_template.format(
            name=user["name"],
            code=generate_code(cur, user["key"], user["email"], "change email")
        )
    )

    return {
    }, 200


@bp.post("/user/email/2")
@session(True)
@rate_limit(20, 1)
def email_2_old_code(cur, user):
    error = check_code(cur, user["key"], user["email"], "code_1")
    if error:
        return {
            "code_1": error
        }, 422

    return {
    }, 200


@bp.post("/user/email/3")
@session(True)
@rate_limit(20, 1)
def email_3_new_email(cur, user):
    error = check_code(cur, user["key"], user["email"], "code_1")
    if error:
        return {
            "error": "Invalid request"
        }, 422

    email_template = request.json.get("email_template")
    if not email_template:
        return {
            "error": "Invalid request"
        }, 422

    email = request.json.get("email")
    error = None
    if not email:
        error = "This field is required"
    elif not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
        error = "Invalid email address"
    if error:
        return {
            "email": error
        }, 422

    if user["email"] == email:
        return {
            "email": "please use a different email form your current email"
        }, 422

    cur.execute('SELECT * FROM "user" WHERE email = %s;', (email,))
    exist = cur.fetchone()
    if exist:
        return {
            "email": "email is already in use"
        }, 422

    send_mail(
        email,
        "Email Change Confirmation - Code",
        email_template.format(
            name=user["name"],
            code=generate_code(
                cur, user["key"], email, "change email", False)
        )
    )

    return {
    }, 200


@bp.post("/user/email/4")
@session(True)
@rate_limit(20, 1)
@log("user")
def email_4_new_code(cur, user):
    if user["email"] == os.environ["MAIL_USERNAME"]:
        cur.execute("DELETE FROM code WHERE user_key = %s;", (user["key"],))
        return {
            "error": "Invalid request"
        }, 403

    error = check_code(cur, user["key"], user["email"], "code_1")
    if error:
        return {
            "error": "Invalid request"
        }, 422

    email = request.json.get("email")
    if not email or not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
        return {
            "error": "Invalid request"
        }, 422

    if user["email"] == email:
        return {
            "error": "Invalid request"
        }, 422

    cur.execute('SELECT * FROM "user" WHERE email = %s;', (email,))
    exist = cur.fetchone()
    if exist:
        return {
            "error": "Invalid request"
        }, 422

    error = check_code(cur, user["key"], email, "code_2")
    if error:
        return {
            "error": "Invalid request"
        }, 422

    previous = user
    cur.execute("""
        UPDATE "user" SET email = %s WHERE key = %s RETURNING *;
    """, (email, user["key"]))
    user = cur.fetchone()

    cur.execute("DELETE FROM code WHERE user_key = %s;", (user["key"],))

    return {
        "user": user_schema(user),
        "log": {
            "misc": {
                "from": previous['email'],
                "to": user['email'],
            }

        }
    }, 200
