from flask import Blueprint, render_template, g

products_bp = Blueprint('products_bp', __name__,
                        template_folder='templates',
                        static_folder='static', static_url_path='assets')


@products_bp.url_value_preprocessor
def get_profile_owner(endpoint, values):
    # query = User.query.filter_by(url_slug=values.pop('user_url_slug'))
    g.profile_owner = values.pop('user_url_slug')


@products_bp.route('/')
def list():
    return "Hello product " + g.profile_owner
    # products = Example.query.all()
    # return render_template('products/list.html', products=products)


@products_bp.route('/view/<int:product_id>')
def view(product_id):
    return "Product %s" % product_id
    # product = Example.query.get(product_id)
    # return render_template('products/view.html', product=product)
