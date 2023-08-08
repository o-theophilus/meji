from flask import current_app
from flask_mail import Mail, Message


mail = Mail()


def send_mail(to, subject, body):
    if current_app.config["DEBUG"]:
        print(body)
    else:
        mail.send(Message(
            subject,
            recipients=[to],
            html=body
        ))
