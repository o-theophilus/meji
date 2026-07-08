from flask import Blueprint, request

from ..tools import log, rate_limit, session
from .get import many_blogs, many_items

bp = Blueprint("comment", __name__)


@bp.post("/comments/blogs/<key>")
@session(True)
@rate_limit(20, 1)
@log("comment")
def add_blog_comment(cur, user, key):
    cur.execute("""
        SELECT * FROM blog WHERE slug = %s OR key = %s;
    """, (key, key))
    if not cur.fetchone():
        return {
            "status": 404,
            "error": "Invalid request"
        }, 404

    parent_key = request.json.get("parent_key")
    comment = request.json.get("comment", "").strip()

    if parent_key:
        cur.execute("SELECT * FROM comment WHERE key = %s;", (parent_key,))
        parent = cur.fetchone()
        if not parent or parent["parent_key"] is not None:
            return {
                "status": 404,
                "error": "Invalid request"
            }, 404

    error = {}
    if not comment:
        error["comment"] = "This field is required"
    elif len(comment) > 500:
        error["comment"] = "This field cannot exceed 500 characters"
    if error:
        return {
            "status": 422,
            **error
        }, 422

    cur.execute("""
        INSERT INTO comment (user_key, blog_key, comment, parent_key)
        VALUES (%s, %s, %s, %s) RETURNING *;
    """, (user["key"], key, comment, parent_key))
    comment = cur.fetchone()

    blogs = many_blogs(cur, key, user["key"])

    return {
        "status": 200,
        "comments": blogs["comments"],
        "total_comment": blogs["total_comment"],
        "total_page": blogs["total_page"],
        "log": {
            "entity_key": comment["key"],
            "misc": {
                "entity_key": key,
                "entity_type": "blog"
            }
        }
    }, 200


@bp.post("/comments/items/<key>")
@session(True)
@rate_limit(20, 1)
@log("comment")
def add_item_comment(cur, user, key):
    cur.execute("""
        SELECT * FROM item WHERE slug = %s OR key = %s;
    """, (key, key))
    if not cur.fetchone():
        return {
            "status": 404,
            "error": "Invalid request"
        }, 404

    parent_key = request.json.get("parent_key")
    if parent_key:
        if "comment.reply" not in user["access"]:
            return {
                "status": 403,
                "error": "unauthorized access"
            }, 403

        cur.execute("SELECT * FROM comment WHERE key = %s;", (parent_key,))
        if not cur.fetchone():
            return {
                "status": 404,
                "error": "Invalid request"
            }, 404

    cur.execute("""
        WITH purchase_check AS (
            SELECT EXISTS (
                SELECT 1
                FROM "order" o
                LEFT JOIN order_item oi ON o.key = oi.order_key
                LEFT JOIN item_version iv ON oi.item_version_key = iv.key
                WHERE
                    o.user_key = %s
                    AND o.status = 'delivered'
                    AND iv.item_key = %s
            ) AS has_purchased
        ),

        comment_check AS (
            SELECT EXISTS (
                SELECT 1
                FROM comment
                WHERE
                    comment.user_key = %s
                    AND comment.item_key = %s
                    AND comment.parent_key IS NULL
            ) AS has_commented
        )

        SELECT
            purchase_check.has_purchased,
            purchase_check.has_purchased AND NOT comment_check.has_commented
                AS can_comment
        FROM purchase_check, comment_check
    """, (user["key"], key, user["key"], key))
    user_comment_info = cur.fetchone()

    if not user_comment_info["can_comment"]:
        return {
            "status": 403,
            "error": "Invalid request"
        }, 403

    rating = request.json.get("rating", 0)
    comment = request.json.get("comment", "").strip()
    error = {}
    if rating not in [1, 2, 3, 4, 5]:
        error["rating"] = "This field is required"

    if not comment:
        error["comment"] = "This field is required"
    elif len(comment) > 500:
        error["comment"] = "This field cannot exceed 500 characters"
    if error:
        return {
            "status": 422,
            **error
        }, 422

    cur.execute("""
        INSERT INTO comment (user_key, item_key, rating,
            comment, parent_key)
        VALUES (%s, %s, %s, %s, %s) RETURNING *;
    """, (user["key"], key, rating, comment, parent_key))
    comment = cur.fetchone()

    items = many_items(cur, key, user["key"])

    return {
        "status": 200,
        "comments": items["comments"],
        "total_page": items["total_page"],
        "total_comment": items["total_comment"],
        "ratings": items["ratings"],
        "has_purchased": items["has_purchased"],
        "can_comment": items["can_comment"],
        "log": {
            "entity_key": comment["key"],
            "misc": {
                "entity_key": key,
                "entity_type": "item"
            }
        }
    }, 200


@bp.delete("/comments/<key>")
@session(True)
@rate_limit(20, 1)
@log("comment")
def delete(cur, user, key):
    cur.execute("""SELECT * FROM comment WHERE key = %s;""", (key,))
    comment = cur.fetchone()
    if not comment:
        return {
            "status": 404,
            "error": "Invalid request"
        }, 404

    _comment = request.json.get("comment", "").strip()
    misc = {}

    if comment["user_key"] != user["key"]:
        if "comment.delete_others" not in user["access"]:
            return {
                "status": 403,
                "error": "unauthorized access"
            }, 403

        error = {}
        if not _comment:
            error["comment"] = "This field is required"
        elif len(_comment) > 500:
            error["comment"] = "This field cannot exceed 500 characters"
        if error:
            return {
                "status": 422,
                **error
            }, 422

        misc["comment"] = _comment

    cur.execute("DELETE FROM comment WHERE key = %s;", (comment["key"],))

    entity = {}
    if comment["entity_key"] == "item":
        items = many_items(cur, key, user["key"])
        entity["comments"] = items["comments"]
        entity["total_comment"] = items["total_comment"]
        entity["total_page"] = items["total_page"]
        entity["ratings"] = items["ratings"]
        entity["has_purchased"] = items["has_purchased"]
        entity["can_comment"] = items["can_comment"]
    else:
        blogs = many_blogs(cur, key, user["key"])
        entity["comments"] = blogs["comments"]
        entity["total_comment"] = blogs["total_comment"]
        entity["total_page"] = blogs["total_page"]

    return {
        "status": 200,
        **entity,
        "log": {
            "entity_key": comment["key"],
            "misc": misc
        }
    }, 200
