from flask import Flask
from flask_cors import CORS
from .api.mail import mail

from . import api
from .api import auth
from .api import user
from .api import user_get
from .api import user_photo
from .api import user_save
from .api import user_cart
from .api import user_password
from .api import user_email
from .api import confirm
from .api import order
from .api import order_get
from .api import voucher

from .api import item
from .api import item_get
from .api import item_photo
from .api import item_ad_photo
from .api import item_ad
from .api import feedback

from .api import category


def create_app(config_file="config.py"):
    app = Flask(__name__)
    app.config.from_prefixed_env()
    app.config.from_pyfile(config_file)
    mail.init_app(app)
    CORS(app)

    app.register_blueprint(api.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(user_get.bp)
    app.register_blueprint(user_photo.bp)
    app.register_blueprint(user_save.bp)
    app.register_blueprint(user_cart.bp)
    app.register_blueprint(user_password.bp)
    app.register_blueprint(user_email.bp)
    app.register_blueprint(confirm.bp)
    app.register_blueprint(order.bp)
    app.register_blueprint(order_get.bp)
    app.register_blueprint(voucher.bp)

    app.register_blueprint(item.bp)
    app.register_blueprint(item_get.bp)
    app.register_blueprint(item_photo.bp)
    app.register_blueprint(item_ad_photo.bp)
    app.register_blueprint(item_ad.bp)
    app.register_blueprint(feedback.bp)

    app.register_blueprint(category.bp)

    return app
