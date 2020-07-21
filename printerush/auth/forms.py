from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import EmailField, TelField
from wtforms.validators import InputRequired, Length, EqualTo, Email

from printerush.common.assistant_func import get_translation


def form_open(form_name, f_id=None, enctype=None, f_action=""):
    f_open = """<form action="%s" method="post" name="%s" """ % (f_action, form_name,)

    if f_id:
        f_open += """ id="%s" """ % (f_id,)
    if enctype:
        f_open += """ enctype="%s" """ % (enctype,)

    f_open += """class="main-form full">"""

    return f_open


def form_close():
    return """</form>"""


class SubmitField(SubmitField):
    def __call__(self, *args, **kwargs):
        return '<button name="' + self.id + '" type="submit" class="btn-color right-side">' + \
               self.label.text + '</button>'


class WebUserForm(FlaskForm):
    t = get_translation()['auth']['forms']['web_user']

    first_name = StringField(
        "%s:" % t['first_name']['label'],
        validators=[InputRequired(t['first_name']['required']), Length(max=40, message=t['first_name']['length'])],
        id='first_name', render_kw={"placeholder": t['first_name']['label']}
    )

    last_name = StringField(
        "%s:" % t['last_name']['label'],
        validators=[InputRequired(t['last_name']['required']), Length(max=40, message=t['last_name']['length'])],
        id='last_name', render_kw={"placeholder": t['last_name']['label']}
    )

    email = EmailField(
        "%s:" % t['email']['label'],
        validators=[
            InputRequired(t['email']['required']),
            Length(max=254, message=t['email']['length']),
            Email(t['email']['required'])
        ],
        id='email', render_kw={"placeholder": t['email']['label']}
    )

    phone_number = TelField(
        "%s:" % t['phone_number']['label'],
        validators=[Length(max=20, message=t['phone_number']['length'])],
        id='phone_number', render_kw={"placeholder": t['phone_number']['label']}
    )

    password = PasswordField(
        "%s:" % t['password']['label'],
        validators=[InputRequired(t['password']['required']), Length(max=30, message=t['password']['length'])],
        id='password', render_kw={"placeholder": t['password']['label']}
    )

    password_verification = PasswordField(
        "%s:" % t['password_verification']['label'],
        validators=[InputRequired(t['password_verification']['required']),
                    Length(max=20, message=t['password_verification']['length']),
                    EqualTo('password', message=t['password_verification']['password_equal_to'])],
        id='password_verification', render_kw={"placeholder": t['password_verification']['label']}
    )

    is_admin = BooleanField(
        label="%s:" % t['is_admin']['label'], id='is_admin',
        render_kw={"class": "checkbox"}
    )

    is_active = BooleanField(
        label="%s:" % t['is_active']['label'], id='is_active',
        render_kw={"data-toggle": "toggle", "data-onstyle": "success"}
    )

    submit = SubmitField(label=t['submit']['label'], render_kw={"class": "btn-color right-side"})


class RegisterForm(WebUserForm):
    t = get_translation()['auth']['forms']['register']

    open = form_open(form_name='form-register')
    close = form_close()
    form_title = t['form_title']

    is_admin = None
    is_active = None

    submit = SubmitField(label=t['submit']['label'], render_kw={"class": "btn-color right-side"})


class LoginForm(WebUserForm):
    t = get_translation()['auth']['forms']['login']

    open = form_open(form_name='form-login')
    close = form_close()
    form_title = t['form_title']

    first_name = None
    last_name = None
    username = None
    phone_number = None
    password_verification = None
    is_admin = None
    is_active = None

    remember_me = BooleanField(
        label=t['remember_me']['label'], id='remember_me', default=True,
        render_kw={"class": "checkbox"}
    )

    submit = SubmitField(label=t['submit']['label'], render_kw={"class": "btn-color right-side"})


class UpdateForm(WebUserForm):
    t = get_translation()['auth']['forms']['account']

    open = form_open(form_name='form-update')
    close = form_close()
    form_title = t['title']
    #current_user.is_authenticated
    #first_name = current_user.first_name
    #last_name = None
    #phone_number = None
    password_verification = None
    is_admin = None
    is_active = None
    password_hash = None

    submit = SubmitField(label=t['submit']['label'], render_kw={"class": "btn-color right-side"})


class ChangePassword(WebUserForm):
    t = get_translation()['auth']['forms']['web_user']
    translation = get_translation()['auth']['forms']['account']

    open = form_open(form_name='form-update')
    close = form_close()
    form_title = translation['title']
    #current_user.is_authenticated
    first_name = None
    last_name = None
    phone_number = None
    email = None
    password_verification = None
    new_password = PasswordField(
        "%s:" % t['new_password']['label'],
        validators=[InputRequired(t['new_password']['required']), Length(max=30, message=t['password']['length'])],
        id='password', render_kw={"placeholder": t['new_password']['label']}
    )
    new_password_verification = PasswordField(
        "%s:" % t['new_password_verification']['label'],
        validators=[InputRequired(t['new_password_verification']['required']), Length(max=30, message=t['new_password_verification']['length'])],
        id='password', render_kw={"placeholder": t['new_password_verification']['label']}
    )
    #password_verification = None
    is_admin = None
    is_active = None
    #password_hash = None

    submit = SubmitField(label=translation['submit']['label'], render_kw={"class": "btn-color right-side"})