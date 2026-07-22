from flask import Blueprint, request

from ..storage import storage
from ..tools import log, rate_limit, session
from .get import blog_schema

bp = Blueprint("blog_file", __name__)


@bp.post("/blogs/<key>/file")
@session(True)
@rate_limit(20, 1)
@log("blog")
def add_file(cur, user, key):
    if "blog.edit_files" not in user["access"]:
        return {
            "error": "unauthorized access"
        }, 403

    cur.execute('SELECT * FROM blog WHERE key = %s;', (key,))
    blog = cur.fetchone()
    if not blog:
        return {
            "error": "Invalid request"
        }, 404

    if 'files' not in request.files:
        return {
            "error": "Invalid request"
        }, 422

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
        return {
            "error": error
        }, 422

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

    return {
        "blog": blog_schema(blog),
        "error": error,
        "log": {
            "entity_key": blog["key"],
            "misc": {
                "added": ", ".join(file_names),
                "error": error
            }
        }
    }, 200


@bp.put("/blogs/<key>/file")
@session(True)
@rate_limit(20, 1)
@log("blog")
def order_delete_file(cur, user, key):
    if "blog.edit_files" not in user["access"]:
        return {
            "error": "unauthorized access"
        }, 403

    cur.execute('SELECT * FROM blog WHERE key = %s;', (key,))
    blog = cur.fetchone()
    if not blog:
        return {
            "error": "Invalid request"
        }, 404

    files = request.json.get("files")
    if not files or type(files) is not list:
        return {
            "error": "Invalid request"
        }, 422

    files = [p.split("/")[-1] for p in files]
    if not all(x in blog["files"] for x in files):
        return {
            "error": "Invalid request"
        }, 422

    for x in blog["files"]:
        if x not in files:
            storage.delete(x, "blog")

    old_blog = blog
    cur.execute("""
        UPDATE blog SET files = %s WHERE key = %s RETURNING *;
    """, (files, blog["key"]))
    blog = cur.fetchone()

    return {
        "blog": blog_schema(blog),
        "log": {
            "entity_key": blog["key"],
            "misc": {
                "from": old_blog["files"],
                "to": blog["files"],
            }
        }
    }, 200
