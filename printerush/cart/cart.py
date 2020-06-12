from flask import Blueprint, render_template, g

cart_bp = Blueprint('cart_bp', __name__,
                    template_folder='templates',
                    static_folder='static', static_url_path='assets')


@cart_bp.url_value_preprocessor
def get_profile_owner(endpoint, values):
    # query = User.query.filter_by(url_slug=values.pop('user_url_slug'))
    g.profile_owner = values.pop('user_url_slug')


@cart_bp.route('/')
def list():
    return "Hello product " + g.profile_owner
    # product = Example.query.all()
    # return render_template('product/list.html', product=product)


@cart_bp.route('/view/<int:cart_id>')
def view(cart_id):
    return "Product %s" % cart_id
    # product = Example.query.get(product_id)
    # return render_template('product/view_product.html', product=product)
