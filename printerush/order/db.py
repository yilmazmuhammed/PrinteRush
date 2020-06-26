from flask_login import current_user

from printerush.database.models import Order, DataStatus, SubOrder, OrderProduct


def create_order(web_user, shipping_address, invoicing_address):
    remove_order_if_exist(web_user)

    cart_products = web_user.cart_products_set
    order = Order(
        data_status_ref=DataStatus(creator_ref=current_user),
        web_user_ref=web_user,
        shipping_address_ref=shipping_address,
        invoicing_address_ref=invoicing_address
    )

    # sub_orders = {}
    for cp in cart_products:
        so = order.sub_orders_set.select(lambda so: so.store_ref == cp.product_ref.store_ref).get()
        # so = sub_orders.get(cp.product_ref.store_ref)
        if not so:
            so = SubOrder(
                customer_data_status_ref=DataStatus(creator_ref=web_user),
                order_ref=order, store_ref=cp.product_ref.store_ref
            )
            # sub_orders[cp.product_ref.store_ref] = so

        create_order_product_from_cart_product(cart_product=cp, sub_order=so)
    return order


def remove_order_if_exist(web_user):
    old_order = get_cart_order(web_user)
    if old_order:
        old_order.delete()
        return True
    return False


def create_order_product_from_cart_product(cart_product, sub_order):
    op = OrderProduct(
        product_name=cart_product.product_ref.name,
        quantity=cart_product.quantity,
        unit_price=cart_product.product_ref.main_option.price,
        product_ref=cart_product.product_ref,
        sub_order_ref=sub_order
    )
    return op


def get_cart_order(web_user):
    return web_user.orders_set.select(lambda o: o.stage == 0).get()


def get_order(order_id):
    return Order[order_id]