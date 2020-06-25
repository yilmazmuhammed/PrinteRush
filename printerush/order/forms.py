from flask_wtf import FlaskForm
from wtforms import HiddenField

from printerush.common.forms import form_open, form_close


class ShippingAddressForm(FlaskForm):
    open = form_open(form_name='form-shipping-address', f_id="form-shipping-address")
    close = form_close()
    shipping_address = HiddenField("shipping_address")
    invoicing_address = HiddenField("invoicing_address")
