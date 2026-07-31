import os
import re
from math import ceil

from flask import Blueprint, request

from ..comment.get import many_blog_comments
from ..tools import session

bp = Blueprint("blog_get", __name__)


def blog_schema(i):
    i["photo"] = (f"{request.host_url}photo/blog/{i['photo']}"
                  if i['photo'] else None)
    i["files"] = [f"{request.host_url}photo/blog/{x}" for x in i[
        "files"]]
    return i


def get_blog_tags(cur):
    cur.execute("SELECT tags FROM blog WHERE status = 'active';")
    temp = cur.fetchall()

    tags = []
    for x in temp:
        tags += x["tags"]

    tags_count = []
    unique_tags = []
    for x in tags:
        if x not in unique_tags:
            unique_tags.append(x)
            tags_count.append({
                "tag":  x,
                "count":  tags.count(x)
            })

    tags_count = sorted(tags_count, key=lambda d: d["count"], reverse=True)
    return [x["tag"] for x in tags_count]


@bp.get("/blogs/<key>")
@session(False)
def get(cur, user, key):
    cur.execute("""
        SELECT * FROM blog WHERE slug = %s OR key::TEXT = %s
    """, (key, key))
    blog = cur.fetchone()

    if not blog:
        return {
            "error": "Oops! The blog you're looking for doesn't exist"
        }, 404

    if (
        blog["status"] != "active"
        and "blog.add" not in user["access"]
        and "blog.edit_status" not in user["access"]
    ):
        return {
            "error": "unauthorized access"
        }, 403

    return {
        "blog": blog_schema(blog)
    }, 200


def many(cur, user):
    order_by = {
        'latest': 'blog.date_created',
        'oldest': 'blog.date_created',
        'title (a-z)': 'blog.title',
        'title (z-a)': 'blog.title',
        'comment': "COALESCE(c._count, 0)",
        'like': 'COALESCE(l."like", 0) - COALESCE(l.dislike, 0)',
        'view': "COALESCE(v._count, 0)"
    }

    order_dir = {
        'latest': 'DESC',
        'oldest': 'ASC',
        'title (a-z)': 'ASC',
        'title (z-a)': 'DESC',
        'comment': 'DESC',
        'view': 'DESC',
        'like': 'DESC'
    }

    search_params = {
        "search": "",
        "status": "active",
        "tag": "",
        "order": "latest",
        "page_no": 1,
        "page_size": 24
    }
    search = request.args.get("search", search_params["search"]).strip()
    status = request.args.get("status", search_params["status"])
    tag = request.args.get("tag", search_params["tag"])
    order = request.args.get("order", search_params["order"])
    page_no = int(request.args.get("page_no", search_params["page_no"]))
    page_size = int(request.args.get("page_size", search_params["page_size"]))
    page_size = min(page_size, 100)

    if (
        "blog.edit_status" not in user["access"]
        and "blog.add" not in user["access"]
    ):
        status = "active"

    params = [status, search, f"%{search}%"]

    op = "&&"
    tag_query = ""
    if tag[-4:] == ":all":
        op = "@>"
        tag = tag[:-4]
    tags = tag.split(",") if tag else []
    if tags != []:
        tag_query = f"AND cardinality(blog.tags) > 0 AND blog.tags {op} %s"
        params.append(tags)

    cur.execute(f"""
        SELECT
            blog.*,
            jsonb_build_object(
                'comment', COALESCE(c._count, 0),
                'like', COALESCE(l."like", 0) - COALESCE(l.dislike, 0),
                'view', COALESCE(v._count, 0),
                'share', COALESCE(s._count, 0)
            ) AS engagement

        FROM blog

        LEFT JOIN (
            SELECT blog_key, COUNT(*) AS _count
            FROM comment
            GROUP BY blog_key
        ) c ON c.blog_key = blog.key

        LEFT JOIN (
            SELECT blog_key,
                COUNT(*) FILTER (WHERE reaction = 'like') AS "like",
                COUNT(*) FILTER (WHERE reaction = 'dislike') AS dislike
            FROM "like"
            GROUP BY blog_key
        ) l ON l.blog_key = blog.key

        LEFT JOIN (
            SELECT entity_key, COUNT(DISTINCT user_key) AS _count
            FROM log
            WHERE entity_type = 'blog'
                AND action = 'viewed blog'
            GROUP BY entity_key
        ) v ON v.entity_key = blog.key::TEXT

        LEFT JOIN (
            SELECT entity_key, COUNT(DISTINCT user_key) AS _count
            FROM log
            WHERE entity_type = 'blog'
                AND action = 'shared'
            GROUP BY entity_key
        ) s ON s.entity_key = blog.key::TEXT

        WHERE blog.status = %s
            AND (%s = '' OR blog.title ILIKE %s) {tag_query}
        ORDER BY {order_by[order]} {order_dir[order]}, blog.key DESC
        LIMIT %s OFFSET %s;
    """, (*params, page_size, (page_no - 1) * page_size))
    blogs = cur.fetchall()

    cur.execute(f"""
        SELECT COUNT(*) FROM blog
        WHERE blog.status = %s
            AND (%s = '' OR blog.title ILIKE %s) {tag_query};
    """, (*params,))
    total_page = cur.fetchone()["count"]

    return {
        "blogs": [blog_schema(x) for x in blogs],
        "order_by": list(order_by.keys()),
        "status": ['active', 'draft'],
        "total_page": ceil(total_page / page_size),
        "searchParams": search_params
    }


@bp.get("/blogs")
@session(False)
def _many(cur, user):
    return many(cur, user), 200


def get_engagement(cur, key, user_key):
    cur.execute("""
        SELECT
            COUNT(CASE WHEN user_key != %s
                AND reaction = 'like' THEN 1 END) AS others_like,
            COUNT(CASE WHEN user_key != %s
                AND reaction = 'dislike' THEN 1 END) AS others_dislike,
            MAX(CASE WHEN user_key = %s THEN reaction END) AS user_reaction
        FROM "like"
        WHERE blog_key = %s;
    """, (user_key, user_key, user_key, key))
    reactions = cur.fetchone()

    cur.execute("""
        SELECT COUNT(*) FROM comment
        WHERE blog_key = %s;
    """, (key,))
    comment_count = cur.fetchone()["count"]

    cur.execute("""
        SELECT COUNT(DISTINCT user_key) FROM log
        WHERE entity_type = 'blog' AND action = 'viewed blog'
        AND entity_key = %s;
    """, (key,))
    view_count = cur.fetchone()["count"]

    cur.execute("""
        SELECT COUNT(*) FROM log
        WHERE entity_type = 'blog' AND action = 'shared' AND entity_key = %s;
    """, (key,))
    share_count = cur.fetchone()["count"]

    return {
        "comment": comment_count,
        "view": view_count,
        "share": share_count,
        **reactions,
    }


def get_author(cur, key):
    cur.execute("""
        SELECT "user".key, "user".name,  "user".username, "user".photo
        FROM blog
        LEFT JOIN "user" ON blog.author_key = "user".key
        WHERE blog.key = %s;
    """, (key,))
    author = cur.fetchone()
    if not author:
        cur.execute("""
            SELECT key, name, photo FROM "user" WHERE email = %s;
        """, (os.environ["MAIL_USERNAME"],))
        author = cur.fetchone()
    if not author:
        return None

    author["photo"] = (
        f"{request.host_url}photo/user/{author['photo']}"
        if author["photo"] else None
    )

    return author


def get_similar(cur, key):
    cur.execute("""SELECT * FROM blog WHERE key = %s;""", (key,))
    blog = cur.fetchone()
    if not blog:
        return []

    keywords = list(set(
        blog["tags"] + re.split(r'\s+', blog["title"].lower())))

    cur.execute("""
        WITH likeness AS (
            SELECT key, COUNT(*) AS score
            FROM blog,
                unnest(tags || STRING_TO_ARRAY(lower(title), ' ')) AS tn
            WHERE tn = ANY(%s)
            GROUP BY key
        )
        SELECT blog.*
        FROM blog
        JOIN likeness ON blog.key = likeness.key
        WHERE blog.status = 'active'
            AND blog.key != %s
            AND likeness.score > 0
        ORDER BY likeness.score DESC
        LIMIT 4;
    """, (keywords, key))
    blogs = cur.fetchall()

    return [blog_schema(x) for x in blogs]


@bp.get("/blogs/<key>/after")
@session(False)
def after_blog(cur, user, key):

    return {
        "engagement": get_engagement(cur, key, user["key"]),
        "author": get_author(cur, key),
        "comment_resp": many_blog_comments(cur, key, user["key"]),
        "similar": get_similar(cur, key)
    }, 200
