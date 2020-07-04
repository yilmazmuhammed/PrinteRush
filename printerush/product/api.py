from flask import Blueprint, jsonify

from printerush.common.assistant_func import get_translation
from printerush.product.db import get_product
from printerush.product.exception import ThereIsNotProduct

product_api_bp = Blueprint('product_api_bp', __name__)


@product_api_bp.route('/product/<int:product_id>')
def get_product_api(product_id):
    # translation = get_translation()['product']['api']['get_product_api']
    try:
        product = get_product(product_id=product_id)
        p_dict = product.to_dict(only="id name short_description_html")
        p_dict["photos_set"] = [{"file_path": photo.file_path} for photo in product.photos_set]
        p_dict["store_ref"] = {"id": product.store_ref.id, "short_name": product.store_ref.short_name}
        p_dict["point"] = round(product.point, 2)
        p_dict["product_code"] = product.product_code
        p_dict["main_option"] = {"price": product.main_option.price, "stock": product.main_option.stock}
        return jsonify(result=True, product=p_dict)
    except ThereIsNotProduct as tinp:
        return jsonify(result=False, err_msg=str(tinp))
