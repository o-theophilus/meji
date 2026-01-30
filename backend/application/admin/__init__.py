from flask import Blueprint, jsonify, request
import os
from ..postgres import db_open, db_close
from ..log import log
from uuid import uuid4
from ..tools import get_session, user_schema, access_pass
from werkzeug.security import check_password_hash


bp = Blueprint("admin", __name__)


@bp.put("/admin/action/<key>")
def perform_action(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    me = session["user"]

    cur.execute("""SELECT * FROM "user" WHERE key = %s;""", (key,))
    user = cur.fetchone()
    if (
        not user
        or user["key"] == me["key"]
        or user["key"] != "active"
        or user["email"] == os.environ["MAIL_USERNAME"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    _actions = request.json.get("actions")
    note = request.json.get("note")

    error = {}
    if not _actions or type(_actions) is not list or _actions == []:
        error["actions"] = "select action"
    if not note:
        error["note"] = "This field is required"
    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    actions = []
    error = None
    if "reset_name" in _actions:
        if "user:reset_name" in me["access"]:
            actions.append("name")
        else:
            error = "unauthorized access"
    if "reset_username" in _actions:
        if "user:reset_username" in me["access"]:
            actions.append("username")
        else:
            error = "unauthorized access"
    if "reset_photo" in _actions:
        if "user:reset_photo" in me["access"]:
            actions.append("photo")
        else:
            error = "unauthorized access"

    if actions == []:
        error = "Invalid request"
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": error
        })

    _key = uuid4().hex
    cur.execute("""
        UPDATE "user" SET name = %s, username = %s, photo = %s
        WHERE key = %s RETURNING *;
    """, (
        f"user {_key[-8:]}" if "name" in actions else user["name"],
        f"user_{_key[:8]}" if "username" in actions else user["username"],
        None if "photo" in actions else user["photo"],
        user["key"]
    ))
    user = cur.fetchone()

    log(
        cur=cur,
        user_key=me["key"],
        action="reset user details",
        entity_type="user",
        entity_key=user["key"],
        misc={
            "field(s)": ", ".join(actions),
            "note": note
        }
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })


@bp.get("/admin/access")
@bp.get("/admin/access/<search>")
def get_access(search=None):
    _all = [f"{x}:{y[0]}" for x in access_pass for y in access_pass[x]]
    if search:
        _all = [x for x in _all if x.find(search) != -1]

    return jsonify({
        "status": 200,
        "access": _all
    })


@bp.put("/admin/access/<key>")
def set_access(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    me = session["user"]

    if "user:set_access" not in me["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute('SELECT * FROM "user" WHERE key = %s;', (key,))
    user = cur.fetchone()

    access = request.json.get("access")

    if (
        not user
        or not access
        or type(access) is not list
        or user["key"] == me["key"]
        or user["status"] != "active"
        or user["email"] == os.environ["MAIL_USERNAME"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    password = request.json.get("password")

    error = None
    if not password:
        error = "This field is required"
    elif not check_password_hash(me["password"], password):
        error = "incorrect password"
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "password": error
        })

    cur.execute("""
        UPDATE "user" SET access = %s WHERE key = %s RETURNING *;
    """, (access, user["key"]))
    user = cur.fetchone()

    log(
        cur=cur,
        user_key=me["key"],
        action="changed admin access",
        entity_key=user["key"],
        entity_type="user",
        misc={"from": user["access"], "to": access}
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })
