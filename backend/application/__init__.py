from flask import Flask, jsonify
from flask_cors import CORS

from . import api
from . import user
from . import user_get
from . import voucher
from . import feedback
from . import advert

from . import auth
from . import user_save_cart
from . import order_get
from . import order
from . import log
from . import item
from . import item_get


def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()
    CORS(app)

    @app.route("/")
    def index():
        return jsonify({
            "status": 200,
            "message": "Welcome to MEJI API"
        })

    app.register_blueprint(api.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(user_get.bp)
    app.register_blueprint(user_save_cart.bp)
    app.register_blueprint(order.bp)
    app.register_blueprint(order_get.bp)
    app.register_blueprint(voucher.bp)
    app.register_blueprint(log.bp)

    app.register_blueprint(item.bp)
    app.register_blueprint(item_get.bp)
    app.register_blueprint(advert.bp)
    app.register_blueprint(feedback.bp)

    return app
