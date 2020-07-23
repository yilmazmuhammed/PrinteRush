from functools import wraps

from flask import request, current_app, g, redirect, url_for, flash, abort
from flask_login import current_user
from flask_login.config import EXEMPT_METHODS
from pony.orm import select

from printerush.common.assistant_func import get_translation
from printerush.store.db import get_store
from printerush.store.exceptions import ThereIsNotStore


def store_login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        try:
            g.store = get_store(store_id=kwargs['store_id'])
            g.slt = get_translation()["store"]["layout"]
        except ThereIsNotStore:
            abort(404)

        if request.method in EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif current_app.config.get('LOGIN_DISABLED'):
            return func(*args, **kwargs)
        elif not current_user.is_authenticated or current_user.account_type != 1:
            return current_app.login_manager.unauthorized()
        return func(*args, **kwargs)

    return decorated_view


def store_authorization_required(is_admin=False):
    def sar_decorator(func):
        @store_login_required
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if current_user.is_admin:
                return func(*args, **kwargs)
            elif kwargs['store_id'] not in [store.id for store in current_user.authorized_stores()]:
                flash(u"Bu sayfaya giriş yetkiniz yok.", 'danger')
                return current_app.login_manager.unauthorized()
            else:
                sa = current_user.store_authorizations_set.select(lambda sa: sa.store_ref == g.store).get()
                if not sa.is_admin and not (sa.is_admin >= is_admin):
                    #     if not sa.is_admin and not (ma.is_admin >= is_admin
                    #                             and ma.reading_transaction >= reading_transaction
                    #                             and ma.writing_transaction >= writing_transaction
                    #                             and ma.adding_member >= adding_member
                    #                             and ma.throwing_member >= throwing_member):
                    #     # TODO yetkilere göre sayfa
                    flash(u"Bu sayfaya giriş yetkiniz yok.", 'danger')
                    return current_app.login_manager.unauthorized()
            return func(*args, **kwargs)

        return decorated_view

    return sar_decorator
