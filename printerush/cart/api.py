from flask import Blueprint, jsonify, request, session
from flask_login import current_user

from printerush.common.assistant_func import get_translation
from printerush.database.models import CartProduct
from printerush.product.db import get_product
from printerush.product.exception import ThereIsNotProduct

cart_api_bp = Blueprint('cart_api_bp', __name__)


@cart_api_bp.route('/add_product_to_cart')
def add_product_to_cart():
    translation = get_translation()['cart']['api']['add_product_to_cart']
    product_id = request.args.get('product_id', 0)
    quantity = int(request.args.get('quantity', 0))
    try:
        product = get_product(product_id=product_id)
        if current_user.is_authenticated:
            cart_product = CartProduct.get(product_ref=product, web_user_ref=current_user)
            if cart_product:
                cart_product.quantity += quantity
            else:
                cart_product = CartProduct(product_ref=product, quantity=quantity, web_user_ref=current_user)
        else:
            cart_product = {
                "product_ref": {
                    "id": product.id,
                    "name": product.name,
                    "main_photo": {
                        "file_path": product.main_photo.file_path
                    },
                    "main_option": {
                        "price": product.main_option.price
                    }
                },
                "quantity": quantity
            }
            if "shopping_cart" in session:
                sc = session["shopping_cart"]
                key = cart_product["product_ref"]["id"]
                eklendi = False
                for cp in sc:
                    if cp["product_ref"]["id"] == key:
                        cart_product["quantity"] += cp["quantity"]
                        sc.remove(cp)
                        break
                sc.append(cart_product)
            else:
                session["shopping_cart"] = [cart_product]
            print("Son:", session.get("shopping_cart"))
        return jsonify(result=True, msg=translation["success_msg"])
    except ThereIsNotProduct as tinp:
        return jsonify(result=False, err_msg=str(tinp))
