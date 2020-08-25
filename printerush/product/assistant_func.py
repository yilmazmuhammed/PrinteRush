from printerush.common.assistant_func import FormPI
from printerush.product.db import get_root_category


class ProductPI(FormPI):
    def __init__(self, product, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.product = product


class ProductCategoryPI(FormPI):
    def __init__(self, category, products, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.products = products
        self.category = category


def product_category_choices(root=None, level=-1):
    root = root if root is not None else get_root_category()

    ret = [(root.id, '--'*level+" "+root.title_key)]
    for sub in root.sub_categories_set.order_by(lambda pc: pc.title_key):
        ret += product_category_choices(root=sub, level=level+1)
    return ret


def detect_sorting_and_filtering(**kwargs):
    sorting = "lambda p: (desc(int(bool(p.stock))),"
    filtering = "lambda p: True"

    if kwargs.get("min_price"):
        filtering += " and p.max_price >= %s" % (kwargs.get("min_price"),)
    if kwargs.get("max_price"):
        filtering += " and p.min_price <= %s" % (kwargs.get("max_price"),)
    if kwargs.get("min_point"):
        filtering += " and p.point >= %s" % (int(kwargs.get("min_point")),)

    if kwargs.get("sort"):
        value = kwargs.get("sort")
        if value[:10] == "descending":
            sorting += "desc(p.%s)"
            value = value[11:]
        elif value[:9] == "ascending":
            sorting += "p.%s"
            value = value[10:]

        if value == "name":
            sorting %= "name"
        elif value == "price":
            sorting %= "min_price"
        elif value == "point":
            sorting %= "point"
        elif value == "sold":
            sorting %= "sold"
        sorting += ",)"
    else:
        sorting += "desc(p.sold),)"

    return sorting, filtering
