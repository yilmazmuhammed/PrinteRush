from flask import Blueprint, render_template, url_for
from flask_login import login_required

from printerush.address.assistant_func import country_select_choices, create_address_json
from printerush.address.forms import AddressModalForm
from printerush.common.assistant_func import FormPI, get_translation

address_bp = Blueprint('address_bp', __name__, template_folder='templates', static_folder='static',
                       static_url_path='assets')


@address_bp.route("/new_address")
@login_required
def new_address_page():
    form = AddressModalForm(url_for("address_api_bp.new_address_api"))
    form.country.choices += country_select_choices()

    for field in form:
        print(field, field.errors)
    title = get_translation()["address"]["address"]["new_address"]["title"]
    return render_template("address/address_deneme.html", page_info=FormPI(form=form, title=title))
