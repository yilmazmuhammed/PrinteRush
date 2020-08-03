from flask import Blueprint, redirect, url_for, render_template, g

from printerush.bots.mail_bot import send_email
from printerush.common.assistant_func import LayoutPI, FormPI
from printerush.general.forms import ContactUserForm
from printerush.product.db import get_root_category

general_bp = Blueprint('general_bp', __name__,
                       template_folder='templates',
                       static_folder='static', static_url_path='general/assets')


@general_bp.route('/')
def index():
    g.new_arrivals = get_root_category().products(sort_by="lambda p: p.data_status_ref.confirmation_time")[:20]
    g.best_seller = get_root_category().products(sort_by="lambda p: desc(p.sold)")[:20]
    return render_template('general/index.html', page_info=LayoutPI(title="Ana Sayfa"))


@general_bp.route('/about')
def about():
    return render_template('general/about.html', page_info=LayoutPI(title="Hakkımızda"))


@general_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactUserForm()

    if form.validate_on_submit():
        data = {
            "first_name": form.first_name.data,
            "email": form.email.data,
            "phone_number": form.phone_number.data,
            "message": form.message.data
        }
        msg = "Gönderen: {first_name} \n" \
              "Mail: {email}\n" \
              "Telefon: {phone_number}\n" \
              "Mesaj: {message}".format(**data)

        send_email(["iletisim@printerush.com"], subject="İletişim", message=msg)

        return redirect(url_for('general_bp.contact'))

    return render_template('general/contact.html', page_info=FormPI(title="İletişim Kur", form=form))
