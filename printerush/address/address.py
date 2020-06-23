from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user

from printerush.address.assistant_func import country_select_choices, create_address_json
from printerush.address.db import db_add_address
from printerush.address.exceptions import ThereIsNotDistrict
from printerush.address.forms import AddressModalForm
from printerush.common.assistant_func import FormPI, get_translation

address_bp = Blueprint('address_bp', __name__, template_folder='templates', static_folder='static',
                       static_url_path='assets')


@address_bp.route("/new_address", methods=["GET"])
@login_required
def new_address_page():
    form = AddressModalForm()
    form.country.choices += country_select_choices()

    if form.validate_on_submit():
        print("ok")
    for field in form:
        print(field, field.errors)
    title = get_translation()["address"]["address"]["new_address"]["title"]
    return render_template("address/address_deneme.html", page_info=FormPI(form=form, title=title))


@address_bp.route("/new_address", methods=["POST"])
@login_required
def new_address_page_post():
    translation = get_translation()["address"]["address"]["new_address"]

    form = AddressModalForm()

    if form.validate_on_submit():
        try:
            json_data = create_address_json(form, request.form, web_user=current_user)
            address = db_add_address(json_data)
            return jsonify(result=True, msg=translation["success_msg"], address=address.to_dict())
        except ThereIsNotDistrict as tisd:
            return jsonify(result=False, validate_on_submit=True, err_msg=str(tisd))

    errors = []
    for field in form:
        errors += field.errors
    return jsonify(result=False, validate_on_submit=False, errors=errors)
