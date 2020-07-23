import os
import pathlib

from flask import render_template, g, request, url_for, current_app
from flask_login import current_user
from pony.orm import flush
from werkzeug.utils import secure_filename

from printerush.common.assistant_func import flask_form_to_dict
from printerush.common.db import db_add_photos
from printerush.product.assistant_func import product_category_choices
from printerush.product.db import db_add_product
from printerush.product.forms import NewProductForm
from printerush.store.db import get_store
from printerush.store.requirement import store_login_required


@store_login_required
def new_product_page(store_id):
    g.store = get_store(store_id=store_id)
    form = NewProductForm(product_category_choices=product_category_choices())
    if form.validate_on_submit():
        dict_data = flask_form_to_dict(request_form=request.form)
        dict_data['store_ref'] = store_id
        product = db_add_product(dict_product=dict_data, creator_ref=current_user)
        flush()
        db_add_photos(form.photos.data, product_ref=product)
        # db_add_printable_3d_models(form.printable_3d_models_set.data, product_ref=product)
        # for photo in form.photos.data:
        #     filename = secure_filename(photo.filename)
        #     directory_path = os.path.join(current_app.config['UPLOADED_FILES'], 'product', str(product.id))
        #     pathlib.Path(directory_path).mkdir(exist_ok=True)
        #     photo.save(os.path.join(directory_path, filename))
        #     product.photos_set.add(db_add_photo)

    return render_template("store/products/new_product.html", form=form)
