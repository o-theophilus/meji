import os
import re

from flask import Blueprint, request

from ..log import log
from ..postgres import db_close, db_open
from ..tools import (check_code, generate_code, get_session, send_mail,
                     user_schema)

bp = Blueprint("user_email", __name__)


@bp.post("/user/email/1")
def email_1_old_email():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return session
    user = session["user"]

    email_template = request.json.get("email_template")
    if not email_template:
        db_close(con, cur)
        return {
            "status": 400,
            "error": "Invalid request"
        }, 400

    send_mail(
        user["email"],
        "Email Change Confirmation - Code",
        email_template.format(
            name=user["name"],
            code=generate_code(cur, user["key"], user["email"], "change email")
        )
    )

    db_close(con, cur)
    return {
        "status": 200
    }, 200


@bp.post("/user/email/2")
def email_2_old_code():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return session
    user = session["user"]

    error = check_code(cur, user["key"], user["email"], "code_1")
    if error:
        db_close(con, cur)
        return {
            "status": 400,
            "code_1": error
        }, 400

    db_close(con, cur)
    return {
        "status": 200
    }, 200


@bp.post("/user/email/3")
def email_3_new_email():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return session
    user = session["user"]

    error = check_code(cur, user["key"], user["email"], "code_1")
    if error:
        db_close(con, cur)
        return {
            "status": 400,
            "error": "Invalid request"
        }, 400

    email_template = request.json.get("email_template")
    if not email_template:
        db_close(con, cur)
        return {
            "status": 400,
            "error": "Invalid request"
        }, 400

    email = request.json.get("email")
    error = None
    if not email:
        error = "This field is required"
    elif not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
        error = "Invalid email address"
    if error:
        db_close(con, cur)
        return {
            "status": 400,
            "email": error
        }, 400

    if user["email"] == email:
        db_close(con, cur)
        return {
            "status": 400,
            "email": "please use a different email form your current email"
        }, 400

    cur.execute('SELECT * FROM "user" WHERE email = %s;', (email,))
    exist = cur.fetchone()
    if exist:
        db_close(con, cur)
        return {
            "status": 400,
            "email": "email is already in use"
        }, 400

    send_mail(
        email,
        "Email Change Confirmation - Code",
        email_template.format(
            name=user["name"],
            code=generate_code(
                cur, user["key"], email, "change email", False)
        )
    )

    db_close(con, cur)
    return {
        "status": 200
    }, 200


@bp.post("/user/email/4")
def email_4_new_code():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return session
    user = session["user"]

    error = check_code(cur, user["key"], user["email"], "code_1")
    if error:
        db_close(con, cur)
        return {
            "status": 400,
            "error": "Invalid request"
        }, 400

    email = request.json.get("email")
    if not email or not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
        db_close(con, cur)
        return {
            "status": 400,
            "error": "Invalid request"
        }, 400

    if user["email"] == email:
        db_close(con, cur)
        return {
            "status": 400,
            "error": "Invalid request"
        }, 400

    cur.execute('SELECT * FROM "user" WHERE email = %s;', (email,))
    exist = cur.fetchone()
    if exist:
        db_close(con, cur)
        return {
            "status": 400,
            "error": "Invalid request"
        }, 400

    error = check_code(cur, user["key"], email, "code_2")
    if error:
        db_close(con, cur)
        return {
            "status": 400,
            "error": "Invalid request"
        }, 400

    if user["email"] == os.environ["MAIL_USERNAME"]:
        cur.execute("DELETE FROM code WHERE user_key = %s;", (user["key"],))
        db_close(con, cur)
        return {
            "status": 400,
            "error": "LoL"
        }, 400

    log(
        cur=cur,
        user_key=user["key"],
        action="changed email",
        entity_type="user",
        entity_key=user["key"],
        misc={
            "from": user['email'],
            "to": email
        }
    )

    cur.execute("""
        UPDATE "user" SET email = %s WHERE key = %s RETURNING *;
    """, (email, user["key"]))
    user = cur.fetchone()

    cur.execute("DELETE FROM code WHERE user_key = %s;", (user["key"],))

    db_close(con, cur)
    return {
        "status": 200,
        "user": user_schema(user)
    }, 200
