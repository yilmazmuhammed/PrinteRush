from flask import Blueprint, render_template, g, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from pony.orm import db_session

from printerush.common.assistant_func import LayoutPI, get_translation, flask_form_to_dict
from printerush.store.additional_components import LayoutSPI
from printerush.store.db import db_add_store, get_store
from printerush.store.exceptions import ThereIsNotStore
from printerush.store.forms import NewStoreForm
from printerush.store.requirement import store_login_required, store_authorization_required
from printerush.store.store_auth import login_page
from printerush.store.store_products import new_product_page

store_sbp = Blueprint('store_sbp', __name__, template_folder='templates', static_folder='static',
                      static_url_path='')

store_sbp.add_url_rule('/login', view_func=login_page, methods=['GET', 'POST'])

store_sbp.add_url_rule('/s<int:store_id>/products/new_product', view_func=new_product_page, methods=['GET', 'POST'])

prefix_sid = "/s<int:store_id>"


@store_sbp.route('/s<int:store_id>/dashboard')
@store_authorization_required(is_admin=True)
def dashboard_page(store_id):
    return render_template("store/layout.html", page_info=LayoutSPI(title="Dashboard"))


@store_sbp.route('/new_store_request', methods=['GET', 'POST'])
@login_required
def new_store_request_page():
    t = get_translation()['store']['store']['new_store_request_page']

    if request.args.get("result_message"):
        flash(request.args.get("result_message"), "success")
        g.result = True
        return render_template("store/new_store_request.html", page_info=LayoutPI(title=t['title']))

    form = NewStoreForm()
    if form.validate_on_submit():
        json_data = flask_form_to_dict(request_form=request.form)
        db_add_store(json_store=json_data, creator_ref=current_user, admin_ref=current_user)
        return redirect(url_for("store_bp.new_store_request_page",
                                result_message="Başvurunuz alınmıştır. En kısa zamanda verdiğiniz iletişim bilgilerine dönüş yapılacaktır."))

    g.store_form = form
    return render_template("store/new_store_request.html", page_info=LayoutPI(title=t['title']))
