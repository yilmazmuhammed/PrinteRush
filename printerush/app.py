# https://realpython.com/flask-blueprint/#what-a-flask-blueprint-looks-like
# https://github.com/j127/Flask-Blueprint-Example/blob/master/flaskbp/__init__.py
# https://realpython.com/flask-blueprint/#what-a-flask-blueprint-looks-like
import os

from flask import Flask
from flask_jsglue import JSGlue
from flask_login import LoginManager
from pony.flask import Pony

from printerush.address.address import address_bp
from printerush.address.api import address_api_bp
from printerush.auth.auth import auth_bp
from printerush.cart.api import cart_api_bp
from printerush.cart.cart import cart_bp
from printerush.database.models import WebUser
from printerush.general.general import general_bp
from printerush.printable_3d_model.printable_3d_model import models_bp
from printerush.product.product import products_bp

app = Flask(__name__, instance_relative_config=True)
jsglue = JSGlue(app)
Pony(app)

app.secret_key = os.getenv("SECRET_KEY")

app.register_blueprint(auth_bp, url_prefix="/")
app.register_blueprint(general_bp, url_prefix="/")
app.register_blueprint(cart_bp, url_prefix="/cart/")
app.register_blueprint(products_bp, url_prefix="/products/")
app.register_blueprint(models_bp, url_prefix="/models/")
app.register_blueprint(address_bp, url_prefix="/address")
app.register_blueprint(cart_api_bp, url_prefix="/api/cart")
app.register_blueprint(address_api_bp, url_prefix="/api/address")

lm = LoginManager()


@lm.user_loader
def load_user(wu_id):
    return WebUser.get(id=wu_id)


lm.init_app(app)
lm.login_view = "auth_bp.login"
lm.login_message_category = 'danger'

if __name__ == '__main__':
    app.run()
