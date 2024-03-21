from flask import Flask, jsonify
from flask_cors import CORS

from . import api
from . import user
from . import user_get
from . import admin
from . import voucher
from . import feedback
from . import advert

from . import auth
from . import save
from . import cart
from . import order
from . import log
from . import item
from . import item_get

from . import storage
from . import postgres


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
            "message": "Welcome to MEJI API"
        })

    app.register_blueprint(api.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(user_get.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(save.bp)
    app.register_blueprint(cart.bp)
    app.register_blueprint(order.bp)
    app.register_blueprint(voucher.bp)
    app.register_blueprint(log.bp)

    app.register_blueprint(item.bp)
    app.register_blueprint(item_get.bp)
    app.register_blueprint(advert.bp)
    app.register_blueprint(feedback.bp)

    app.register_blueprint(storage.bp)
    app.register_blueprint(postgres.bp)

    return app
