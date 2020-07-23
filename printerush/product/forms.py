from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, FieldList, SubmitField, IntegerField, DecimalField
from wtforms.validators import InputRequired, Length, NumberRange

from printerush.common.assistant_func import get_translation, Forms
from printerush.common.forms import CustomSelectField, form_open, form_close


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


class ProductForm(FlaskForm):
    t = get_translation()['product']['forms']['product']

    open = form_open(form_name='form-product', enctype="multipart/form-data")
    close = form_close()

    name = StringField(
        label="%s" % t['name']['label'],
        validators=[InputRequired(t['name']['required']), Length(max=100, message=t['name']['length'])],
        id='name', render_kw={"placeholder": t['name']['label']}
    )

    price = DecimalField(
        label="%s" % t['price']['label'],
        validators=[
            InputRequired(t['price']['required']),
            NumberRange(min=0, message=t['price']['number_range'])
        ],
        id='price', render_kw={"placeholder": t['price']['placeholder']}
    )

    stock = IntegerField(
        label="%s" % t['stock']['label'],
        validators=[
            InputRequired(t['stock']['required']),
            NumberRange(min=0, message=t['stock']['number_range'])
        ],
        id='stock', render_kw={"placeholder": t['stock']['label']}
    )

    product_category_ref = CustomSelectField(
        label="%s:" % t['product_category_ref']['label'],
        validators=[InputRequired(t['product_category_ref']['required'])],
        # validate_choice=False,
        coerce=int, choices=[('', t['product_category_ref']['please_select'])],
        id='product_category_ref'
    )

    short_description_html = TextAreaField(
        label="%s" % t['short_description_html']['label'],
        id='short_description_html', render_kw={"placeholder": t['short_description_html']['label']}
    )

    description_html = TextAreaField(
        label="%s" % t['description_html']['label'],
        id='description_html', render_kw={"placeholder": t['description_html']['label']}
    )

    images_extension_set = ['jpg', 'png', 'jpeg']
    photos = FieldList(
        FileField(
            label=t["photos"]["label"],
            validators=[
                FileAllowed(images_extension_set, t['photos']['file_allowed'] + str(images_extension_set))
            ]
        ),
        min_entries=1, max_entries=20
    )

    models_extension_set = ['jpg', 'png', 'jpeg']
    printable_3d_models_set = FieldList(
        FileField(
            label=t["printable_3d_models_set"]["label"],
            validators=[
                FileAllowed(models_extension_set,
                            t['printable_3d_models_set']['file_allowed'] + str(models_extension_set))
            ]
        ),
        min_entries=1, max_entries=10
    )

    submit = SubmitField(label=t['submit']['label'], render_kw={"class": "btn-color right-side"})

    def __init__(self, product_category_choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.product_category_ref.choices += product_category_choices


class NewProductForm(ProductForm):
    t = get_translation()['product']['forms']['new_product']

    open = form_open(form_name='form-new_product', enctype="multipart/form-data", f_class="form-horizontal")
    close = form_close()
    form_title = t["form_title"]

    printable_3d_models_set = None

    submit = SubmitField(label=t['submit']['label'], render_kw={"class": "btn-color right-side"})
