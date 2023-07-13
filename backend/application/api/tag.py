from flask import Blueprint, jsonify, request
from .tools import token_to_user
from .schema import tag_schema, item_schema
from uuid import uuid4
from .database import database


bp = Blueprint("tag", __name__)


@bp.get("/tag")
def get_all():
    data = database()

    user = token_to_user(data)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    if "admin" not in user["roles"]:
        return jsonify({
            "status": 102,
            "message": "unauthorised access"
        })

    # tags = get_tags(data)
    tags = []

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "tags": [tag_schema(x) for x in tags]
        }
    })


@ bp.get("/tag/<name>")
def get(name):
    data = database()

    user = token_to_user(data)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    if "admin" not in user["roles"]:
        return jsonify({
            "status": 102,
            "message": "unauthorised access"
        })

    tag = query("tag", "name", name, data)
    if not tag:
        return jsonify({
            "status": 400,
            "message": "invalid request"
        })

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "tag": tag_schema(tag)
        }
    })


@ bp.post("/tag")
def add_new():
    data = database()

    user = token_to_user(data)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    if "admin" not in user["roles"]:
        return jsonify({
            "status": 102,
            "message": "unauthorised access"
        })

    if "name" not in request.json or not request.json["name"]:
        return jsonify({
            "status": 201,
            "message": "this field is required"
        })

    cate_with_name = query("tag", "name", request.json["name"], data)
    if cate_with_name:
        return jsonify({
            "status": 201,
            "message": "name in use"
        })

    tag = {
        "key": uuid4().hex,
        "name": request.json["name"],
        "icon": request.json["name"],
        "items": [],
        "type": "tag",
        "order": 1000000
    }

    if "icon" in request.json and request.json["icon"]:
        tag["icon"] = request.json["icon"]

    tag = database(tag)
    # tags = get_tags(data)
    tags = []
    tags = [*tags, tag]

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            # "tag": tag_schema(tag),
            "tags": [tag_schema(x) for x in tags]
        }
    })


@ bp.post("/tag/<key>")
def item_edit_cate(key):
    data = database()

    user = token_to_user(data)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    if "admin" not in user["roles"]:
        return jsonify({
            "status": 102,
            "message": "unauthorised access"
        })

    item = query("item", "key", key, data)
    if not item:
        return jsonify({
            "status": 400,
            "message": "invalid request"
        })

    tags = []
    cates_ = request.json["tags"]
    for row in data:
        if row["type"] == "tag":
            if row["name"] in cates_:
                cates_.remove(row["name"])
                if item["key"] not in row["items"]:
                    row["items"] = [*row["items"], item["key"]]
                    tags.append(row)

            elif item["key"] in row["items"]:
                row["items"] = [x for x in row["items"] if x != item["key"]]
                tags.append(row)

    for name in cates_:
        tag = {
            "key": uuid4().hex,
            "name": name,
            "icon": name,
            "items": [item["key"]],
            "type": "tag",
            "order": 1000000
        }
        tags.append(tag)

    database([*tags])

    data = database()
    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "item": item_schema(item, data)
        }
    })


@bp.put("/tag/<key>")
def edit(key):
    data = database()

    user = token_to_user(data)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    if "admin" not in user["roles"]:
        return jsonify({
            "status": 102,
            "message": "unauthorised access"
        })

    if "name" not in request.json or not request.json["name"]:
        return jsonify({
            "status": 201,
            "message": "this field is required"
        })

    tag = query("tag", "key", key, data)
    if not tag:
        return jsonify({
            "status": 400,
            "message": "invalid request"
        })

    cate_with_name = query("tag", "name", request.json["name"], data)
    if cate_with_name and tag["key"] != cate_with_name["key"]:
        return jsonify({
            "status": 201,
            "message": "name in use"
        })

    tag["name"] = request.json["name"]
    if "icon" in request.json and request.json["icon"]:
        tag["icon"] = request.json["icon"]

    tag = database(tag)
    # tags = get_tags(data)
    tags = []

    _tags = []
    for x in tags:
        if x["key"] == tag["key"]:
            x = tag
        _tags.append(x)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "tags": [tag_schema(x) for x in _tags]
        }
    })


@bp.put("/tag_/<key>")
def rearrange(key):
    data = database()

    user = token_to_user(data)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    if "admin" not in user["roles"]:
        return jsonify({
            "status": 102,
            "message": "unauthorised access"
        })

    tag = query("tag", "key", key, data)
    if not tag:
        return jsonify({
            "status": 400,
            "message": "invalid request"
        })

    if "dir" not in request.json or not request.json["dir"]:
        return jsonify({
            "status": 400,
            "message": "invalid request"
        })

    # tags = get_tags(data)
    tags = []
    temp_list = [x["key"] for x in tags]

    i = temp_list.index(key)
    if request.json["dir"] == "down":
        i += 1
    else:
        i -= 1

    if i < 0:
        i = 0

    temp_list.remove(key)
    temp_list.insert(i, key)

    for x in tags:
        x["order"] = temp_list.index(x["key"])

    tags = sorted(tags, key=lambda d: d['order'])
    # Limit to 25
    database(tags)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "tags": [tag_schema(x) for x in tags]
        }
    })


@bp.delete("/tag/<key>")
def delete(key):
    data = database()

    user = token_to_user(data)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    if "admin" not in user["roles"]:
        return jsonify({
            "status": 102,
            "message": "unauthorised access"
        })

    tag = query("tag", "key",  key, data)
    if not tag:
        return jsonify({
            "status": 400,
            "message": "invalid request"
        })

    db.rem(tag)

    # tags = get_tags(data)
    tags = []
    tags = [x for x in tags if x["key"] != tag["key"]]

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "tags": [tag_schema(x) for x in tags]
        }
    })
