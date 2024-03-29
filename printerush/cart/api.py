from flask import Blueprint, jsonify, request, session, url_for, current_app
from flask_login import current_user

from printerush.bots.mail_bot import send_email
from printerush.cart.assistanc_fuct import add_to_db_cart, add_to_session_cart, cart_product_json
from printerush.cart.exception import NoStock
from printerush.common.assistant_func import get_translation
from printerush.database.models import CartProduct
from printerush.product.db import get_product
from printerush.product.exception import ThereIsNotProduct

cart_api_bp = Blueprint('cart_api_bp', __name__)


@cart_api_bp.route('/')
def cart():
    cart_ = []
    if current_user.is_authenticated:
        for cp in current_user.cart_products_set.order_by(lambda cp: cp.product_ref.id):
            cart_.append(cart_product_json(product=cp.product_ref, quantity=cp.quantity))
    else:
        cart_ = sorted(session["shopping_cart"],
                       key=lambda k: k["product_ref"]["id"]) if "shopping_cart" in session else []
    return jsonify(result=True, cart=cart_)


@cart_api_bp.route('/cart')
def add_to_cart():
    translation = get_translation()['cart']['api']['add_to_cart']
    product_id = request.args.get('product_id', 0)
    quantity = int(request.args.get('quantity', 0))
    if quantity == 0:
        return jsonify(result=False, err_msg=translation["quantity_less_than_zero"])
    try:
        product = get_product(product_id=product_id)
        if current_user.is_authenticated:
            add_to_db_cart(product=product, quantity=quantity)
        else:
            add_to_session_cart(product=product, quantity=quantity)
        return jsonify(result=True, msg=translation["success_msg"])
    except (NoStock, ThereIsNotProduct) as e:
        return jsonify(result=False, err_msg=str(e))


@cart_api_bp.route('/remove_from_cart')
def remove_from_cart():
    translation = get_translation()['cart']['api']['remove_from_cart']
    product_id = int(request.args.get('product_id', 0))
    quantity = int(request.args.get('quantity', 0))

    try:
        if current_user.is_authenticated:
            product = get_product(product_id=product_id)
            cart_product = CartProduct.get(product_ref=product, web_user_ref=current_user)
            if quantity == 0 or quantity >= cart_product.quantity:
                cart_product.delete()
            else:
                cart_product.quantity -= quantity
        else:
            if "shopping_cart" in session:
                sc = session["shopping_cart"]
                for cp in sc:
                    if cp["product_ref"]["id"] == product_id:
                        if quantity == 0 or quantity >= cp["quantity"]:
                            sc.remove(cp)
                        else:
                            cp["quantity"] -= quantity
                        break
        return jsonify(result=True, msg=translation["success_msg"])
    except ThereIsNotProduct as tinp:
        return jsonify(result=False, err_msg=str(tinp))


@cart_api_bp.route('/cart_product/<int:product_id>')
def cart_product(product_id):
    translation = get_translation()['cart']['api']['cart_product']
    try:
        cp_json = None
        product = get_product(product_id=product_id)
        if current_user.is_authenticated:
            cart_product = CartProduct.get(product_ref=product, web_user_ref=current_user)
            cp_json = cart_product_json(product, cart_product.quantity)
        else:
            if "shopping_cart" in session:
                sc = session["shopping_cart"]
                for cp in sc:
                    if cp["product_ref"]["id"] == product_id:
                        cp_json = cp
                        break
        if cp_json:
            return jsonify(result=True, cart_product=cp_json)
        else:
            return jsonify(result=False, err_msg=translation["there_is_no_cart_product"])
    except ThereIsNotProduct as tinp:
        return jsonify(result=False, err_msg=str(tinp))


@cart_api_bp.route('/stock_subscribe')
def stock_subscribe_api():
    translation = get_translation()['cart']['api']['stock_subscribe_api']

    email = request.args.get("email", None)
    product_id = request.args.get("product_id", None)
    product_url = current_app.config['SERVER_NAME'] + url_for("products_bp.view", product_id=product_id)

    try:
        msg = translation["mail_msg"].format(email=email, product_id=product_id, product_url=product_url)
        send_email(["iletisim@printerush.com"], subject=translation["subject"], message=msg)
        return jsonify(result=True, msg=translation["success_msg"])
    except Exception as e:
        return jsonify(result=False, err_msg=str(e))
