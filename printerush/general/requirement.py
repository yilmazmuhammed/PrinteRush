from functools import wraps

from flask import redirect, url_for, request
from flask_login import current_user, login_required


def cart_required(func):
    @wraps(func)
    @login_required
    def decorated_view(*args, **kwargs):
        if current_user.cart_products_set.count() == 0:
            return redirect(url_for("general_bp.index"))
        return func(*args, **kwargs)

    return decorated_view


def url_reformative(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        path = request.path
        if path.count(" ") or not path.islower():
            path = path.casefold().replace(" ", "-")
            args = "&".join([key+"="+value for key, value in request.args.to_dict().items()])
            url = path+"?"+args
            return redirect(url)
        return func(*args, **kwargs)

    return decorated_view
