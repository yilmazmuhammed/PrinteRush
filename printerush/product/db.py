from printerush.common.assistant_func import get_translation
from printerush.database.models import Product
from printerush.product.exception import ThereIsNotProduct


def get_product(product_id):
    translation = get_translation()['product']['db']['get_product']
    p = Product.get(id=product_id)
    if p is None:
        raise ThereIsNotProduct(translation['there_is_not_product'])
    return p
