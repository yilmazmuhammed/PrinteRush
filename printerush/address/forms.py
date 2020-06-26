from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, RadioField, TextAreaField
from wtforms.fields.html5 import TelField
from wtforms.validators import InputRequired, Length

from printerush.common.assistant_func import get_translation
from printerush.common.forms import form_open, form_close, SelectField, SubmitField


class AddressForm(FlaskForm):
    t = get_translation()['address']['forms']['address']

    open = form_open(form_name='form-address')
    close = form_close()
    form_title = t['form_title']

    title = StringField(
        label="%s:" % t['title']['label'],
        validators=[InputRequired(t['title']['required']), Length(max=40, message=t['title']['length'])],
        id='title', render_kw={"placeholder": t['title']['label']}
    )

    first_name = StringField(
        label="%s:" % t['first_name']['label'],
        validators=[InputRequired(t['first_name']['required']), Length(max=40, message=t['first_name']['length'])],
        id='first_name', render_kw={"placeholder": t['first_name']['label']}
    )

    last_name = StringField(
        label="%s:" % t['last_name']['label'],
        validators=[InputRequired(t['last_name']['required']), Length(max=40, message=t['last_name']['length'])],
        id='last_name', render_kw={"placeholder": t['last_name']['label']}
    )

    country = SelectField(
        label="%s:" % t['country']['label'],
        validators=[InputRequired(t['country']['required'])], validate_choice=False,
        coerce=int, choices=[('', t['country']['please_select'])],
        id='country', render_kw={"placeholder": t['country']['label'], "class": "form-control"}
    )

    city = SelectField(
        label="%s:" % t['city']['label'],
        validators=[InputRequired(t['city']['required'])], validate_choice=False,
        coerce=int, choices=[('', t['city']['please_select'])],
        id='city', render_kw={"placeholder": t['city']['label'], "class": "form-control"}
    )

    district = SelectField(
        label="%s:" % t['district']['label'],
        validators=[InputRequired(t['district']['required'])], validate_choice=False,
        coerce=int, choices=[('', t['district']['please_select'])],
        id='district', render_kw={"placeholder": t['district']['label'], "class": "form-control"}
    )

    address_detail = TextAreaField(
        label="%s:" % t['address_detail']['label'],
        validators=[
            InputRequired(t['address_detail']['required']),
            Length(max=1000, message=t['address_detail']['length'])
        ],
        id='address_detail', render_kw={"placeholder": t['address_detail']['label']}
    )

    phone_number = TelField(
        label="%s:" % t['phone_number']['label'],
        validators=[
            InputRequired(t['address_detail']['required']),
            Length(max=20, message=t['phone_number']['length'])
        ],
        id='phone_number', render_kw={"placeholder": t['phone_number']['label']}
    )

    is_invoice_address = BooleanField(
        label=t['is_invoice_address']['label'], id='is_invoice_address', default=True,
        render_kw={"class": "checkbox"}
    )

    invoice_type = RadioField(
        label="%s:" % t['invoice_type']['label'],
        choices=[(1, t['invoice_type']['individual']), (2, t['invoice_type']['corporate'])], default=1, coerce=int,
        id='invoice_type', render_kw={"class": "radio-button"}
    )

    company_name = StringField(
        label="%s:" % t['company_name']['label'],
        validators=[Length(max=100, message=t['company_name']['length'])],
        id='company_name', render_kw={"placeholder": t['company_name']['label']}
    )

    tax_number = StringField(
        label="%s:" % t['tax_number']['label'],
        validators=[Length(max=20, message=t['tax_number']['length'])],
        id='tax_number', render_kw={"placeholder": t['tax_number']['label']}
    )

    tax_office = StringField(
        label="%s:" % t['tax_office']['label'],
        validators=[Length(max=50, message=t['tax_office']['length'])],
        id='tax_office', render_kw={"placeholder": t['tax_office']['label']}
    )

    submit = SubmitField(label=t['submit']['label'], render_kw={"class": "btn-color right-side"})


class AddressModalForm(AddressForm):
    def __init__(self, url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.open = form_open(form_name='modal-form-address', f_action=url)
