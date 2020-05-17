# https://realpython.com/flask-blueprint/#what-a-flask-blueprint-looks-like
# https://github.com/j127/Flask-Blueprint-Example/blob/master/flaskbp/__init__.py
# https://realpython.com/flask-blueprint/#what-a-flask-blueprint-looks-like
import os

from flask import Flask
from flask_login import LoginManager
from pony.flask import Pony

from printerush.auth.auth import auth_bp
from printerush.database.models import WebUser
from printerush.general.general import general_bp
from printerush.products.products import products_bp

app = Flask(__name__, instance_relative_config=True)
Pony(app)

app.secret_key = os.getenv("SECRET_KEY")

app.register_blueprint(auth_bp, url_prefix="/")
app.register_blueprint(general_bp, url_prefix="/")
app.register_blueprint(products_bp, url_prefix="/as/<language_id>")

lm = LoginManager()


@lm.user_loader
def load_user(wu_id):
    return WebUser.get(id=wu_id)


lm.init_app(app)
lm.login_view = "Login Page"
lm.login_message_category = 'danger'

if __name__ == '__main__':
    app.run()
