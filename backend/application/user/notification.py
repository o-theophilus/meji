from flask import Blueprint

from ..api.file_error import file_error
from ..tools import rate_limit, session

bp = Blueprint("notification", __name__)


@bp.get("/notification")
@session(True)
@rate_limit(20, 1)
def notification(cur, user):
    nots = []
    if "admin.manage_files" in user["access"]:
        ferr = file_error(cur)

        if "unused_item_photo" in ferr and ferr[
                "unused_item_photo"]:
            nots.append({
                "type": 'unused item photo',
                "count": len(ferr["unused_item_photo"]),
                "slug": "/admin/file_error"
            })

        if "unused_user_photo" in ferr and ferr[
                "unused_user_photo"]:
            nots.append({
                "type": 'unused user photo',
                "count": len(ferr["unused_user_photo"]),
                "slug": "/admin/file_error"
            })

        if "items" in ferr and ferr["items"]:
            nots.append({
                "type": 'missing item photo',
                "count": len(ferr["items"]),
                "slug": "/admin/file_error"
            })

        if "users" in ferr and ferr["users"]:
            nots.append({
                "type": 'missing user photo',
                "count": len(ferr["users"]),
                "slug": "/admin/file_error"
            })

    return {
        "nots": nots
    }, 200
