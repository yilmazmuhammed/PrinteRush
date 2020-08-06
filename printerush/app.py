# https://realpython.com/flask-blueprint/#what-a-flask-blueprint-looks-like
# https://github.com/j127/Flask-Blueprint-Example/blob/master/flaskbp/__init__.py
# https://realpython.com/flask-blueprint/#what-a-flask-blueprint-looks-like
import locale
import os
from datetime import timedelta

from flask import Flask, render_template, request, redirect, url_for
from flask_jsglue import JSGlue
from flask_login import LoginManager
from pony.flask import Pony

from printerush.address.address import address_bp
from printerush.address.api import address_api_bp
from printerush.auth.auth import auth_bp
from printerush.cart.api import cart_api_bp
from printerush.cart.cart import cart_bp
from printerush.common.assistant_func import LayoutPI
from printerush.database import db_bp
from printerush.database.models import WebUser
from printerush.general.api import general_api_bp
from printerush.general.general import general_bp
from printerush.order.order import order_bp
from printerush.printable_3d_model.printable_3d_model import models_bp
from printerush.product.api import product_api_bp
from printerush.product.product import products_bp
from printerush.store.store import store_sbp
from printerush.visitor.assistant_func import track_visitor

locale.setlocale(locale.LC_ALL, 'tr_TR.utf8')

app = Flask(__name__, instance_relative_config=True)

app.secret_key = os.getenv("SECRET_KEY")

app.config['SERVER_NAME'] = 'printerush.com'
# app.config['DEBUG'] = True
# SESSION_COOKIE_DOMAIN


jsglue = JSGlue(app)
Pony(app)


def configure_blueprints(app, blueprint, **kwargs):
    app.register_blueprint(blueprint, **kwargs)
    if not blueprint.subdomain and not kwargs.get('subdomain'):
        app.register_blueprint(blueprint, subdomain='www', **kwargs)


configure_blueprints(app, db_bp, url_prefix="/db")
configure_blueprints(app, auth_bp, url_prefix="/")
configure_blueprints(app, general_bp, url_prefix="/")
configure_blueprints(app, order_bp, url_prefix="/order/")
configure_blueprints(app, cart_bp, url_prefix="/cart/")
configure_blueprints(app, products_bp, url_prefix="/products/")
configure_blueprints(app, models_bp, url_prefix="/models/")
configure_blueprints(app, address_bp, url_prefix="/address")
configure_blueprints(app, store_sbp, subdomain="store", url_prefix="/")
configure_blueprints(app, cart_api_bp, url_prefix="/api/cart")
configure_blueprints(app, address_api_bp, url_prefix="/api/address")
configure_blueprints(app, product_api_bp, url_prefix="/api/product")
configure_blueprints(app, general_api_bp, url_prefix="/api/general")
# app.register_blueprint(db_bp, url_prefix="/db")
# app.register_blueprint(auth_bp, url_prefix="/")
# app.register_blueprint(general_bp, url_prefix="/")
# app.register_blueprint(order_bp, url_prefix="/order/")
# app.register_blueprint(cart_bp, url_prefix="/cart/")
# app.register_blueprint(products_bp, url_prefix="/products/")
# app.register_blueprint(models_bp, url_prefix="/models/")
# app.register_blueprint(address_bp, url_prefix="/address")
# app.register_blueprint(store_sbp, subdomain="store", url_prefix="/")
# app.register_blueprint(cart_api_bp, url_prefix="/api/cart")
# app.register_blueprint(address_api_bp, url_prefix="/api/address")
# app.register_blueprint(product_api_bp, url_prefix="/api/product")

app.config['UPLOADED_FILES'] = 'printerush/database/static/files'

lm = LoginManager()


@lm.user_loader
def load_user(wu_id):
    return WebUser.get(id=wu_id)


lm.init_app(app)
lm.login_message_category = 'danger'
lm.login_message = u"Lütfen giriş yapınız."

lm.blueprint_login_views = {
    'store_bp': 'store_sbp.login_page',
    'order_bp': 'auth_bp.login'
}


@app.errorhandler(404)
def unauthorized_access_page(err):
    l = request.url_root.split('.')
    if len(l) == 3:
        t = l[0].split(('://'))
        if len(t) == 2:
            subdomain = t[1]
        elif len(t) == 1:
            subdomain = t[0]
        if subdomain == 'store':
            return redirect(url_for("store_sbp.login_page"))
    else:
        return render_template("error/404.html", page_info=LayoutPI(title="Aradığınız sayfa bulunamadı"))


app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)


# @app.before_request
# def do_something_when_a_request_comes_in():
#     track_visitor()


if __name__ == '__main__':
    app.run()
