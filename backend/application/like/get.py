from math import ceil

from flask import Blueprint, request

from ..tools import item_schema, session

bp = Blueprint("like_get", __name__)


def get_user_like(cur, user_key):
    cur.execute("""
        SELECT item_key FROM "like"
        WHERE user_key = %s AND item_key IS NOT NULL;
    """, (user_key,))
    likes = cur.fetchall()
    return [x["item_key"] for x in likes]


@bp.get("/items/like")
@session(False)
def like_page(cur, user,):
    order_by = {
        'latest': 'item.date_created',
        'oldest': 'item.date_created',
        'name (a-z)': 'item.name',
        'name (z-a)': 'item.name',
        'cheap': 'item.price',
        'costly': 'item.price'
    }

    order_dir = {
        'latest': 'DESC',
        'oldest': 'ASC',
        'name (a-z)': 'ASC',
        'name (z-a)': 'DESC',
        'cheap': 'ASC',
        'costly': 'DESC'
    }

    search_params = {
        "search": "",
        "order": "latest",
        "page_no": 1,
        "page_size": 24
    }
    search = request.args.get("search", search_params["search"]).strip()
    order = request.args.get("order", search_params["order"])
    page_no = int(request.args.get("page_no", search_params["page_no"]))
    page_size = int(request.args.get("page_size", search_params["page_size"]))
    page_size = min(page_size, 100)

    cur.execute(f"""
        WITH rating AS (
            SELECT
                comment.item_key AS key,
                AVG(comment.rating) as rating
            FROM comment
            WHERE comment.item_key IS NOT NULL AND comment.parent_key IS NULL
            GROUP BY comment.item_key
        )

        SELECT
            item.*,
            COALESCE(rating.rating, 0) AS rating,
            COUNT(*) OVER() AS _count
        FROM item
        LEFT JOIN "like" ON item.key = "like".item_key
        LEFT JOIN rating ON item.key = rating.key
        WHERE
            item.status = 'active'
            AND "like".user_key = %s
            AND "like".item_key IS NOT NULL
            AND (%s = '' OR item.name ILIKE %s)
        ORDER BY {order_by[order]} {order_dir[order]}, item.key DESC
        LIMIT %s OFFSET %s;
    """, (
        user["key"],
        search, f"%{search}%",
        page_size, (page_no - 1) * page_size
    ))
    items = cur.fetchall()

    return {
        "items": [item_schema(x) for x in items],
        "total_page": ceil(items[0]["_count"] / page_size) if items else 0,
        "order_by": list(order_by.keys()),
        "search_params": search_params,
    }, 200
