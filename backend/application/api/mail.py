from flask import current_app
from flask_mail import Mail, Message


mail = Mail()


def send_mail(to, subject, body):
    # if current_app.config["ENV"] == "development":
    #     print(body)
    # else:
    msg = Message(
        subject,
        recipients=[to],
        html=body
    )
    mail.send(msg)


def notify(subject, mail_body, plain_body):

    send_mail(
        current_app.config["MAIL_DEFAULT_SENDER"][1],
        subject,
        mail_body
    )
