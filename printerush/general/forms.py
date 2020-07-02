from wtforms import SubmitField
from flask_wtf import FlaskForm
from printerush.common.assistant_func import get_translation
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length, Email
from wtforms.fields.html5 import EmailField, TelField

from printerush.common.forms import form_open, form_close


class SubmitField(SubmitField):
    def __call__(self, *args, **kwargs):
        return '<button name="' + self.id + '" type="submit" class="btn-color right-side">' + \
               self.label.text + '</button>'


class ContactUserForm(FlaskForm):
    t = get_translation()['auth']['forms']['contact_user']
    open = form_open(form_name='form-update')
    close = form_close()
    first_name = StringField(
        "%s:" % t['first_name']['label'],
        validators=[InputRequired(t['first_name']['required']), Length(max=40, message=t['first_name']['length'])],
        id='first_name', render_kw={"placeholder": t['first_name']['label']}
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

    phone_number = TelField(
        "%s:" % t['phone_number']['label'],
        validators=[Length(max=20, message=t['phone_number']['length'])],
        id='phone_number', render_kw={"placeholder": t['phone_number']['label']}
    )

    message = TextAreaField(
        "%s:" % t['message']['label'],
        validators=[InputRequired(t['message']['required']), Length(min=20, message=t['message']['length'])],
        id='message', render_kw={"placeholder": t['message']['label']}
    )
    submit = SubmitField(label=t['submit']['label'], render_kw={"class": "btn-color right-side"})
