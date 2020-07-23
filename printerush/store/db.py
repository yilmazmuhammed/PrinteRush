from printerush.common.assistant_func import get_translation
from printerush.database.models import DataStatus, Store, Address, StoreAuthorization
from printerush.store.exceptions import ThereIsNotStore


def db_add_store(json_store, creator_ref, admin_ref=None):
    json_store['data_status_ref'] = DataStatus(creator_ref=creator_ref)
    json_store['address_ref'] = Address(title="Mağaza adresi",
                                        district_ref=json_store.pop("district"),
                                        address_detail=json_store.pop("address_detail"),
                                        phone_number=json_store.get("phone_number"),
                                        invoice_type=0
                                        )
    json_store.pop("country")
    json_store.pop("city")

    store = Store(**json_store)

    # TODO acaba burada mı yoksa mağazayı onaylarken mi yapılmalı
    if admin_ref:
        StoreAuthorization(authorization="Yönetici", is_admin=True, web_users_set=[admin_ref], store_ref=store)

    return store


def get_store(store_id):
    translation = get_translation()['store']['db']['get_store']
    store = Store.get(id=store_id)
    if not store:
        raise ThereIsNotStore(translation["there_is_not_store"])
    return store
