import os
import re
from math import ceil

from flask import Blueprint, jsonify, request

from ..postgres import db_close, db_open
from ..tools import get_session

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
def get(key):
    con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute("""
        SELECT * FROM blog WHERE slug = %s OR key::TEXT = %s
    """, (key, key))
    blog = cur.fetchone()

    if not blog:
        db_close(con, cur)
        return jsonify({
            "status": 404,
            "error": "Oops! The blog you're looking for doesn't exist"
        })

    if (
        blog["status"] != "active"
        and "blog.add" not in user["access"]
        and "blog.edit_status" not in user["access"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 403,
            "error": "unauthorized access"
        })

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "blog": blog_schema(blog)
    })


@bp.get("/blogs")
def get_blogs(cur=None):
    close_conn = not cur
    if not cur:
        con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        if close_conn:
            db_close(con, cur)
        return jsonify(session)
    user = session["user"]

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

    searchParams = {
        "search": "",
        "status": "active",
        "tag": "",
        "order": "latest",
        "page_no": 1,
        "page_size": 24
    }
    search = request.args.get("search", searchParams["search"]).strip()
    status = request.args.get("status", searchParams["status"])
    tag = request.args.get("tag", searchParams["tag"])
    order = request.args.get("order", searchParams["order"])
    page_no = int(request.args.get("page_no", searchParams["page_no"]))
    page_size = int(request.args.get("page_size", searchParams["page_size"]))
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
            SELECT entity_key, COUNT(*) AS _count
            FROM comment
            WHERE entity_type = 'blog'
            GROUP BY entity_key
        ) c ON c.entity_key = blog.key

        LEFT JOIN (
            SELECT entity_key,
                COUNT(*) FILTER (WHERE reaction = 'like') AS "like",
                COUNT(*) FILTER (WHERE reaction = 'dislike') AS dislike
            FROM "like"
            WHERE entity_type = 'blog'
            GROUP BY entity_key
        ) l ON l.entity_key = blog.key

        LEFT JOIN (
            SELECT entity_key, COUNT(DISTINCT user_key) AS _count
            FROM log
            WHERE entity_type = 'blog'
                AND action = 'viewed'
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

    if close_conn:
        db_close(con, cur)
    return jsonify({
        "status": 200,
        "blogs": [blog_schema(x) for x in blogs],
        "order_by": list(order_by.keys()),
        "_status": ['active', 'draft'],
        "total_page": ceil(total_page / page_size),
        "searchParams": searchParams
    })


@bp.get("/blogs/<key>/comments")
def get_comments(key, cur=None):
    close_conn = not cur
    if not cur:
        con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        if close_conn:
            db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    order_by = {
        'latest': 'c.date_created',
        'oldest': 'c.date_created',
        'most reply': 'reply_count',
        # 'like': '"like"',
        # 'dislike': 'dislike',
        'most relevant': 'most_like',
        # 'most engaged': 'most_engaged',
    }
    order_dir = {
        'latest': 'DESC',
        'oldest': 'ASC',
        'most reply': 'DESC',
        'like': 'DESC',
        'dislike': 'DESC',
        'most relevant': 'DESC',
        'most engaged': 'DESC',
    }

    searchParams = {
        "order": 'most relevant',
        "page_no": 1,
        "page_size": 24
    }
    order = request.args.get("order", searchParams["order"])
    page_no = int(request.args.get("page_no", searchParams["page_no"]))
    page_size = int(request.args.get("page_size", searchParams["page_size"]))
    page_size = min(page_size, 100)

    cur.execute(f"""
        SELECT
            c.key, c.date_created, c.comment, c.parent_key,
            u.key AS user_key, u.name, u.username, u.photo,
            COALESCE(sub_c.reply_count, 0) AS reply_count,
            COALESCE(l."like", 0) AS "like",
            COALESCE(l.dislike, 0) AS dislike,
            COALESCE(l."like", 0) - COALESCE(l.dislike, 0) AS most_like,
            COALESCE(sub_c.reply_count, 0) + COALESCE(l."like", 0)
                + COALESCE(l.dislike, 0) AS most_engaged
        FROM comment c
        JOIN "user" u ON u.key = c.user_key

        LEFT JOIN (
            SELECT parent_key, COUNT(*) AS reply_count
            FROM comment
            WHERE parent_key IS NOT NULL
                AND entity_key = %s AND entity_type = 'blog'
            GROUP BY parent_key
        ) sub_c ON sub_c.parent_key = c.key

        LEFT JOIN (
            SELECT entity_key,
                COUNT(*) FILTER (WHERE reaction = 'like') AS "like",
                COUNT(*) FILTER (WHERE reaction = 'dislike') AS dislike
            FROM "like"
            WHERE entity_type = 'comment'
            GROUP BY entity_key
        ) l ON l.entity_key = c.key

        WHERE c.entity_key = %s AND  c.entity_type = 'blog'
            AND c.parent_key IS NULL
        ORDER BY {order_by[order]} {order_dir[order]}, c.key DESC
        LIMIT %s OFFSET %s;
    """, (key, key, page_size, (page_no - 1) * page_size))
    _comments = cur.fetchall()
    comment_keys = [r["key"] for r in _comments]

    replies = []
    likes = []

    if comment_keys:
        cur.execute("""
            SELECT
                c.key, c.date_created, c.comment, c.parent_key,
                u.key AS user_key, u.name, u.username, u.photo
            FROM comment c
            JOIN "user" u ON u.key = c.user_key
            WHERE c.parent_key::TEXT = ANY(%s)
            ORDER BY c.date_created ASC
        """, (comment_keys,))
        replies = cur.fetchall()

        for x in replies:
            comment_keys.append(x["key"])

        cur.execute("""
            SELECT
                entity_key,
                COUNT(*) FILTER (WHERE reaction = 'like' AND user_key != %s)
                    AS others_like,
                COUNT(*) FILTER (WHERE reaction = 'dislike' AND user_key != %s)
                    AS others_dislike,
                MAX(reaction) FILTER (WHERE user_key = %s) AS user_reaction
            FROM "like"
            WHERE entity_key::TEXT = ANY(%s) AND entity_type = 'comment'
            GROUP BY entity_key
        """, (user["key"], user["key"], user["key"], comment_keys))
        likes = cur.fetchall()

    likes_map = {
        x["entity_key"]: {
            "others_like": x["others_like"],
            "others_dislike": x["others_dislike"],
            "user_reaction": x["user_reaction"]
        }
        for x in likes
    }

    replies_map = {}
    for x in replies:
        replies_map.setdefault(x["parent_key"], []).append({
            "key": x["key"],
            "date_created": x["date_created"],
            "comment": x["comment"],
            "user": {
                "key": x["user_key"],
                "name": x["name"],
                "username": x["username"],
                "photo": f'{request.host_url}photo/user/{x["photo"]}' if x[
                    "photo"] else None
            },
            "stats": likes_map.get(x["key"], {
                "others_like": 0,
                "others_dislike": 0,
                "user_reaction": None
            }),
        })

    comments = []
    for x in _comments:
        comments.append({
            "key": x["key"],
            "date_created": x["date_created"],
            "comment": x["comment"],
            "user": {
                "key": x["user_key"],
                "name": x["name"],
                "username": x["username"],
                "photo": f'{request.host_url}photo/user/{x["photo"]}' if x[
                    "photo"] else None
            },
            "stats": likes_map.get(x["key"], {
                "others_like": 0,
                "others_dislike": 0,
                "user_reaction": None
            }),
            "replies": replies_map.get(x["key"], [])
        })

    cur.execute("""
        SELECT
            COUNT(*) AS total_comment,
            COUNT(*) FILTER (WHERE parent_key IS NULL) AS total_parent
        FROM comment
        WHERE entity_key = %s AND entity_type = 'blog';
    """, (key,))
    total = cur.fetchone()
    total_comment = total["total_comment"]
    total_parent = total["total_parent"]

    if close_conn:
        db_close(con, cur)
    return jsonify({
        "status": 200,
        "comments": comments,
        "order_by": list(order_by.keys()),
        "total_comment": total_comment,
        "total_page": ceil(total_parent / page_size),
        "searchParams": searchParams,
    })


def get_engagement(cur, key, user_key):
    cur.execute("""
        SELECT
            COUNT(CASE WHEN user_key != %s
                AND reaction = 'like' THEN 1 END) AS others_like,
            COUNT(CASE WHEN user_key != %s
                AND reaction = 'dislike' THEN 1 END) AS others_dislike,
            MAX(CASE WHEN user_key = %s THEN reaction END) AS user_reaction
        FROM "like"
        WHERE entity_key = %s AND entity_type = 'comment'
    """, (user_key, user_key, user_key, key))
    reactions = cur.fetchone()

    cur.execute("""
        SELECT COUNT(*) FROM comment
        WHERE entity_key = %s AND entity_type = 'blog';
    """, (key,))
    comment_count = cur.fetchone()["count"]

    cur.execute("""
        SELECT COUNT(DISTINCT user_key) FROM log
        WHERE entity_type = 'blog' AND action = 'viewed' AND entity_key = %s
    """, (key,))
    view_count = cur.fetchone()["count"]

    cur.execute("""
        SELECT COUNT(*) FROM log
        WHERE entity_type = 'blog' AND action = 'shared' AND entity_key = %s
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
def after_blog(key):
    con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    engagement = get_engagement(cur, key, user["key"])
    author = get_author(cur, key)
    comment_resp = get_comments(key, cur).json
    similar = get_similar(cur, key)

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "engagement": engagement,
        "author": author,
        "comment_resp": comment_resp,
        "similar": similar
    })
