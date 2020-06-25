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
    @login_required
    def decorated_view(*args, **kwargs):
        url = request.path
        if url.count(" ") or not url.islower():
            return redirect(url.casefold().replace(" ", "-"))
        return func(*args, **kwargs)

    return decorated_view