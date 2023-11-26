from flask import request, current_app
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime, timedelta
from .database import query
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
    "home", "shop", "save", "cart", "profile", "orders", "terms", "admin",
    "omni", "user", "users", "store", "stores", "item", "items", "all"]


def token_to_user(data):
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

    return query({"type": "user", "key": token}, db=data)


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
