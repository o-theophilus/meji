
from flask import Blueprint, request
from psycopg2.extras import Json

from ..tools import log, rate_limit, session

bp = Blueprint("item_tag", __name__)


def all_tags(cur):
    cur.execute("SELECT tags FROM item WHERE status = 'active';")
    temp = cur.fetchall()

    all_tags = []
    for x in temp:
        all_tags += x["tags"]

    tags_count = []
    unique_tags = []
    for x in all_tags:
        if x not in unique_tags:
            unique_tags.append(x)
            tags_count.append({
                "tag":  x,
                "count":  all_tags.count(x)
            })

    tags_count = sorted(tags_count, key=lambda d: d["count"], reverse=True)
    return [x["tag"] for x in tags_count]


def featured_tags(cur):
    cur.execute("""SELECT value FROM app WHERE key = 'featured_tag';""")
    featured = cur.fetchone()
    if not featured:
        cur.execute("""
            INSERT INTO app (key, value)
            VALUES ('featured_tag', %s) RETURNING *;
        """, (Json({"value": []}),))
        featured = cur.fetchone()

    featured = featured["value"]["value"]

    _all = all_tags(cur)

    return [x for x in _all if x in featured]


@bp.post("/items/tag/featured")
@session(True)
@rate_limit(20, 1)
@log("app")
def featured(cur, user):
    if "admin.tag.featured" not in user["access"]:
        return {
            "status": 403,
            "error": "unauthorized access"
        }, 403

    cur.execute("""SELECT value FROM app WHERE key = 'featured_tag';""")
    _featured = cur.fetchone()["value"]["value"]

    _new = request.json.get("tags")

    error = {}
    if not _new:
        error["tags"] = "Invalid request"
    elif type(_new) is not list:
        error["tags"] = "This field is required"
    elif set(_new) == set(_featured):
        error["tags"] = "No changes were made"
    if error:
        return {
            "status": 422,
            **error
        }, 422

    _all = all_tags(cur)
    _new = [x.lower() for x in _new]
    featured = [x for x in _all if x in _new]

    cur.execute("""
        UPDATE app SET value= %s
        WHERE key = 'featured_tag';
    """, (Json({"value": featured}),))

    return {
        "status": 200,
        "featured": featured_tags(cur),
        "all": all_tags(cur),
        "log": {
            "misc": {
                "from": _featured,
                "to": featured,
            }
        }
    }, 200


@bp.post("/items/tag/rename")
@session(True)
@rate_limit(20, 1)
@log("app")
def rename(cur, user):
    if "admin.tag.rename" not in user["access"]:
        return {
            "status": 403,
            "error": "unauthorized access"
        }, 403

    old = request.json.get("old")
    tag = request.json.get("tag")

    error = {}
    if not old:
        error["old"] = "Choose the tag to rename"
    if not tag:
        error["tag"] = "This field is required"
    elif old and old == tag:
        error["tags"] = "No changes were made"
    if error:
        return {
            "status": 422,
            **error
        }, 422

    old = old.lower()
    tag = tag.lower()

    cur.execute("""
        UPDATE item
        SET tags = (
            SELECT array_agg(DISTINCT elem)
            FROM unnest(array_replace(tags, %s, %s)) AS elem
        )
        WHERE %s = ANY(tags);
    """, (old, tag, old))

    return {
        "status": 200,
        "featured": featured_tags(cur),
        "all": all_tags(cur),
        "log": {
            "misc": {
                "from": old,
                "to": tag,
            }
        }
    }, 200


@bp.post("/items/tag/delete")
@session(True)
@rate_limit(20, 1)
@log("app")
def delete(cur, user):
    if "admin.tag.delete" not in user["access"]:
        return {
            "status": 403,
            "error": "unauthorized access"
        }, 403

    tags = request.json.get("tags")

    error = {}
    if not tags:
        error["tags"] = "Invalid request"
    elif type(tags) is not list:
        error["tags"] = "This field is required"
    if error:
        return {
            "status": 422,
            **error
        }, 422

    tags = [x.lower() for x in tags]

    cur.execute("""
        UPDATE item
        SET tags = COALESCE((
            SELECT array_agg(elem)
            FROM unnest(tags) AS elem
            WHERE elem <> ALL(%s)
        ), '{}')
        WHERE tags && %s;
    """, (tags, tags))

    return {
        "status": 200,
        "featured": featured_tags(cur),
        "all": all_tags(cur),
        "log": {
            "misc": {"tags": tags, }
        }
    }, 200
