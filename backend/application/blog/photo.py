from flask import Blueprint, request

from ..log import log
from ..postgres import db_close, db_open
from ..storage import storage
from ..tools import get_session
from .get import blog_schema

bp = Blueprint("blog_photo", __name__)


@bp.put("/blogs/<key>/photo")
def add_photo(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return session
    user = session["user"]

    if "blog.edit_photo" not in user["access"]:
        db_close(con, cur)
        return {
            "status": 403,
            "error": "unauthorized access"
        }, 403

    cur.execute('SELECT * FROM blog WHERE key = %s;', (key,))
    blog = cur.fetchone()
    if 'file' not in request.files or not blog:
        db_close(con, cur)
        return {
            "status": 400,
            "error": "Invalid request"
        }, 400

    file = request.files["file"]
    if file.content_type not in ['image/jpeg', 'image/png']:
        db_close(con, cur)
        return {
            "status": 400,
            "error": "invalid file"
        }, 400

    old_photo = None
    if blog["photo"]:
        old_photo = blog["photo"]
        storage.delete(blog["photo"], "blog")

    file_name = storage.save(file, blog["title"], "blog")

    cur.execute("""
        UPDATE blog
        SET photo = %s
        WHERE key = %s
        RETURNING *;
    """, (
        file_name,
        blog["key"]
    ))
    blog = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="updated blog photo",
        entity_type="blog",
        entity_key=blog["key"],
        misc={
            "from": old_photo,
            "to": file_name
        }
    )

    db_close(con, cur)
    return {
        "status": 200,
        "blog": blog_schema(blog)
    }, 200


@bp.delete("/blogs/<key>/photo")
def delete_photo(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return session
    user = session["user"]

    if "blog.edit_photo" not in user["access"]:
        db_close(con, cur)
        return {
            "status": 403,
            "error": "unauthorized access"
        }, 403

    cur.execute('SELECT * FROM blog WHERE key = %s;', (key,))
    blog = cur.fetchone()
    if not blog or not blog["photo"]:
        db_close(con, cur)
        return {
            "status": 400,
            "error": "Invalid request"
        }, 400

    storage.delete(blog["photo"], "blog")

    log(
        cur=cur,
        user_key=user["key"],
        action="deleted blog photo",
        entity_type="blog",
        entity_key=blog["key"],
        misc={"photo": blog["photo"]}
    )

    if blog["status"] == "active":
        log(
            cur=cur,
            user_key=user["key"],
            action="edited blog",
            entity_type="blog",
            entity_key=blog["key"],
            misc={"status": "draft"}
        )

    cur.execute("""
        UPDATE blog
        SET photo = NULL, status = %s
        WHERE key = %s
        RETURNING *;
    """, (
        "draft" if blog["status"] == "active" else blog["status"],
        blog["key"]
    ))
    blog = cur.fetchone()

    db_close(con, cur)
    return {
        "status": 200,
        "blog": blog_schema(blog)
    }, 200
