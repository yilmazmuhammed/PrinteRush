from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Length

from printerush.common.assistant_func import get_translation, Forms


class CommentForm(FlaskForm):
    t = get_translation()['product']['forms']['comment']

    open = Forms.form_open(form_name='form-comment')
    close = Forms.form_close()

    title = StringField(
        label="%s:" % t['title']['label'],
        validators=[InputRequired(t['title']['required']), Length(max=100, message=t['title']['length'])],
        id='title', render_kw={"placeholder": t['title']['label']}
    )

    point = SelectField(
        label="%s:" % t['point']['label'],
        validators=[InputRequired(t['point']['required'])],
        coerce=int, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=5,
        id='select_field'
    )

    message = TextAreaField(
        label="%s:" % t['message']['label'],
        validators=[InputRequired(t['message']['required'])],
        id='message', render_kw={"placeholder": t['message']['label']}
    )

    submit = Forms.SubmitField(label=t['submit']['label'], render_kw={"class": "btn btn-color"})


class FilterForm(FlaskForm):
    t = get_translation()['product']['forms']['filter']

    open = Forms.form_open(form_name='form-filter')
    close = Forms.form_close()

    submit = Forms.SubmitField(label=t['submit']['label'], render_kw={"class": "btn btn-color"})
