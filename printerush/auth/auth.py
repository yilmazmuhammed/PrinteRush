from datetime import datetime, timedelta

import jwt
from flask_login import login_user, login_required, logout_user, current_user
from passlib.hash import pbkdf2_sha256 as hasher

from printerush.bots.mail_bot import send_email
from printerush.cart.assistanc_fuct import update_cart
from printerush.common.assistant_func import flask_form_to_dict, FormPI, get_translation, LayoutPI
from printerush.auth.db import db_add_web_user, get_webuser
from printerush.auth.exceptions import RegisterException
from printerush.auth.forms import RegisterForm, LoginForm, UpdateForm, ChangePassword, ForgottenPasswordForm, \
    RenewPasswordForm
from flask import Blueprint, redirect, url_for, flash, render_template, request, g, current_app
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


@auth_bp.route("/forgotten_password/", methods=['GET', 'POST'])
def forgotten_password_page():
    translation = get_translation()["auth"]["auth"]["forgotten_password"]
    form = ForgottenPasswordForm()

    if form.validate_on_submit():
        web_user = get_webuser(email=form.email.data, account_type=0)
        if web_user:
            expiration_time = datetime.now() + timedelta(hours=5)
            info = {
                'email': web_user.email,
                'account_type': web_user.account_type,
                'expiration_time': {
                    "year": expiration_time.year,
                    "month": expiration_time.month,
                    "day": expiration_time.day,
                    "hour": expiration_time.hour,
                    "minute": expiration_time.minute
                }
            }
            token = jwt.encode(info, current_app.secret_key)
            # TODO Mail adresine şifre yenileme linki yolla, form=None yaparak bilgi mesajı ver

            html = """<h3>{first_name} {last_name}</h3>
            <p>PrinteRush hesabının parolasının sıfırlanması için talepte bulunuldu.</p>
            <a href="{url}" ><button type="button">Şifremi sıfırla</button></a>
            <p>Eğer üstteki düğme çalışmazsa aşağıdaki bağlantıyı tarayıcınızın adres çubuğuna yapıştırabilirsiniz:<br>
            <a href="{url}">{url}</a></p>
            <p>Eğer parola sıfırlama talebinde bulunmadıysanız bu epostayı önemsemeyiniz.</p>
            """.format(first_name=web_user.first_name, last_name=web_user.last_name, url=current_app.config['SERVER_NAME']+url_for("auth_bp.renew_password_page", token=token))
            send_email([web_user.email], "Parola sıfırlama", html, message_type="html")

            flash(translation["sent_mail"], "success")
            form = None
        else:
            flash(translation["there_is_not_email"], "danger")

    return render_template("general/general_form.html", page_info=FormPI(title=translation['title'], form=form))


@auth_bp.route("/renew_password/<string:token>", methods=['GET', 'POST'])
def renew_password_page(token):
    translation = get_translation()["auth"]["auth"]["renew_password"]
    form = RenewPasswordForm()
    info = jwt.decode(token, current_app.secret_key)

    if form.validate_on_submit():
        web_user = get_webuser(email=info["email"], account_type=info["account_type"])
        web_user.password_hash = hasher.hash(form.new_password_verification.data)
        return redirect(url_for("auth_bp.login"))

    if datetime.now() > datetime(**info["expiration_time"]):
        flash(translation["expired_link"], "danger")
        form = None
    return render_template("general/general_form.html", page_info=FormPI(title=translation['title'], form=form))
