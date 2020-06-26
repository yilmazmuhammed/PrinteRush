from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from printerush.address.assistant_func import create_address_json
from printerush.address.db import get_country, get_city, db_add_address, get_last_address, get_address, remove_address
from printerush.address.exceptions import ThereIsNotCountry, ThereIsNotDistrict, ThereIsNotAddress
from printerush.address.forms import AddressModalForm
from printerush.common.assistant_func import get_translation

address_api_bp = Blueprint('address_api_bp', __name__)


@address_api_bp.route('/cities')
def cities_api():
    country_id = int(request.args.get('country_id', 0))

    try:
        country = get_country(country_id)
        cities = []
        for c in country.cities_set:
            cities.append(c.to_dict(exclude='country_ref'))
        return jsonify(result=True, country=country.to_dict(), cities=cities)
    except ThereIsNotCountry as tinc:
        return jsonify(result=False, err_msg=str(tinc))


@address_api_bp.route('/counties')
def counties_api():
    city_id = int(request.args.get('city_id', 0))

    try:
        city = get_city(city_id)
        counties = []
        for c in city.districts_set:
            counties.append(c.to_dict(exclude='city_ref'))
        return jsonify(result=True, city=city.to_dict(), counties=counties)
    except ThereIsNotCountry as tinc:
        return jsonify(result=False, err_msg=str(tinc))


@address_api_bp.route("/new_address", methods=["POST"])
@login_required
def new_address_api():
    translation = get_translation()["address"]["api"]["new_address_api"]

    form = AddressModalForm()

    if form.validate_on_submit():
        try:
            json_data = create_address_json(form, request.form, web_user=current_user)
            address = db_add_address(json_data)
            return jsonify(result=True, msg=translation["success_msg"], address=address.to_dict())
        except ThereIsNotDistrict as tisd:
            return jsonify(result=False, validate_on_submit=True, err_msg=str(tisd), address_id=address.id)

    errors = []
    for field in form:
        errors += field.errors
    return jsonify(result=False, validate_on_submit=False, errors=errors)


@address_api_bp.route("/get_last_address", methods=["GET"])
@login_required
def get_last_address_api():
    try:
        address = get_last_address(current_user)
        ret = address.to_dict(
            "id title first_name last_name address_detail phone_number invoice_type company_name tax_number tax_office"
        )
        ret["district_ref"] = {
            "district": address.district_ref.district,
            "city_ref": {
                "city": address.district_ref.city_ref.city,
                "country_ref": {
                    "country": address.district_ref.city_ref.country_ref.country
                }
            }
        }
        return jsonify(result=True, address=ret)
    except ThereIsNotAddress as tisa:
        return jsonify(result=False, err_msg=str(tisa))


@address_api_bp.route("/remove_address/<int:address_id>", methods=["GET"])
@login_required
def remove_address_api(address_id):
    translation = get_translation()["address"]["api"]["remove_address_api"]
    try:
        address = get_address(address_id)
        if address.web_user_ref != current_user:
            return jsonify(result=False, err_msg=translation["web_user_address_mismatch"])
        remove_address(address)
        return jsonify(result=True, msg=translation["success_msg"])
    except ThereIsNotAddress as tina:
        return jsonify(result=False, err_msg=str(tina))
