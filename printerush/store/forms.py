from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.fields.html5 import TelField, EmailField
from wtforms.validators import InputRequired, Length, Email

from printerush.common.assistant_func import get_translation
from printerush.common.forms import form_open, form_close, SubmitField, SelectField


class StoreForm(FlaskForm):
    t = get_translation()['store']['forms']['store_form']

    open = form_open(form_name='form-store')
    close = form_close()

    name = StringField(
        "%s:" % t['name']['label'],
        validators=[InputRequired(t['name']['required']), Length(max=100, message=t['name']['length'])],
        id='name', render_kw={"placeholder": t['name']['label']}
    )

    short_name = StringField(
        "%s:" % t['short_name']['label'],
        validators=[InputRequired(t['short_name']['required']), Length(max=20, message=t['short_name']['length'])],
        id='short_name', render_kw={"placeholder": t['short_name']['label']}
    )

    about_html = TextAreaField(
        "%s:" % t['about_html']['label'],
        id='about_html', render_kw={"placeholder": t['about_html']['label']}
    )

    explanation_html = TextAreaField(
        "%s:" % t['explanation_html']['label'],
        id='explanation_html', render_kw={"placeholder": t['explanation_html']['label']}
    )

    phone_number = TelField(
        "%s:" % t['phone_number']['label'],
        validators=[InputRequired(t['phone_number']['required']), Length(max=20, message=t['phone_number']['length'])],
        id='phone_number', render_kw={"placeholder": t['phone_number']['label']}
    )

    email = EmailField(
        "%s:" % t['email']['label'],
        validators=[
            InputRequired(t['email']['required']),
            Length(max=254, message=t['email']['length']),
            Email(t['email']['required'])
        ],
        id='username', render_kw={"placeholder": t['email']['label']}
    )

    submit = SubmitField(label=t['submit']['label'], render_kw={"class": "btn-color right-side"})


class NewStoreForm(StoreForm):
    t = get_translation()['store']['forms']['new_store_form']

    open = form_open(form_name='form-new_store')
    close = form_close()
    form_title = t['form_title']

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
    submit = SubmitField(label=t['submit']['label'])

