from flask import request, url_for, redirect, flash, render_template
from flask_login import login_user
from passlib.hash import pbkdf2_sha256

from printerush.auth.db import get_webuser, db_add_web_user
from printerush.auth.exceptions import RegisterException
from printerush.auth.forms import LoginForm, RegisterForm
from printerush.common.assistant_func import get_translation, FormPI, flask_form_to_dict


def login_page():
    form = LoginForm()
    translation = get_translation()["store"]["store_auth"]["login"]

    if form.validate_on_submit():
        user = get_webuser(email=form.email.data, account_type=1)
        if user and pbkdf2_sha256.verify(form.password.data, user.password_hash) and user.is_active:
            login_user(user, remember=form.remember_me.data)
            store_id = user.get_first_store().id
            next_page = request.args.get("next", url_for("store_sbp.dashboard_page", store_id=store_id))
            return redirect(next_page)
        elif user and not user.is_active:
            flash(translation["passive_user"], 'danger')
        else:  # If password or username is incorrect
            flash(translation["wrong_password"], 'danger')
    return render_template("store/auth/login.html", page_info=FormPI(form=form, title=translation['title']))


def register():
    form = RegisterForm()
    translation = get_translation()["store"]["store_auth"]['register']

    if form.validate_on_submit():
        if form.password.data != form.password_verification.data:
            flash(u"%s" % translation['passwords_do_not_match'], 'danger')
        else:
            try:
                json_data = flask_form_to_dict(request_form=request.form, exclude=['password_verification'])
                json_data["account_type"] = 1
                db_add_web_user(json_webuser=json_data)
                flash(translation["success_msg"], 'success')
                return redirect(url_for('auth_bp.login'))
            except RegisterException as ex:
                flash(u"%s" % ex, 'danger')

    return render_template("store/auth/register.html", page_info=FormPI(form=form, title=translation['title']))
