from flask import Blueprint, redirect, url_for, flash, render_template, request
from flask_login import login_user, login_required, logout_user
from passlib.hash import pbkdf2_sha256 as hasher

from printerush.common.assistant_func import flask_form_to_dict, FormPI, get_translation
from printerush.auth.db import db_add_web_user
from printerush.auth.exceptions import RegisterException
from printerush.auth.forms import RegisterForm, LoginForm
from printerush.database.models import WebUser

auth_bp = Blueprint('auth_bp', __name__, template_folder='templates', static_folder='static', static_url_path='assets')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    translation = get_translation()['auth']['auth']['register']

    if form.validate_on_submit():
        if form.password.data != form.password_verification.data:
            flash(u"%s" % translation['passwords_do_not_match'], 'danger')
        else:
            try:
                json_data = flask_form_to_dict(request_form=request.form, exclude=['password_verification'])
                db_add_web_user(json_webuser=json_data)
                return redirect(url_for('auth_bp.login'))
            except RegisterException as ex:
                flash(u"%s" % ex, 'danger')

    return render_template("auth/register.html", page_info=FormPI(form=form, title=translation['title']))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    translation = get_translation()["auth"]["auth"]["login"]

    if form.validate_on_submit():
        user = WebUser.get(email=form.email.data)
        if user and hasher.verify(form.password.data, user.password_hash) and user.is_active:
            print("Remember", form.remember_me.data)
            login_user(user, remember=form.remember_me.data)
            flash(translation["login_successful"], 'success')
            next_page = request.args.get("next", url_for("general_bp.index"))
            return redirect(next_page)
        elif user and not user.is_active:
            flash(translation["passive_user"], 'danger')
        else:  # If password or username is incorrect
            flash(translation["wrong_password"], 'danger')
    return render_template("auth/login.html", page_info=FormPI(form=form, title=translation['title']))


@login_required
@auth_bp.route("/logout")
def logout():
    logout_user()
    flash(get_translation()["auth"]["auth"]["logout"]["logout_successful"], 'success')
    return redirect(url_for("general_bp.index"))
