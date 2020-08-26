import math

from flask import Blueprint, render_template, abort, request, g, redirect, url_for
from flask_login import current_user
from pony.orm import desc

from printerush.common.assistant_func import get_translation, flask_form_to_dict
from printerush.common.db import db_add_comment
from printerush.database.models import Product, ProductCategory
from printerush.general.requirement import url_reformative
from printerush.product.assistant_func import ProductPI, detect_sorting_and_filtering, ProductCategoryPI
from printerush.product.db import get_product
from printerush.product.forms import CommentForm, FilterForm

products_bp = Blueprint('products_bp', __name__, template_folder='templates', static_folder='static',
                        static_url_path='assets')


@products_bp.route('/p<int:product_id>', defaults={'p': None}, methods=['GET', 'POST'])
@products_bp.route('/<p>-p<int:product_id>', methods=['GET', 'POST'])
@url_reformative
def view(product_id, p):
    product = get_product(product_id=product_id)
    if not product:
        abort(404)

    g.similar_products = product.product_category_ref.products_set.select().order_by(lambda pr: (desc(int(bool(pr.stock))), desc(pr.sold)))[:10]

    # TODO eğer bir yorum varsa yorumu düzenle formu oluştur
    comment_form = CommentForm()

    # TODO yorumu js ile ekle
    if comment_form.validate_on_submit():
        json_data = flask_form_to_dict(request_form=request.form)
        json_data['to_product_ref'] = product
        db_add_comment(json_comment=json_data, creator_ref=current_user)
        return redirect(url_for("products_bp.view", product_id=product_id, p=p))

    title = get_translation()['product']['product']['view']['title']
    return render_template('product/view_product.html',
                           page_info=ProductPI(product=product, title=title, form=comment_form))


@products_bp.route('/c<category_id>', defaults={'p': None}, methods=['GET', 'POST'])
@products_bp.route('/<p>-c<category_id>', methods=['GET', 'POST'])
@url_reformative
def view_category(category_id, p):
    g.request_args = lambda exl: {key: value for key, value in request.args.to_dict().items() if key not in exl}

    g.page = 1 if not request.args.get('page', None) else int(request.args['page'])
    pagesize = 24 if not request.args.get('pagesize', None) else int(request.args['pagesize'])

    sorting, filtering = detect_sorting_and_filtering(**request.args.to_dict())

    category = ProductCategory.get(id=category_id)
    if not category:
        abort(404)

    filter_form = FilterForm()
    # try:
    products = category.products().filter(filtering).sort_by(sorting)
    g.product_count = products.count()
    products = products.page(g.page, pagesize)
    # except Exception as e:
    #     return redirect(url_for("products_bp.view_category", category_id=category_id, p=p))

    g.number_of_page = math.ceil(g.product_count / pagesize)
    g.best_seller = category.products().sort_by("lambda p: (desc(int(bool(p.stock))), desc(p.sold))")[:3]
    title = get_translation()['product']['product']['view_category']['title']
    return render_template('product/view_category.html',
                           page_info=ProductCategoryPI(category=category, products=products, title=title,
                                                       form=filter_form))
