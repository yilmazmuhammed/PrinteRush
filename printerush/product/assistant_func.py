from printerush.common.assistant_func import FormPI


class ProductPI(FormPI):
    def __init__(self, product, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.product = product


class ProductCategoryPI(FormPI):
    def __init__(self, category, products, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.products = products
        self.category = category


def detect_sorting_and_filtering(**kwargs):
    sorting = "lambda p: ("
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
