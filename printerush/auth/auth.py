from flask_login import login_user, login_required, logout_user, current_user
from passlib.hash import pbkdf2_sha256 as hasher
from printerush.cart.assistanc_fuct import update_cart
from printerush.common.assistant_func import flask_form_to_dict, FormPI, get_translation, LayoutPI
from printerush.auth.db import db_add_web_user, get_webuser
from printerush.auth.exceptions import RegisterException
from printerush.auth.forms import RegisterForm, LoginForm, UpdateForm, ChangePassword
from flask import Blueprint, redirect, url_for, flash, render_template, request, g
from printerush.address.forms import AddressModalForm
from printerush.address.assistant_func import country_select_choices

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
                flash(translation["success_msg"], 'success')
                return redirect(url_for('auth_bp.login'))
            except RegisterException as ex:
                flash(u"%s" % ex, 'danger')

    return render_template("auth/register.html", page_info=FormPI(form=form, title=translation['title']))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    translation = get_translation()["auth"]["auth"]["login"]

    if form.validate_on_submit():
        user = get_webuser(email=form.email.data, account_type=0)
        if user and hasher.verify(form.password.data, user.password_hash) and user.is_active:
            login_user(user, remember=form.remember_me.data)
            update_cart()
            # flash(translation["login_successful"], 'success')
            next_page = request.args.get("next", url_for("general_bp.index"))
            return redirect(next_page)
        elif user and not user.is_active:
            flash(translation["passive_user"], 'danger')
        else:  # If password or username is incorrect
            flash(translation["wrong_password"], 'danger')
    return render_template("auth/login.html", page_info=FormPI(form=form, title=translation['title']))


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    # flash(get_translation()["auth"]["auth"]["logout"]["logout_successful"], 'success')
    return redirect(url_for("general_bp.index"))


@auth_bp.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form_1 = UpdateForm()
    form_2 = ChangePassword()
    g.form_1 = form_1
    g.form_2 = form_2
    g.tab = 1 if not request.args.get("tab") else int(request.args.get("tab"))
    g.addresses = current_user.addresses_set
    g.new_address_form = AddressModalForm(url_for("address_api_bp.new_address_api"))
    g.new_address_form.country.choices += country_select_choices()
    translation = get_translation()["auth"]["auth"]["account"]

    if form_1.validate_on_submit():
        form_2.error = []
        if hasher.verify(form_1.password.data, current_user.password_hash):
            current_user.first_name = form_1.first_name.data
            current_user.last_name = form_1.last_name.data
            current_user.email = form_1.email.data
            current_user.phone_number = form_1.phone_number.data

            flash(get_translation()["auth"]["auth"]["account"]["password_update_successful"], 'success')
            return redirect(url_for("auth_bp.account", tab=2))
        else:
            flash(u"%s" % translation['wrong_password'], 'danger')

    form_1.first_name.data = current_user.first_name
    form_1.last_name.data = current_user.last_name
    form_1.email.data = current_user.email
    form_1.phone_number.data = current_user.phone_number

    if form_2.validate_on_submit():
        form_1.error = []
        if hasher.verify(form_2.password.data, current_user.password_hash):
            if form_2.new_password_verification.data == form_2.new_password.data:

                current_user.password_hash = hasher.hash(form_2.new_password_verification.data)
                flash(get_translation()["auth"]["auth"]["account"]["password_update_successful"], 'success')
                return redirect(url_for("auth_bp.account", tab=4))
            else:
                flash(u"%s" % translation['passwords_do_not_match'], 'danger')
        else:
            flash(u"%s" % translation['wrong_password'], 'danger')

    g.orders = current_user.orders_set
    return render_template("auth/account.html", page_info=FormPI(title=translation['title'], form=form_1))
