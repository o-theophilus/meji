from flask import Blueprint

from ..api.file_error import get_file_error
from ..postgres import db_close, db_open
from ..tools import get_session

bp = Blueprint("notification", __name__)


@bp.get("/notification")
def notification():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return session
    user = session["user"]

    nots = []
    if "admin.manage_files" in user["access"]:
        file_error = get_file_error(cur).json

        if "unused_item_photo" in file_error and file_error[
                "unused_item_photo"]:
            nots.append({
                "type": 'unused item photo',
                "count": len(file_error["unused_item_photo"]),
                "slug": "/admin/file_error"
            })

        if "unused_user_photo" in file_error and file_error[
                "unused_user_photo"]:
            nots.append({
                "type": 'unused user photo',
                "count": len(file_error["unused_user_photo"]),
                "slug": "/admin/file_error"
            })

        if "items" in file_error and file_error["items"]:
            nots.append({
                "type": 'missing item photo',
                "count": len(file_error["items"]),
                "slug": "/admin/file_error"
            })

        if "users" in file_error and file_error["users"]:
            nots.append({
                "type": 'missing user photo',
                "count": len(file_error["users"]),
                "slug": "/admin/file_error"
            })

    db_close(con, cur)
    return {
        "status": 200,
        "nots": nots
    }, 200
