import os
import re
from uuid import uuid4

from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash

from ..log import log
from ..postgres import db_close, db_open
from ..storage import storage
from ..tools import get_session, reserved_words
from .get import blog_schema, get_blogs, get_comments

bp = Blueprint("blog", __name__)


@bp.post("/blogs")
def add():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "blog.add" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 403,
            "error": "unauthorized access"
        })

    title = request.json.get("title")

    error = {}
    if not title:
        error["title"] = "This field is required"
    elif len(title) > 100:
        error["title"] = "This field cannot exceed 100 characters"
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    slug = re.sub('-+', '-', re.sub('[^a-zA-Z0-9]', '-', title.lower()))
    slug = slug[:100]
    cur.execute('SELECT * FROM blog WHERE slug = %s;', (slug,))
    blog = cur.fetchone()
    if blog or slug in reserved_words:
        slug = f"{slug[:89]}-{str(uuid4().hex)[:10]}"

    cur.execute("""
        INSERT INTO blog (title, slug, author_key)
        VALUES (%s, %s, %s) RETURNING *;
    """, (title, slug, user["key"],))
    blog = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="created blog",
        entity_type="blog",
        entity_key=blog["key"],
    )

    blogs = get_blogs(cur)

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "blog": blog_schema(blog),
        "blogs": blogs.json["blogs"],
        "total_page": blogs.json["total_page"]
    })


@bp.put("/blogs/<key>")
def edit(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute('SELECT * FROM blog WHERE key = %s;', (key,))
    blog = cur.fetchone()
    if not blog:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    error = {}

    title = blog["title"]
    slug = blog["slug"]
    date_created = blog["date_created"]
    description = blog["description"]
    content = blog["content"]
    tags = blog["tags"]
    author_key = blog["author_key"]
    status = blog["status"]

    if "title" in request.json:
        title = request.json.get("title", "").strip()
        if "blog.edit_title" not in user["access"]:
            error["title"] = "unauthorized access"
        elif not title:
            error["title"] = "This field is required"
        elif title == blog["title"]:
            error["title"] = "No changes were made"
        elif len(title) > 100:
            error["name"] = "This field cannot exceed 100 characters"
        else:
            slug = re.sub(
                '-+', '-', re.sub('[^a-zA-Z0-9]', '-', title.lower()))
            slug = slug[:100]
            cur.execute('SELECT * FROM blog WHERE key != %s AND slug = %s;',
                        (blog["key"], slug))
            slug_in_use = cur.fetchone()
            if (slug_in_use or slug in reserved_words):
                slug = f"{slug[:89]}-{str(uuid4().hex)[:10]}"

    if "date_created" in request.json:
        date_created = request.json.get("date_created")
        if "blog.edit_date" not in user["access"]:
            error["date_created"] = "unauthorized access"
        elif not date_created:
            error["date_created"] = "This field is required"
        elif date_created == blog["date_created"]:
            error["date_created"] = "No changes were made"

    if "description" in request.json:
        description = request.json.get("description", "").strip()
        if "blog.edit_description" not in user["access"]:
            error["description"] = "unauthorized access"
        elif description == blog["description"]:
            error["description"] = "No changes were made"
        elif len(description) > 500:
            error["description"] = "This field cannot exceed 500 characters"

    if "content" in request.json:
        content = request.json.get("content", "").strip()
        if "blog.edit_content" not in user["access"]:
            error["content"] = "unauthorized access"
        elif content == blog["content"]:
            error["content"] = "No changes were made"
        elif len(content) > 5000:
            error["content"] = "This field cannot exceed 5000 characters"

    if "tags" in request.json:
        tags = request.json.get("tags")
        if "blog.edit_tags" not in user["access"]:
            error["tags"] = "unauthorized access"
        elif type(tags) is not list:
            error["tags"] = "This field is required"
        elif set(tags) == set(blog["tags"]):
            error["tags"] = "No changes were made"

    if "author_key" in request.json:
        author_key = request.json.get("author_key")
        if "blog.edit_author" not in user["access"]:
            error["author_key"] = "unauthorized access"
        elif not author_key:
            error["author_key"] = "This field is required"
        else:
            if author_key == "default":
                author_key = os.environ["MAIL_USERNAME"]

            cur.execute("""
                SELECT key FROM "user"
                WHERE key::TEXT = %s OR email = %s OR username = %s;
            """, (author_key, author_key, author_key))
            author = cur.fetchone()

            if not author:
                error["author_key"] = "no user found"
            elif author["key"] == blog["author_key"]:
                error["author_key"] = "No changes were made"
            else:
                author_key = author["key"]

    if "status" in request.json:
        status = request.json.get("status")
        if "blog.edit_status" not in user["access"]:
            error["status"] = "unauthorized access"
        elif not status or status not in ['active', 'draft']:
            error["status"] = "Invalid request"
        elif status == blog["status"]:
            error["status"] = "No changes were made"
        elif status == "active" and not blog["photo"]:
            error["status"] = "no title photo"
        elif status == "active" and not blog["content"]:
            error["status"] = "no content"

    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    cur.execute("""
        UPDATE blog
        SET title = %s, slug = %s, date_created= %s, description= %s,
        content= %s, tags= %s, author_key= %s, status= %s, featured= %s
        WHERE key = %s RETURNING *;
    """, (
        title, slug, date_created, description, content, tags,
        author_key, status,
        blog["featured"] if status == "active" else 0,
        blog["key"]
    ))
    blog = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="edited blog",
        entity_type="blog",
        entity_key=blog["key"],
        misc=request.json
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "blog": blog_schema(blog)
    })


@bp.delete("/blogs/<key>")
def delete(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    password = request.json.GET("password")

    error = None
    if "blog.edit_status" not in user["access"]:
        error = "unauthorized access"
    elif not password:
        error = "This field is required"
    elif not check_password_hash(user["password"], password):
        error = "Incorrect password"
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": error
        })

    cur.execute('SELECT * FROM blog WHERE key = %s;', (key,))
    blog = cur.fetchone()
    if not blog:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute("""
        DELETE FROM blog WHERE key = %s;
    """, (blog["key"],))

    storage.delete(blog["photo"], "blog")
    for x in blog["files"]:
        storage.delete(x, "blog")

    log(
        cur=cur,
        user_key=user["key"],
        action="deleted blog",
        entity_type="blog",
        entity_key=blog["key"]
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/blogs/<key>/like")
def like(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    reaction = request.json.get("reaction")

    cur.execute("""SELECT * FROM blog WHERE key = %s;""", (key,))
    blog = cur.fetchone()
    if not blog or reaction not in ["like", "dislike"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute("""
        SELECT * FROM "like" WHERE user_key = %s AND blog_key = %s;
    """, (user["key"], blog["key"]))
    user_reaction = cur.fetchone()

    un = ""
    if not user_reaction:
        cur.execute("""
            INSERT INTO "like" (user_key, reaction, blog_key)
            VALUES (%s, %s, %s);
        """, (user["key"], reaction, key))
    elif user_reaction["reaction"] == reaction:
        un = "un"
        cur.execute("""DELETE FROM "like" WHERE key = %s;""",
                    (user_reaction["key"],))
    else:
        cur.execute("""
            UPDATE "like"
            SET date_created = now(), reaction = %s WHERE key = %s;
        """, (reaction, user_reaction["key"]))

    log(
        cur=cur,
        user_key=user["key"],
        action=f"{un}{reaction} blog",
        entity_type="blog",
        entity_key=blog["key"],
    )

    cur.execute("""
        SELECT
            COUNT(CASE WHEN user_key != %s
                AND reaction = 'like' THEN 1 END) AS others_like,
            COUNT(CASE WHEN user_key != %s
                AND reaction = 'dislike' THEN 1 END) AS others_dislike,
            MAX(CASE WHEN user_key = %s THEN reaction END) AS user_reaction
        FROM "like"
        WHERE blog_key = %s;
    """, (user["key"], user["key"], user["key"], blog["key"]))
    reactions = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        **reactions
    })


@bp.post("/blogs/<key>/comments")
def add_comment(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute("""
        SELECT * FROM blog WHERE slug = %s OR key = %s;
    """, (key, key))
    blog = cur.fetchone()
    if not blog:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    parent_key = request.json.get("parent_key")
    if parent_key:
        cur.execute("SELECT * FROM comment WHERE key = %s;", (parent_key,))
        parent = cur.fetchone()
        if not parent or parent["parent_key"] is not None:
            db_close(con, cur)
            return jsonify({
                "status": 400,
                "error": "Invalid request"
            })

    comment = request.json.get("comment", "").strip()
    error = {}
    if not comment:
        error["comment"] = "This field is required"
    elif len(comment) > 500:
        error["comment"] = "This field cannot exceed 500 characters"
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    cur.execute("""
        INSERT INTO comment (user_key, blog_key, comment, parent_key)
        VALUES (%s, %s, %s, %s) RETURNING *;
    """, (user["key"], blog["key"], comment, parent_key))
    comment = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="added comment",
        entity_type="blog",
        entity_key=blog["key"],
        misc={
            "comment_key": comment["key"]
        }
    )

    comments = get_comments(blog["key"], cur)
    db_close(con, cur)
    return comments
