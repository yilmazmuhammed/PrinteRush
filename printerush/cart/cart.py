from flask import Blueprint, render_template

from printerush.common.assistant_func import LayoutPI, get_translation

cart_bp = Blueprint('cart_bp', __name__,
                    template_folder='templates',
                    static_folder='static', static_url_path='assets')


@cart_bp.route("/")
def view_cart():
    title = get_translation()['cart']['cart']['view_cart']['title']
    return render_template("cart/view_cart.html", page_info=LayoutPI(title=title))


# @cart_bp.url_value_preprocessor
# def get_profile_owner(endpoint, values):
#     # query = User.query.filter_by(url_slug=values.pop('user_url_slug'))
#     g.profile_owner = values.pop('user_url_slug')
