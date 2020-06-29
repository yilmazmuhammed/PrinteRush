import iyzipay
from flask import Blueprint, render_template, g, url_for, flash, redirect, request, json
from flask_login import current_user

from printerush.address.assistant_func import country_select_choices
from printerush.address.db import get_address
from printerush.address.exceptions import ThereIsNotAddress
from printerush.address.forms import AddressModalForm
from printerush.common.assistant_func import LayoutPI, get_translation
from printerush.general.requirement import cart_required
from printerush.order.assistanc_func import IyzikoInitialize, IyzikoRetrieve
from printerush.order.db import create_order, get_cart_order, get_order
from printerush.order.forms import ShippingAddressForm

order_bp = Blueprint('order_bp', __name__, template_folder='templates', static_folder='static',
                     static_url_path='assets')


@order_bp.route("/checkout/shipping", methods=["GET", "POST"])
@cart_required
def shipping_page():
    # if current_user.cart_products_set.count() == 0:
    #     return redirect(url_for("general_bp.index"))
    translation = get_translation()["order"]["order"]["shipping_page"]

    sa_form = ShippingAddressForm()
    new_address_form = AddressModalForm(url_for("address_api_bp.new_address_api"))
    new_address_form.country.choices += country_select_choices()

    if sa_form.validate_on_submit():
        try:
            s_address = get_address(sa_form.shipping_address.data)
            i_address = get_address(sa_form.invoicing_address.data)
            create_order(current_user, shipping_address=s_address, invoicing_address=i_address)
            return redirect(url_for("order_bp.order_overview_page"))
        except ThereIsNotAddress as tina:
            flash(tina, "danger")
    g.addresses = current_user.addresses_set
    g.sa_form = sa_form
    g.new_address_form = new_address_form
    cart_sum = 0
    for cp in current_user.cart_products_set:
        cart_sum += cp.quantity * cp.product_ref.main_option.price
    g.products_price = cart_sum
    return render_template("order/shipping.html",
                           page_info=LayoutPI(title=translation["title"]))


@order_bp.route("/checkout/order_overview")
@cart_required
def order_overview_page():
    translation = get_translation()["order"]["order"]["order_overview_page"]

    g.order = get_cart_order(current_user)
    return render_template("order/order_overview.html",
                           page_info=LayoutPI(title=translation["title"]))


token = ""


@order_bp.route("/checkout/payment", methods=["GET"])
@cart_required
def payment_page():
    order = get_cart_order(current_user)

    if request.method == "GET":
        initialize = IyzikoInitialize(current_user, order)
        checkout_form_initialize = iyzipay.CheckoutFormInitialize().create(initialize.request, initialize.options)
        ret = json.loads(checkout_form_initialize.read().decode('utf-8'))
        g.iyziko_js = ret.get("checkoutFormContent")
    # elif request.method == "POST":
    #     retrieve = IyzikoRetrieve(request.form["token"])
    #     checkout_form_result = iyzipay.CheckoutForm().retrieve(retrieve.request, retrieve.options)
    #     ret = json.loads(checkout_form_result.read().decode('utf-8'))
    #     print(ret)
    #     if ret["status"] == "success":
    #         order = get_cart_order(current_user)
    #         order.stage = 1
    #         for cp in current_user.cart_products_set:
    #             cp.delete()
    #         return redirect(url_for("order_bp.order_completed_page"), code=307)
    #     else:
    #         # print(ret)
    #         # TODO ödeme sağlanamadıysa ne olsun
    #         pass
    translation = get_translation()["order"]["order"]["payment_page"]
    return render_template("order/payment.html",
                           page_info=LayoutPI(title=translation["title"]))


@order_bp.route("/checkout/order_completed", methods=["POST"])
@cart_required
def order_completed_page():
    if not request.form.get("token"):
        return redirect(url_for("general_bp.index"))

    retrieve = IyzikoRetrieve(request.form["token"])
    checkout_form_result = iyzipay.CheckoutForm().retrieve(retrieve.request, retrieve.options)
    ret = json.loads(checkout_form_result.read().decode('utf-8'))
    if ret["status"] == "success":
        order = get_cart_order(current_user)
        order.stage = 2
        for cp in current_user.cart_products_set:
            cp.delete()

        order_id = ret["basketId"]

        translation = get_translation()["order"]["order"]["order_completed_page"]
        g.order = get_order(order_id)
        return render_template("order/order_complete.html", page_info=LayoutPI(title=translation["title"]))
    else:
        # print(ret)
        # TODO ödeme sağlanamadıysa ne olsun
        return render_template(url_for("order_bp.shipping_page"))
