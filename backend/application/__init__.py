from flask import Flask, jsonify
from flask_cors import CORS

from . import storage
from . import postgres
from . import log
from .log import get as log_get
from . import auth
from .auth import forgot
from . import admin
from .admin import block
from .admin.block import get as block_get
from .admin import file_error
from .admin import highlight
from .admin.highlight import get as highlight_get
from . import report
from .report import get as report_get
from . import user
from .user import get as user_get
from .user import email
from .user import password
from .user import photo as user_photo
from .user import notification
from . import item
from .item import get as item_get
from .item import file
from .item import item_like
from .item import review
from .item.review import get as review_get
from .item.review import like as review_like
from . import cart
from .cart import get as cart_get
from . import order
from .order import get as order_get
from . import api
from . import fix


def create_app(conf=None):
    app = Flask(__name__)
    app.config.from_prefixed_env()
    if conf:
        app.config.from_pyfile(conf)
    CORS(app)

    @app.route("/")
    def index():

        return jsonify({
            "status": 200,
            "message": "Welcome to Theophilus Portfolio Website"
        })

    app.register_blueprint(storage.bp)
    app.register_blueprint(postgres.bp)
    app.register_blueprint(log.bp)
    app.register_blueprint(log_get.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(forgot.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(block.bp)
    app.register_blueprint(block_get.bp)
    app.register_blueprint(file_error.bp)
    app.register_blueprint(highlight.bp)
    app.register_blueprint(highlight_get.bp)
    app.register_blueprint(report.bp)
    app.register_blueprint(report_get.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(user_get.bp)
    app.register_blueprint(email.bp)
    app.register_blueprint(password.bp)
    app.register_blueprint(user_photo.bp)
    app.register_blueprint(notification.bp)
    app.register_blueprint(item.bp)
    app.register_blueprint(item_get.bp)
    app.register_blueprint(file.bp)
    app.register_blueprint(item_like.bp)
    app.register_blueprint(review.bp)
    app.register_blueprint(review_get.bp)
    app.register_blueprint(review_like.bp)
    app.register_blueprint(cart.bp)
    app.register_blueprint(cart_get.bp)
    app.register_blueprint(order.bp)
    app.register_blueprint(order_get.bp)
    app.register_blueprint(api.bp)
    app.register_blueprint(fix.bp)

    return app
