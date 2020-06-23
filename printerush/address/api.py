from flask import Blueprint, request, jsonify

from printerush.address.db import get_country, get_city, get_district
from printerush.address.exceptions import ThereIsNotCountry
from printerush.address.forms import AddressForm

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