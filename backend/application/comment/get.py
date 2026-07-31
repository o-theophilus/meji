from math import ceil

from flask import Blueprint, request

from ..tools import session

bp = Blueprint("comment_get", __name__)


def many_item_comments(cur, key, user_key, page_size=24):
    order_by = {
        'latest': 'date_created',
        'oldest': 'date_created',
        'reply': 'reply_count',
        'most relevant ▼': 'most_like',
        'least relevant ▲': 'most_like',
        'rating ▼': 'rating',
        'rating ▲': 'rating',
    }
    order_dir = {
        'latest': 'DESC',
        'oldest': 'ASC',
        'reply': 'DESC',
        'most relevant ▼': 'DESC',
        'least relevant ▲': 'ASC',
        'rating ▼': 'DESC',
        'rating ▲': 'ASC',
    }

    search_params = {
        "order": 'most relevant ▼',
        "page_no": 1,
        "page_size": page_size
    }
    order = request.args.get("order", search_params["order"])
    page_no = int(request.args.get("page_no", search_params["page_no"]))
    page_size = int(request.args.get("page_size", search_params["page_size"]))
    page_size = min(page_size, 100)

    cur.execute("""
        SELECT * FROM item WHERE slug = %s OR key::TEXT = %s;
    """, (key, key))
    item = cur.fetchone()
    if not item:
        return {
            "error": "Invalid request"
        }, 404

    cur.execute(f"""
        WITH sub_c AS (
            SELECT parent_key, COUNT(*) AS reply_count
            FROM comment
            WHERE parent_key IS NOT NULL
            GROUP BY parent_key
        ),

        l AS (
            SELECT
                comment_key,
                COUNT(*) FILTER (WHERE reaction = 'like') -
                COUNT(*) FILTER (WHERE reaction = 'dislike') AS most_like
            FROM "like"
            WHERE comment_key IS NOT NULL
            GROUP BY comment_key
        )

        SELECT
            c.key, c.date_created, c.comment, c.rating,
            u.key AS user_key, u.name, u.username, u.photo,
            COALESCE(sub_c.reply_count, 0) AS reply_count,
            COALESCE(l.most_like, 0) AS most_like

        FROM comment c
        JOIN "user" u ON u.key = c.user_key
        LEFT JOIN sub_c ON sub_c.parent_key = c.key
        LEFT JOIN l ON l.comment_key = c.key

        WHERE c.item_key = %s AND c.parent_key IS NULL
        ORDER BY {order_by[order]} {order_dir[order]}, c.key DESC
        LIMIT %s OFFSET %s
    """, (
        item["key"],
        page_size,
        (page_no - 1) * page_size
    ))
    _comments = cur.fetchall()
    comment_keys = [r["key"] for r in _comments]

    replies = []
    likes = []

    if comment_keys:
        cur.execute("""
            SELECT
                c.key, c.date_created, c.comment, c.rating, c.parent_key,
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
                comment_key,
                COUNT(*) FILTER (WHERE reaction = 'like' AND user_key != %s)
                    AS others_like,
                COUNT(*) FILTER (WHERE reaction = 'dislike' AND user_key != %s)
                    AS others_dislike,
                MAX(reaction) FILTER (WHERE user_key = %s) AS user_reaction
            FROM "like"
            WHERE comment_key::TEXT = ANY(%s)
            GROUP BY comment_key
        """, (user_key, user_key, user_key, comment_keys))
        likes = cur.fetchall()

    likes_map = {
        x["comment_key"]: {
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
            "rating": x["rating"],
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
            "rating": x["rating"],
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
            r.rating,
            COUNT(comment.rating) AS count
        FROM generate_series(1, 5) AS r(rating)
        LEFT JOIN comment
            ON comment.rating = r.rating
            AND comment.item_key = %s
            AND comment.parent_key IS NULL
        GROUP BY r.rating
        ORDER BY r.rating DESC
    """, (item["key"],))
    ratings = cur.fetchall()

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
    """, (user_key, item["key"], user_key, item["key"]))
    user_comment_info = cur.fetchone()

    cur.execute("""
        SELECT
            COUNT(*) AS total_comment,
            COUNT(*) FILTER (WHERE parent_key IS NULL) AS total_parent
        FROM comment
        WHERE item_key = %s;
    """, (item["key"],))
    total = cur.fetchone()
    total_comment = total["total_comment"]
    total_parent = total["total_parent"]

    return {
        "item": item,
        "comments": comments,
        "ratings": ratings,
        "total_comment": total_comment,
        "total_page": ceil(total_parent / page_size),
        "order_by": list(order_by.keys()),
        "search_params": search_params,
        "has_purchased": user_comment_info["has_purchased"],
        "can_comment": user_comment_info["can_comment"],
    }


def many_blog_comments(cur, key, user_key):
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

    search_params = {
        "order": 'most relevant',
        "page_no": 1,
        "page_size": 24
    }
    order = request.args.get("order", search_params["order"])
    page_no = int(request.args.get("page_no", search_params["page_no"]))
    page_size = int(request.args.get("page_size", search_params["page_size"]))
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
            WHERE parent_key IS NOT NULL AND blog_key = %s
            GROUP BY parent_key
        ) sub_c ON sub_c.parent_key = c.key

        LEFT JOIN (
            SELECT comment_key,
                COUNT(*) FILTER (WHERE reaction = 'like') AS "like",
                COUNT(*) FILTER (WHERE reaction = 'dislike') AS dislike
            FROM "like"
            WHERE comment_key IS NOT NULL
            GROUP BY comment_key
        ) l ON l.comment_key = c.key

        WHERE c.blog_key = %s AND c.parent_key IS NULL
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
                comment_key,
                COUNT(*) FILTER (WHERE reaction = 'like' AND user_key != %s)
                    AS others_like,
                COUNT(*) FILTER (WHERE reaction = 'dislike' AND user_key != %s)
                    AS others_dislike,
                MAX(reaction) FILTER (WHERE user_key = %s) AS user_reaction
            FROM "like"
            WHERE comment_key::TEXT = ANY(%s)
            GROUP BY comment_key
        """, (user_key, user_key, user_key, comment_keys))
        likes = cur.fetchall()

    likes_map = {
        x["comment_key"]: {
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
        WHERE blog_key = %s;
    """, (key,))
    total = cur.fetchone()
    total_comment = total["total_comment"]
    total_parent = total["total_parent"]

    return {
        "comments": comments,
        "order_by": list(order_by.keys()),
        "total_comment": total_comment,
        "total_page": ceil(total_parent / page_size),
        "search_params": search_params,
    }


@bp.get("/items/<key>/comments")
@session(False)
def items(cur, user, key):
    return many_item_comments(cur, key, user["key"]), 200


@bp.get("/blogs/<key>/comments")
@session(False)
def blogs(cur, user, key):
    return many_blog_comments(cur, key, user["key"]), 200
