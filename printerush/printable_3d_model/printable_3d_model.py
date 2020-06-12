from flask import Blueprint, render_template, abort, g, request, redirect, url_for
from flask_login import current_user
from pony.orm import desc

from printerush.common.assistant_func import get_translation, flask_form_to_dict
from printerush.common.db import db_add_comment
from printerush.database.models import Printable3dModel
from printerush.printable_3d_model.assistans_func import ModelPI
from printerush.product.forms import CommentForm

models_bp = Blueprint('models_bp', __name__, template_folder='templates', static_folder='static',
                      static_url_path='assets')


@models_bp.route('/m<int:model_id>', defaults={'title': None}, methods=['GET', 'POST'])
@models_bp.route('/<title>-m<int:model_id>', methods=['GET', 'POST'])
def view_printable_3d_model(model_id, title):
    model = Printable3dModel.get(id=model_id)
    if not model:
        abort(404)

    g.similar_models = model.product_ref.printable_3d_models_set.select().order_by(lambda m: desc(m.point))[:10]

    # TODO eğer bir yorum varsa yorumu düzenle formu oluştur
    comment_form = CommentForm()

    # TODO yorumu js ile ekle
    if comment_form.validate_on_submit():
        json_data = flask_form_to_dict(request_form=request.form)
        json_data['to_printable3d_model_ref'] = model
        db_add_comment(json_comment=json_data, creator_ref=current_user)
        return redirect(url_for("models_bp.view_printable_3d_model", model_id=model_id, title=title))

    title = get_translation()['printable_3d_model']['printable_3d_model']['view_printable_3d_model']['title']
    return render_template("printable_3d_model/view_printable_3d_model.html",
                           page_info=ModelPI(model=model, title=title, form=comment_form))
