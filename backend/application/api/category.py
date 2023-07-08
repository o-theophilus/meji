from flask import Blueprint, jsonify, request
from .tools import token_to_user
from .schema import category_schema, item_schema
from uuid import uuid4
from .database import database


bp = Blueprint("category", __name__)


@bp.get("/category")
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

    # categories = get_categories(data)
    categories = []

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "categories": [category_schema(x) for x in categories]
        }
    })


@ bp.get("/category/<name>")
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

    category = query("category", "name", name, data)
    if not category:
        return jsonify({
            "status": 400,
            "message": "invalid request"
        })

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "category": category_schema(category)
        }
    })


@ bp.post("/category")
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

    cate_with_name = query("category", "name", request.json["name"], data)
    if cate_with_name:
        return jsonify({
            "status": 201,
            "message": "name in use"
        })

    category = {
        "key": uuid4().hex,
        "name": request.json["name"],
        "icon": request.json["name"],
        "items": [],
        "type": "category",
        "order": 1000000
    }

    if "icon" in request.json and request.json["icon"]:
        category["icon"] = request.json["icon"]

    category = database(category)
    # categories = get_categories(data)
    categories = []
    categories = [*categories, category]

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            # "category": category_schema(category),
            "categories": [category_schema(x) for x in categories]
        }
    })


@ bp.post("/category/<key>")
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

    categories = []
    cates_ = request.json["categories"]
    for row in data:
        if row["type"] == "category":
            if row["name"] in cates_:
                cates_.remove(row["name"])
                if item["key"] not in row["items"]:
                    row["items"] = [*row["items"], item["key"]]
                    categories.append(row)

            elif item["key"] in row["items"]:
                row["items"] = [x for x in row["items"] if x != item["key"]]
                categories.append(row)

    for name in cates_:
        category = {
            "key": uuid4().hex,
            "name": name,
            "icon": name,
            "items": [item["key"]],
            "type": "category",
            "order": 1000000
        }
        categories.append(category)

    database([*categories])

    data = database()
    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "item": item_schema(item, data)
        }
    })


@bp.put("/category/<key>")
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

    category = query("category", "key", key, data)
    if not category:
        return jsonify({
            "status": 400,
            "message": "invalid request"
        })

    cate_with_name = query("category", "name", request.json["name"], data)
    if cate_with_name and category["key"] != cate_with_name["key"]:
        return jsonify({
            "status": 201,
            "message": "name in use"
        })

    category["name"] = request.json["name"]
    if "icon" in request.json and request.json["icon"]:
        category["icon"] = request.json["icon"]

    category = database(category)
    # categories = get_categories(data)
    categories = []

    _categories = []
    for x in categories:
        if x["key"] == category["key"]:
            x = category
        _categories.append(x)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "categories": [category_schema(x) for x in _categories]
        }
    })


@bp.put("/category_/<key>")
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

    category = query("category", "key", key, data)
    if not category:
        return jsonify({
            "status": 400,
            "message": "invalid request"
        })

    if "dir" not in request.json or not request.json["dir"]:
        return jsonify({
            "status": 400,
            "message": "invalid request"
        })

    # categories = get_categories(data)
    categories = []
    temp_list = [x["key"] for x in categories]

    i = temp_list.index(key)
    if request.json["dir"] == "down":
        i += 1
    else:
        i -= 1

    if i < 0:
        i = 0

    temp_list.remove(key)
    temp_list.insert(i, key)

    for x in categories:
        x["order"] = temp_list.index(x["key"])

    categories = sorted(categories, key=lambda d: d['order'])
    # Limit to 25
    database(categories)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "categories": [category_schema(x) for x in categories]
        }
    })


@bp.delete("/category/<key>")
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

    category = query("category", "key",  key, data)
    if not category:
        return jsonify({
            "status": 400,
            "message": "invalid request"
        })

    db.rem(category)

    # categories = get_categories(data)
    categories = []
    categories = [x for x in categories if x["key"] != category["key"]]

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "categories": [category_schema(x) for x in categories]
        }
    })
