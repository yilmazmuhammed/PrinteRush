from flask import Blueprint, render_template

from printerush.common.assistant_func import LayoutPI

general_bp = Blueprint('general_bp', __name__,
                       template_folder='templates',
                       static_folder='static', static_url_path='assets')


@general_bp.route('/')
def index():
    return render_template('general/index.html', page_info=LayoutPI(title="Home page"))
