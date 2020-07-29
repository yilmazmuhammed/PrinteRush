from pony.orm import desc

from printerush.address.exceptions import ThereIsNotCountry, ThereIsNotCity, ThereIsNotDistrict, ThereIsNotAddress
from printerush.common.assistant_func import get_translation
from printerush.database.models import Country, City, District, Address


def get_countries():
    return Country.select().order_by(Country.country)


def get_country(country_id):
    translation = get_translation()['address']['db']['get_country']
    country = Country.get(id=country_id)
    if not country:
        raise ThereIsNotCountry(translation["there_is_not_country"])
    return country


def get_city(city_id):
    translation = get_translation()['address']['db']['get_city']
    city = City.get(id=city_id)
    if not city:
        raise ThereIsNotCity(translation["there_is_not_city"])
    return city


def get_district(district_id, city_id, country_id):
    translation = get_translation()['address']['db']['get_district']

    get_filter = "lambda d: d.id == %s" % district_id
    if city_id:
        get_filter += " and d.city_ref.id == %s" % city_id
    if country_id:
        get_filter += " and d.city_ref.country_ref.id == %s" % country_id

    district = District.get(get_filter)
    if not district:
        raise ThereIsNotDistrict(translation["there_is_not_district"])
    return district


def db_add_address(json_address):
    return Address(**json_address)


def get_address(address_id):
    translation = get_translation()['address']['db']['get_address']
    ret = Address.get(id=address_id)
    if not ret:
        raise ThereIsNotAddress(translation["there_is_not_address"])
    return ret


def get_last_address(web_user):
    translation = get_translation()['address']['db']['get_address']
    ret = web_user.addresses_set.order_by(lambda a: desc(a.id)).first()
    if not ret:
        raise ThereIsNotAddress(translation["there_is_not_address"])
    return ret


def remove_address(address):
    if address.is_erasable():
        address.delete()
    else:
        address.web_user_ref = None
        address.store_ref = None
        # # Adresi düzenlerken kullanılacak
        # old_address_dict = address.to_dict(with_collections=True)
        # old_address_dict.pop("id")
        # old_address_dict.pop("shipped_orders_set")
        # old_address_dict.pop("invoiced_orders_set")
        # new_address = Address(**old_address_dict)
        # address.web_user_ref = None
        # address.store_ref = None
        # return new_address
