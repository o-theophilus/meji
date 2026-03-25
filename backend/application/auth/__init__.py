import os
import re
from uuid import uuid4

from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from ..cart.get import get_cart_items
from ..item.get import get_item_tags
from ..blog.get import get_blog_tags
from ..log import log
from ..postgres import db_close, db_open
from ..storage import storage
from ..tools import (access_pass, check_code, generate_code, get_session,
                     reserved_words, send_mail, user_schema)
from ..user.get import get_user_like

bp = Blueprint("auth", __name__)


def anon(cur):
    key = uuid4().hex
    cur.execute("""
        INSERT INTO "user" (name, username, email, password)
        VALUES (%s, %s, %s, %s)
        RETURNING *;
    """, (
        f"user {key[-8:]}",
        f"user_{key[:8]}",
        uuid4().hex,
        generate_password_hash(uuid4().hex, method="scrypt")))
    return cur.fetchone()


def create_session(cur, user_key, login=False, remember=False):
    cur.execute("""
        INSERT INTO session (user_key, login, remember) VALUES (%s, %s, %s)
        RETURNING *;
    """, (user_key, login, remember))

    return cur.fetchone()["key"]


def copy_like_n_cart(cur, user_key, anon_key):
    cur.execute("""
        INSERT INTO "like" (user_key, entity_key, entity_type)
        SELECT %s, entity_key, 'item'
        FROM "like"
        WHERE user_key = %s AND entity_type = 'item'
        ON CONFLICT DO NOTHING;
    """, (user_key, anon_key))
    cur.execute("""
        DELETE FROM "like"
        WHERE user_key = %s;
    """, (anon_key,))

    cur.execute("""
        SELECT * FROM "order"
        WHERE user_key = %s AND status = 'cart';
    """, (user_key,))
    in_cart = cur.fetchone()
    if not in_cart:
        cur.execute("""
            INSERT INTO "order" (user_key) VALUES (%s) RETURNING *
        ;""", (user_key,))
        in_cart = cur.fetchone()

    cur.execute("""
        UPDATE order_item u
        SET quantity = a.quantity
        FROM order_item a
        JOIN "order" ao ON ao.key = a.order_key
        WHERE ao.user_key = %s
        AND ao.status = 'cart'
        AND u.order_key = %s
        AND u.item_key = a.item_key
        AND u.variation = a.variation
    """, (anon_key, in_cart["key"]))
    cur.execute("""
        UPDATE order_item a
        SET order_key = %s
        FROM "order" ao
        WHERE ao.key = a.order_key
        AND ao.user_key = %s
        AND ao.status = 'cart'
        AND NOT EXISTS (
            SELECT 1
            FROM order_item u
            WHERE u.order_key = %s
            AND u.item_key = a.item_key
            AND u.variation = a.variation
        )
    """, (in_cart["key"], anon_key, in_cart["key"]))
    cur.execute("""
        DELETE FROM "order"
        WHERE user_key = %s AND status = 'cart'
    """, (anon_key,))


@bp.get("/admin/default")
def default_admin():
    con, cur = db_open()
    email = os.environ["MAIL_USERNAME"]

    cur.execute('SELECT * FROM "user" WHERE email = %s;', (email,))
    if not cur.fetchone():
        cur.execute("""
                INSERT INTO "user"
                (status, name, username, email, password, access)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING *;
            """, (
            "active",
            "Theophilus",
            "omni",
            email,
            generate_password_hash(
                os.environ["MAIL_PASSWORD"], method="scrypt"),
            [f"{x}:{y[0]}" for x in access_pass for y in access_pass[x]]
        ))
        user = cur.fetchone()

        log(
            cur=cur,
            user_key=user["key"],
            action="created",
            entity_type="user",
            entity_key=user["key"]
        )
        log(
            cur=cur,
            user_key=user["key"],
            action="signedup",
            entity_type="user",
            entity_key=user["key"]
        )
        log(
            cur=cur,
            user_key=user["key"],
            action="activated account",
            entity_type="user",
            entity_key=user["key"]
        )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/init")
def init():
    con, cur = db_open()

    session = get_session(cur)

    cart_items = []
    if session["status"] == 200:
        user = session["user"]
        token = request.headers.get("Authorization")
        login = session["login"]
        cart_items = get_cart_items(cur).json["items"]

    else:
        user = anon(cur)
        token = create_session(cur, user["key"])
        login = False

        log(
            cur=cur,
            user_key=user["key"],
            action="created",
            entity_type="user",
            entity_key=user["key"]
        )

    likes = get_user_like(cur, user["key"])
    item_tags = get_item_tags(cur)
    blog_tags = get_blog_tags(cur)

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user),
        "token": token,
        "login": login,
        "likes": likes,
        "cart_items": cart_items,
        "item_tags": item_tags,
        "blog_tags": blog_tags
    })


@bp.post("/signup")
def signup():
    con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    name = ' '.join(request.json.get("name", "").strip().split())
    email = request.json.get("email", "").strip()
    password = request.json.get("password")
    confirm_password = request.json.get("confirm_password")
    email_template = request.json.get("email_template")

    if session["login"] or not email_template:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    error = {}

    if not name:
        error["name"] = "This field is required"
    elif len(name) > 100:
        error["name"] = "This field cannot exceed 100 characters"

    email_user = None
    if not email:
        error["email"] = "This field is required"
    elif not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
        error["email"] = "Invalid email address"
    elif len(email) > 255:
        error["email"] = "This field cannot exceed 255 characters"
    else:
        cur.execute('SELECT * FROM "user" WHERE email = %s;', (email,))
        email_user = cur.fetchone()
        if email_user and email_user["status"] != "signedup":
            error["email"] = "Email already in use"

    if not password:
        error["password"] = "This field is required"
    elif (
        not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[^\s]+$", password)
        or len(password) not in range(8, 19)
    ):
        error["password"] = """Password must include at least 1 lowercase
        letter, 1 uppercase letter, 1 number and must contain 8 - 18
        characters"""

    if not confirm_password:
        error["confirm_password"] = "This field is required"
    elif password and confirm_password != password:
        error["confirm_password"] = """Password and confirm password does not
        match"""

    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    if email_user:
        user = email_user
    elif user["status"] != "anonymous":
        user = anon(cur)

    username = re.sub(
        '-+', '-', re.sub('[^a-zA-Z0-9]', '-', name.lower()))[:20]
    cur.execute(
        """SELECT * FROM "user" WHERE email != %s AND username = %s;""",
        (email, username))
    if cur.fetchone() or username in reserved_words:
        username = f"{username[:11]}-{str(uuid4().hex)[:8]}"

    cur.execute("""
        UPDATE "user"
        SET name = %s, username = %s, email = %s,
            password = %s, status = 'signedup'
        WHERE key = %s
        RETURNING *;
    """, (
        name, username, email,
        generate_password_hash(password, method="scrypt"),
        user["key"]
    ))
    user = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="signedup",
        entity_type="user",
        entity_key=user["key"]
    )

    send_mail(
        user["email"],
        "Welcome to my portfolio website! Complete your signup with this Code",
        email_template.format(
            name=user["name"],
            code=generate_code(cur, user["key"], user["email"], "signup")
        )
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/confirm")
def confirm():
    con, cur = db_open()

    email = request.json.get("email")

    error = None
    if not email or not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute('SELECT * FROM "user" WHERE email = %s;', (email,))
    user = cur.fetchone()
    if not user or user["status"] != 'signedup':
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    error = check_code(cur, user["key"], user["email"])
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": error
        })

    cur.execute("""
        UPDATE "user" SET status = 'active' WHERE key = %s;
    """, (user["key"],))

    log(
        cur=cur,
        user_key=user["key"],
        action="activated account",
        entity_type="user",
        entity_key=user["key"]
    )

    cur.execute("DELETE FROM code WHERE user_key = %s;", (user["key"],))

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/login")
def login():
    con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    anon_user = session["user"]

    email_template = request.json.get("email_template")
    if session["login"] or not email_template:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    email = request.json.get("email")
    password = request.json.get("password")
    remember = request.json.get("remember", False)

    error = {}
    if not email:
        error["email"] = "This field is required"
    if not password:
        error["password"] = "This field is required"
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    user = None
    if anon_user["email"] == email or anon_user["username"] == email:
        user = anon_user
    else:
        cur.execute("""
            SELECT * FROM "user" WHERE email = %s OR username = %s;
        """, (email, email))
        user = cur.fetchone()

    if (
        not user
        or user["status"] not in ['signedup', 'active']
        or not check_password_hash(user["password"], password)
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "your email or password is incorrect"
        })

    cur.execute("SELECT * FROM block WHERE user_key = %s;", (user["key"],))
    if cur.fetchone():
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "account blocked"
        })

    if user["status"] == "signedup":
        send_mail(
            user["email"],
            "Welcome to my portfolio website! \
            Complete your signup with this Code",
            email_template.format(
                name=user["name"],
                code=generate_code(
                    cur, user["key"], user["email"], "login")
            )
        )
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "not active"
        })

    cur.execute("""
        DELETE FROM session WHERE user_key = %s;
    """, (anon_user["key"],))

    if anon_user["status"] == "anonymous":
        copy_like_n_cart(cur, user["key"], anon_user["key"])
        cur.execute("""DELETE FROM "user" WHERE key = %s;""",
                    (anon_user["key"],))

    token = create_session(cur, user["key"], True, remember)

    log(
        cur=cur,
        user_key=user["key"],
        action="logged in",
        entity_type="user",
        entity_key=user["key"],
        misc={
            "type": "user",
            "key": anon_user["key"]
        }
    )
    log(
        cur=cur,
        user_key=anon_user["key"],
        action="logged out",
        entity_type="user",
        entity_key=anon_user["key"],
        misc={
            "entity_type": "user",
            "entity_key": user["key"],
        }
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "token": token
    })


@bp.delete("/logout")
def logout():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]
    anon_user = anon(cur)

    cur.execute("""
        DELETE FROM session WHERE user_key = %s;
    """, (user["key"],))

    token = create_session(cur, anon_user["key"])

    log(
        cur=cur,
        user_key=user["key"],
        action="logged out",
        entity_type="user",
        entity_key=user["key"],
        misc={
            "entity_type": "user",
            "entity_key": anon_user["key"],
        }
    )
    log(
        cur=cur,
        user_key=anon_user["key"],
        action="created",
        entity_type="user",
        entity_key=anon_user["key"],
        misc={
            "entity_type": "user",
            "entity_key": user["key"],
        }
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(anon_user),
        "token": token
    })


@bp.delete("/deactivate")
def deactivate():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    password = request.json.get("password")
    comment = request.json.get("comment")
    email_template = request.json.get("email_template")

    if not email_template:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    error = {}
    if not password:
        error["password"] = "This field is required"
    elif not check_password_hash(user["password"], password):
        error["password"] = "Incorrect password"
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    cur.execute(
        """
            UPDATE block
            SET admin_key = (SELECT key FROM "user" WHERE email = %s)
            WHERE admin_key = %s;
        """, (os.environ["MAIL_USERNAME"], user["key"]))
    cur.execute("""DELETE FROM "user" WHERE key = %s;""", (user["key"],))
    # TODO: delete comments -> likes / reports

    storage.delete(user["photo"], "user")
    anon_user = anon(cur)
    token = create_session(cur, anon_user["key"])

    log(
        cur=cur,
        user_key=user["key"],
        action="deleted account",
        entity_type="user",
        entity_key=user["key"],
        misc={"comment": comment} if comment else {}
    )
    log(
        cur=cur,
        user_key=anon_user["key"],
        action="created",
        entity_type="user",
        entity_key=anon_user["key"],
        misc={
            "entity_type": "user",
            "entity_key": user["key"],
        }
    )

    send_mail(
        user["email"],
        "You've Successfully Deleted Your Account",
        email_template.format(name=user["name"])
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(anon_user),
        "token": token
    })
