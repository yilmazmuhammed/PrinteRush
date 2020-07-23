import os
import pathlib

from flask import current_app, url_for
from werkzeug.utils import secure_filename

from printerush.common.assistant_func import get_translation
from printerush.database.models import Product, ProductCategory, DataStatus, ProductOption, Printable3dModel
from printerush.product.exception import ThereIsNotProduct


def get_product(product_id):
    translation = get_translation()['product']['db']['get_product']
    p = Product.get(id=product_id)
    if p is None:
        raise ThereIsNotProduct(translation['there_is_not_product'])
    return p


def get_root_category():
    return ProductCategory[1]


def db_add_product(dict_product, creator_ref):
    price = dict_product.pop('price')
    stock = dict_product.pop('stock')
    dict_product['data_status_ref'] = DataStatus(creator_ref=creator_ref)
    product = Product(**dict_product)
    ProductOption(product_ref=product, price=price, stock=stock)
    return product


def db_add_printable_3d_models(models, product):
    ret = []
    for model in models:
        filename = secure_filename(model.filename)
        task = os.path.join('printable_3d_models', "product", product.id)
        directory_path = os.path.join(current_app.config['UPLOADED_FILES'], task)
        pathlib.Path(directory_path).mkdir(exist_ok=True)
        model.save(os.path.join(directory_path, filename))
        ret.append(Printable3dModel(file_path=os.path.join(url_for('db_bp.static', filename='files'), task, filename),
                                    product_ref=product))

