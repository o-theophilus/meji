import os

from flask import Blueprint, jsonify

from .postgres import db_close, db_open
from .tools import access_pass

bp = Blueprint("fix", __name__)


# @bp.get("/fix")
def quick_fix():
    con, cur = db_open()

    cur.execute("""
        UPDATE log
        SET entity_type = 'user'
        WHERE entity_type = 'account'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'user'
        WHERE entity_type = 'admin'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'item', action = 'added item advert photo(s)'
        WHERE entity_type = 'advert' AND action = 'added advert photos'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'item', action = 'created item advert'
        WHERE entity_type = 'advert' AND action = 'created'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'item', action = 'deleted item advert'
        WHERE entity_type = 'advert' AND action = 'deleted photo'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'app', action = 'cleaned up anonymous users'
        WHERE entity_type = 'app' AND action = 'app maintenance'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'blog', action = 'added comment to blog'
        WHERE entity_type = 'blog' AND action = 'added comment'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'cart', action = 'added item to cart'
        WHERE entity_type = 'cart' AND action = 'added_to_cart'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'cart', action = 'removed item from cart'
        WHERE entity_type = 'cart' AND action = 'removed_from_cart'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'cart', action = 'edited cart receiver'
        WHERE entity_type = 'cart' AND action = 'edited_receiver'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'cart', action = 'added coupon to cart'
        WHERE entity_type = 'coupon' AND action = 'added coupon to cart'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'cart', action = 'removed coupon to cart'
        WHERE entity_type = 'coupon' AND action = 'removed coupon to cart'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'order', action = 'created order'
        WHERE entity_type = 'order' AND action = 'created'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'order', action = 'changed order delivery date'
        WHERE entity_type = 'order' AND action = 'changed_date'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'order', action = 'changed order status'
        WHERE entity_type = 'order' AND action = 'changed_status'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'order', action = 'used coupon'
        WHERE entity_type = 'coupon' AND action = 'used coupon'
    ;""")

    cur.execute("""
        DELETE FROM log WHERE entity_type = 'photo'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'review', action = 'added item review'
        WHERE entity_type = 'review' AND action = 'created'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'review', action = 'deleted item review'
        WHERE entity_type = 'review' AND action = 'deleted'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'item', action = 'added comment to item'
        WHERE entity_type = 'review' AND action = 'added item review'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'comment', action = 'deleted comment'
        WHERE entity_type = 'review' AND action = 'deleted item review'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'comment', action = 'like comment'
        WHERE entity_type = 'review' AND action = 'like review'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'comment', action = 'unlike comment'
        WHERE entity_type = 'review' AND action = 'unlike review'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'comment', action = 'dislike comment'
        WHERE entity_type = 'review' AND action = 'dislike review'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'comment', action = 'undislike comment'
        WHERE entity_type = 'review' AND action = 'undislike review'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'user', action = 'created'
        WHERE entity_type = 'user' AND action = 'created anonymous account'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'user', action = 'created'
        WHERE entity_type = 'user' AND action = 'created account'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'user', action = 'signedup'
        WHERE entity_type = 'user' AND action = 'signedup account'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'user', action = 'activated account'
        WHERE entity_type = 'user' AND action = 'actived account'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'user', action = 'activated account'
        WHERE entity_type = 'user' AND action = 'confirmed_email'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'user', action = 'activated account'
        WHERE entity_type = 'user' AND action = 'confirmed'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'user', action = 'logged in'
        WHERE entity_type = 'user' AND action = 'logged_in'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'user', action = 'logged out'
        WHERE entity_type = 'user' AND action = 'logged_out'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'user', action = 'deleted account'
        WHERE entity_type = 'user' AND action = 'deleted_account'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'user', action = 'blocked user'
        WHERE entity_type = 'user' AND action = 'blocked'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'user', action = 'unblocked user'
        WHERE entity_type = 'user' AND action = 'unblocked'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'user', action = 'changed theme'
        WHERE entity_type = 'user' AND action = 'changed_theme'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'user', action = 'edited profile'
        WHERE entity_type = 'user' AND action = 'edited'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'user', action = 'changed user access'
        WHERE entity_type = 'user' AND action = 'changed_access'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'user', action = 'changed user access'
        WHERE entity_type = 'user' AND action = 'changed admin access'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'user', action = 'updated profile photo'
        WHERE entity_type = 'user' AND action = 'updated_photo'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'user', action = 'edited profile'
        WHERE entity_type = 'user' AND action = 'edited profile details'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'item', action = 'created item'
        WHERE entity_type = 'item' AND action = 'created'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'item', action = 'edited item'
        WHERE entity_type = 'item' AND action = 'edited'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'item', action = 'deleted item'
        WHERE entity_type = 'item' AND action = 'deleted'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'item', action = 'like item'
        WHERE entity_type = 'item' AND action = 'like'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'item', action = 'unlike item'
        WHERE entity_type = 'item' AND action = 'unlike'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'item', action = 'added comment to item'
        WHERE entity_type = 'item' AND action = 'added comment'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'item', action = 'added photo to item'
        WHERE entity_type = 'item' AND action = 'added_file'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'item', action = 'edited item photo'
        WHERE entity_type = 'item' AND action = 'edited_files'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'code', action = 'requested OTP'
        WHERE entity_type = 'code' AND action = 'requested'
    ;""")

    cur.execute("""
        UPDATE log
        SET entity_type = 'item', action = 'viewed item'
        WHERE entity_type = 'item' AND action = 'viewed'
    ;""")
    cur.execute("""
        UPDATE log
        SET entity_type = 'blog', action = 'viewed blog'
        WHERE entity_type = 'blog' AND action = 'viewed'
    ;""")
    cur.execute("""
        UPDATE log
        SET entity_type = 'user', action = 'viewed user'
        WHERE entity_type = 'user' AND action = 'viewed'
    ;""")
    cur.execute("""
        UPDATE log
        SET entity_type = 'coupon', action = 'viewed coupon'
        WHERE entity_type = 'coupon' AND action = 'viewed'
    ;""")


    cur.execute("""
        DELETE FROM log 
        WHERE entity_type = 'page'
        AND action ILIKE '%/review%'
    ;""")
    cur.execute("""
        DELETE FROM log 
        WHERE entity_type = 'page'
        AND action ILIKE '%/orders/%'
    ;""")


    db_close(con, cur)
    return jsonify({
        "status": 200
    })


def fix_access():
    con, cur = db_open()

    cur.execute("""
        UPDATE "user" SET access=%s WHERE email = %s;
    """, (
        [f"{x}.{y[0]}" for x in access_pass for y in access_pass[x]],
        os.environ["MAIL_USERNAME"]
    ))

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
