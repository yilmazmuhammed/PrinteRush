from pony.orm import db_session

from printerush.database.models import Address

if __name__ == '__main__':
    with db_session:
        address = Address[6]
        old_address_dict = address.to_dict(with_collections=True)
        old_address_dict.pop("id")
        old_address_dict.pop("shipped_orders_set")
        old_address_dict.pop("invoiced_orders_set")
        new_address = Address(**old_address_dict)
        address.web_user_ref = None
        address.store_ref = None
