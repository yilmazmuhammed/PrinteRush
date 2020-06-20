from pony.orm import select

from printerush.address.db import get_district
from printerush.common.assistant_func import flask_form_to_dict
from printerush.database.models import Country


def country_select_choices():
    cities = select((c.id, c.country) for c in Country)

    ret = []
    for c_id, country in cities:
        ret.append((c_id, country))

    return ret


def create_address_json(flask_form, request_form, web_user=None, store=None):
    district = get_district(flask_form.district.data, flask_form.city.data, flask_form.country.data)
    exclude = ['country', 'city', 'district', 'is_invoice_address']
    if not flask_form.is_invoice_address.data or flask_form.invoice_type.data == 1:
        exclude += ["company_name", "tax_number", "tax_office"]
    json_data = flask_form_to_dict(request_form=request_form, exclude=exclude)
    json_data['district_ref'] = district
    if not flask_form.is_invoice_address.data:
        json_data['invoice_type'] = 0
    if web_user:
        json_data['web_user_ref'] = web_user
    if store:
        json_data['store_ref'] = store
    return json_data
