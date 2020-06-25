class IyzikoInitialize:
    def __init__(self, web_user, order):
        self.options = {}
        self.buyer = {}
        self.invoicing_address = {}
        self.shipping_address = {}
        self.basket_items = []
        self.request = {}

        self.init_options()
        self.init_buyer(web_user, order)
        self.init_invoicing_address(order)
        self.init_shipping_address(order)
        self.init_basket_items(order)
        self.init_request(order)

    def init_options(self):
        self.options = {
            'api_key': "sandbox-odVGhnYPNFNW4yJday7u5KcdWIdB03lI",
            'secret_key': "sandbox-0CDV337XXxEgGq8RpOYp0TxF9FxKuKeF",
            'base_url': "sandbox-api.iyzipay.com"
        }

    # TODO only web_user info
    def init_buyer(self, web_user, order):
        self.buyer = {
            'id': str(web_user.id),
            'name': web_user.first_name,
            'surname': web_user.last_name,
            'email': web_user.email,
            'identityNumber': '74300864791',
            'ip': '85.34.78.112',
            'gsmNumber': order.invoicing_address_ref.phone_number,
            'city': order.invoicing_address_ref.district_ref.city_ref.city,
            'country': order.invoicing_address_ref.district_ref.city_ref.country_ref.country,
            'registrationAddress': order.invoicing_address_ref.address_detail
        }

    def init_invoicing_address(self, order):
        self.invoicing_address = {
            'contactName': order.invoicing_address_ref.first_name + " " + order.invoicing_address_ref.last_name,
            'city': order.invoicing_address_ref.district_ref.city_ref.city,
            'country': order.invoicing_address_ref.district_ref.city_ref.country_ref.country,
            'address': order.invoicing_address_ref.address_detail
        }

    def init_shipping_address(self, order):
        self.shipping_address = {
            'contactName': order.shipping_address_ref.first_name + " " + order.shipping_address_ref.last_name,
            'city': order.shipping_address_ref.district_ref.city_ref.city,
            'country': order.shipping_address_ref.district_ref.city_ref.country_ref.country,
            'address': order.shipping_address_ref.address_detail
        }

    def init_basket_items(self, order):
        for so in order.sub_orders_set:
            for op in so.order_products_set:
                for i in range(op.quantity):
                    self.basket_items.append(
                        {
                            'id': op.product_ref.id,
                            'name': op.product_name,
                            'category1': op.product_ref.product_category_ref.title_key,
                            'itemType': 'PHYSICAL',
                            'price': op.unit_price
                        }
                    )

    def init_request(self, order):
        self.request = {
            'locale': 'tr',
            'price': order.total_price,
            'paidPrice': order.total_price,
            'currency': 'TRY',
            "callbackUrl": "http://127.0.0.1:5000/order/checkout/payment",
            "enabledInstallments": ['2', '3', '6', '9'],
            'buyer': self.buyer,
            'shippingAddress': self.shipping_address,
            'billingAddress': self.invoicing_address,
            'basketItems': self.basket_items,
            "basketId": str(order.id)
        }


class IyzikoRetrieve:
    def __init__(self, token):
        self.options = {}
        self.request = {}

        self.init_options()
        self.init_request(token)

    def init_options(self):
        self.options = {
            'api_key': "sandbox-odVGhnYPNFNW4yJday7u5KcdWIdB03lI",
            'secret_key': "sandbox-0CDV337XXxEgGq8RpOYp0TxF9FxKuKeF",
            'base_url': "sandbox-api.iyzipay.com"
        }

    def init_request(self, token):
        self.request = {
            'locale': 'tr',
            'conversationId': '123456789',
            'token': token
        }
