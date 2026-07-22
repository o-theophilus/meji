from flask import Blueprint, request

from ..storage import storage
from ..tools import log, rate_limit, session
from .get import blog_schema

bp = Blueprint("blog_photo", __name__)


@bp.put("/blogs/<key>/photo")
@session(True)
@rate_limit(20, 1)
@log("blog")
def add(cur, user, key):
    if "blog.edit_photo" not in user["access"]:
        return {
            "error": "unauthorized access"
        }, 403

    cur.execute('SELECT * FROM blog WHERE key = %s;', (key,))
    blog = cur.fetchone()
    if not blog:
        return {
            "error": "Invalid request"
        }, 404

    if 'file' not in request.files:
        return {
            "error": "Invalid request"
        }, 422

    file = request.files["file"]
    if file.content_type not in ['image/jpeg', 'image/png']:
        return {
            "error": "invalid file"
        }, 422

    if blog["photo"]:
        storage.delete(blog["photo"], "blog")
    file_name = storage.save(file, blog["title"], "blog")

    old_blog = blog
    cur.execute("""
        UPDATE blog SET photo = %s WHERE key = %s RETURNING *;
    """, (file_name, blog["key"]))
    blog = cur.fetchone()

    return {
        "blog": blog_schema(blog),
        "log": {
            "entity_key": blog["key"],
            "misc": {
                "from": old_blog["photo"],
                "to": blog["photo"]
            }
        }
    }, 200


@bp.delete("/blogs/<key>/photo")
@session(True)
@rate_limit(20, 1)
@log("blog")
def delete(cur, user, key):
    if "blog.edit_photo" not in user["access"]:
        return {
            "error": "unauthorized access"
        }, 403

    cur.execute('SELECT * FROM blog WHERE key = %s;', (key,))
    blog = cur.fetchone()
    if not blog or not blog["photo"]:
        return {
            "error": "Invalid request"
        }, 404

    storage.delete(blog["photo"], "blog")

    old_blog = blog
    cur.execute("""
        UPDATE blog
        SET photo = NULL, status = 'draft'
        WHERE key = %s RETURNING *;
    """, (blog["key"],))
    blog = cur.fetchone()

    return {
        "blog": blog_schema(blog),
        "log": {
            "entity_key": blog["key"],
            "misc": {
                "photo": old_blog["photo"],
                "status": "draft"
            }
        }
    }, 200
