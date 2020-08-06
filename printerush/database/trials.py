import locale
from collections import OrderedDict

from pony.orm import db_session

from printerush.database.models import ProductCategory


@db_session
def product_category_choices(root, level=-1):
    ret = [root.id, '-' * level + root.title_key]
    for sub in root.sub_categories_set.order_by(lambda pc: pc.title_key):
        ret += product_category_choices(root=sub, level=level + 1)
    return ret


if __name__ == '__main__':
    # with db_session:
    #     a = product_category_choices(ProductCategory[1])
    #     print(a)
    #     # address = Address[6]
    #     # old_address_dict = address.to_dict(with_collections=True)
    #     # old_address_dict.pop("id")
    #     # old_address_dict.pop("shipped_orders_set")
    #     # old_address_dict.pop("invoiced_orders_set")
    #     # new_address = Address(**old_address_dict)
    #     # address.web_user_ref = None
    #     # address.store_ref = None

    from pyexcel_ods3 import get_data

    data = get_data("Ilce_Listesi.ods")

    country = "Türkiye"
    city = None

    for key in data.keys():
        for line in data[key][:-4]:
            if len(line) == 0:
                continue

            if len(line) == 4 and line[1] == '' and line[2] == '':
                city = line[0]
                continue

            for cell in line:
                if cell == "":
                    continue
                distric = cell
                print(country, city, distric)
                # District(district=cell, city_ref=city)
