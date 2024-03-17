from flask import request, current_app
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime, timedelta
import smtplib
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os


def token_tool():
    return URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"],
        current_app.config["SECURITY_PASSWORD_SALT"]
    )


def now(day=0):
    return (datetime.now() + timedelta(days=1) * day).replace(
        microsecond=0).isoformat()


reserved_words = [
    "meji", "home", "shop", "save", "cart", "profile", "orders", "terms",
    "admin", "omni", "user", "users", "store", "stores", "item", "items",
    "all"]


def token_to_user(cur):
    if (
        "Authorization" not in request.headers or
        not request.headers["Authorization"]
    ):
        return None

    token = request.headers["Authorization"]
    try:
        token = token_tool().loads(token)
    except Exception:
        return None

    cur.execute('SELECT * FROM "user" WHERE key = %s;', (token,))
    return cur.fetchone()


def send_mail(to, subject, body):
    if current_app.config["DEBUG"]:
        print(body)
    else:
        admin = os.environ["MAIL_USERNAME"]

        msg = MIMEMultipart()
        msg['From'] = formataddr(("Meji", admin))
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        server = smtplib.SMTP('smtp.office365.com', 587)
        server.starttls()
        server.login(
            admin,
            os.environ["MAIL_PASSWORD"]
        )
        server.sendmail(admin, to, msg.as_bytes())
        server.quit()


def user_schema(user, saves=[], cart=[]):
    return {
        "key": user["key"],

        "name": user["name"],
        "email": user["email"],
        "phone": user["phone"],
        "address": {
            "line": user["address_line"],
            "country": user["address_country"],
            "state": user["address_state"],
            "local_area": user["address_local_area"],
            "postal_code": user["address_postal_code"]
        },
        "photo": (f"{request.host_url}photos/{user['photo']}"
                  if user["photo"] else None),

        "account_balance": user["account_balance"],

        "setting": {
            "theme": user["setting_theme"],
            "item_view": user["setting_item_view"]
        },
        "roles": user["roles"],
        "status": user["status"],
        "login": user["login"],

        "saves": saves,
        "cart": cart
    }


def item_schema(item):
    return {
        "key": item["key"],

        "date_c": item["date_c"],
        "date_u": item["date_u"],

        "slug": item["slug"],
        "name": item["name"],
        "price": item["price"],
        "old_price": item["old_price"],
        "info": item["info"],

        "variation": item["variation"],

        "photos": [f"{request.host_url}photos/{x}" for x in item["photos"]],
        "status": item["status"],

        "tags": item["tags"],
        "ratings": item["ratings"]
    }
