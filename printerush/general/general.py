from flask import Blueprint, render_template, g
from flask_login import current_user

from printerush.assistant_func import LayoutPI
from printerush.database.models import WebUser

general_bp = Blueprint('general_bp', __name__,
                       template_folder='templates',
                       static_folder='static', static_url_path='assets')


@general_bp.route('/')
def index():
    print(current_user.username, current_user.is_active)
    print(WebUser[1].is_active)
    return render_template('general/index.html', page_info=LayoutPI(title="Home page"))
