from flask import Blueprint, request

from ..log import log
from ..postgres import db_close, db_open
from ..storage import storage
from ..tools import get_session
from .get import blog_schema

bp = Blueprint("blog_file", __name__)


@bp.post("/blogs/<key>/file")
def add_file(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return session
    user = session["user"]

    if "blog.edit_files" not in user["access"]:
        db_close(con, cur)
        return {
            "status": 403,
            "error": "unauthorized access"
        }, 403

    cur.execute('SELECT * FROM blog WHERE key = %s;', (key,))
    blog = cur.fetchone()
    if 'files' not in request.files or not blog:
        db_close(con, cur)
        return {
            "status": 400,
            "error": "Invalid request"
        }, 400

    error = ""
    files = []

    for x in request.files.getlist("files"):
        err = ""
        if x.content_type not in [
                'image/jpeg', 'image/png', 'application/pdf']:
            err = f"{x.filename} => invalid file"
        elif len(blog["files"]) + len(
                files) >= blog["content"].count("@[file]"):
            err = f"{x.filename} => excess file"

        if err:
            error = f"{error}, {err}" if error else err
        else:
            files.append(x)

    if files == []:
        if not error:
            error = "no file"
        db_close(con, cur)
        return {
            "status": 400,
            "error": error
        }, 400

    file_names = []
    for x in files:
        filename = storage.save(x, blog["title"], "blog")
        file_names.append(filename)

    cur.execute("""
        UPDATE blog
        SET files = %s
        WHERE key = %s
        RETURNING *;
    """, (
        blog["files"] + file_names,
        blog["key"]
    ))
    blog = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="added file to blog",
        entity_type="blog",
        entity_key=blog["key"],
        misc={
            "added": ", ".join(file_names),
            "error": error
        }
    )

    db_close(con, cur)
    return {
        "status": 200,
        "blog": blog_schema(blog),
        "error": error
    }, 200


@bp.put("/blogs/<key>/file")
def order_delete_file(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return session
    user = session["user"]

    if "blog.edit_files" not in user["access"]:
        db_close(con, cur)
        return {
            "status": 403,
            "error": "unauthorized access"
        }, 403

    cur.execute('SELECT * FROM blog WHERE key = %s;', (key,))
    blog = cur.fetchone()

    files = request.json.get("files")

    if not blog or not files or type(files) is not list:
        db_close(con, cur)
        return {
            "status": 400,
            "error": "Invalid request"
        }, 400

    files = [p.split("/")[-1] for p in files]

    if not all(x in blog["files"] for x in files):
        db_close(con, cur)
        return {
            "status": 400,
            "error": "Invalid request"
        }, 400

    for x in blog["files"]:
        if x not in files:
            storage.delete(x, "blog")

    log(
        cur=cur,
        user_key=user["key"],
        action="edited blog files",
        entity_type="blog",
        entity_key=blog["key"],
        misc={
            "from": blog["files"],
            "to": files
        }
    )

    cur.execute("""
        UPDATE blog
        SET files = %s
        WHERE key = %s
        RETURNING *;
    """, (
        files,
        blog["key"]
    ))
    blog = cur.fetchone()

    db_close(con, cur)
    return {
        "status": 200,
        "blog": blog_schema(blog)
    }, 200
