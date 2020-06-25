from flask import session
from flask_login import current_user

from printerush.database.models import CartProduct
from printerush.product.db import get_product


def add_to_db_cart(quantity, product_id=None, product=None):
    product = product if product else get_product(product_id=product_id)

    cart_product = CartProduct.get(product_ref=product, web_user_ref=current_user)
    if cart_product:
        cart_product.quantity += quantity
    else:
        cart_product = CartProduct(product_ref=product, quantity=quantity, web_user_ref=current_user)

    return cart_product


def add_to_session_cart(quantity, product_id=None, product=None):
    product = product if product else get_product(product_id=product_id)

    cart_product = cart_product_json(product, quantity)
    if "shopping_cart" in session:
        sc = session["shopping_cart"]
        key = cart_product["product_ref"]["id"]
        for cp in sc:
            if cp["product_ref"]["id"] == key:
                cart_product["quantity"] += cp["quantity"]
                sc.remove(cp)
                break
        sc.append(cart_product)
    else:
        session["shopping_cart"] = [cart_product]

    return cart_product


def update_cart():
    if "shopping_cart" in session:
        s_cart = session["shopping_cart"]
        for cp in s_cart:
            add_to_db_cart(product_id=cp["product_ref"]["id"], quantity=cp["quantity"])
        session.pop("shopping_cart")


def cart_product_json(product, quantity):
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
    return cart_product
