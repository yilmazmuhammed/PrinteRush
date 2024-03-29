import os
from datetime import datetime

from flask_login import UserMixin
from pony.orm import *

db = Database()


# TODO is_active
class WebUser(db.Entity, UserMixin):
    """
    :param account_type: Üyelik tipini belirtir
                         0 -> Müşteri hesabı
                         1 -> Mağaza hesabı,
                         2 -> Yönetici hesabı
    """
    id = PrimaryKey(int, auto=True)
    first_name = Optional(str, 40)
    last_name = Optional(str, 40)
    email = Required(str, 254)
    phone_number = Optional(str, 20)
    password_hash = Required(str)
    is_admin = Required(bool, default=False)
    _is_active = Required(bool, default=True)
    signup_time = Required(datetime, default=lambda: datetime.now())
    account_type = Required(int, size=8, default=0, unsigned=True)
    created_set = Set('DataStatus', reverse='creator_ref')
    deleted_set = Set('DataStatus', reverse='deletor_ref')
    confirmed_set = Set('DataStatus', reverse='confirmer_ref')
    edited_set = Set('DataStatus', reverse='editor_ref')
    cart_products_set = Set('CartProduct')
    shoppin_lists_set = Set('ShoppinList')
    orders_set = Set('Order')
    addresses_set = Set('Address')
    store_authorizations_set = Set('StoreAuthorization')
    visitor_logs_set = Set('VisitorLog')
    composite_key(email, account_type)

    def get_id(self):
        return self.id

    @property
    def is_active(self):
        return self._is_active

    @property
    def name_surname(self):
        return self.first_name + " " + self.last_name

    def get_first_store(self):
        return self.store_authorizations_set.order_by(lambda sa: sa.store_ref.id).first().store_ref

    def authorized_stores(self):
        return select(sa.store_ref for sa in self.store_authorizations_set)


class Product(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, 100)
    short_description_html = Optional(str)
    description_html = Optional(str)
    photos_set = Set('Photo')
    comments_set = Set('Comment')
    data_status_ref = Required('DataStatus')
    store_ref = Required('Store')
    printable_3d_models_set = Set('Printable3dModel')
    product_options_set = Set('ProductOption')
    product_feature_values_set = Set('ProductFeatureValue')
    product_category_ref = Required('ProductCategory')
    product_labels_set = Set('ProductLabel')
    shopping_products_set = Set('CartProduct')
    shoppin_lists_set = Set('ShoppinList')
    ordered_products_set = Set('OrderProduct')

    @property
    def point(self):
        return coalesce(select(c.point for c in self.comments_set).avg(), 0.0)

    @property
    def min_price(self):
        return coalesce(select(po.price for po in self.product_options_set).min(), 0.0)

    @property
    def max_price(self):
        return coalesce(select(po.price for po in self.product_options_set).max(), 0.0)

    @property
    def stock(self):
        return coalesce(select(po.stock for po in self.product_options_set).sum(), 0)

    @property
    def sold(self):
        return coalesce(select(po.sold for po in self.product_options_set).sum(), 0)

    @property
    def product_code(self):
        return '{:06d}'.format(self.id)

    @property
    def main_photo(self):
        return self.photos_set.select().first() if self.photos_set else Photo[1]

    @property
    def main_option(self):
        return self.product_options_set.order_by(lambda o: o.id).first()

    @property
    def url_name(self):
        return self.name.casefold().replace(" ", "-")


class Address(db.Entity):
    id = PrimaryKey(int, auto=True)
    title = Required(str, 40)
    first_name = Optional(str, 40)
    last_name = Optional(str, 40)
    address_detail = Required(str, 1000)
    phone_number = Required(str, 20)
    invoice_type = Required(int, size=8)
    company_name = Optional(str, 100)
    tax_number = Optional(str, 20)
    tax_office = Optional(str, 50)
    district_ref = Required('District')
    store_ref = Optional('Store')
    web_user_ref = Optional(WebUser)
    shipped_orders_set = Set('Order', reverse='shipping_address_ref')
    invoiced_orders_set = Set('Order', reverse='invoicing_address_ref')

    def is_erasable(self):
        if self.is_constant():
            return False
        return True

    def is_constant(self):
        return self.shipped_orders_set.count() > 0 or self.invoiced_orders_set.count() > 0


class Order(db.Entity):
    """
    :param stage: Siparişin hangi durumda olduğunu ifade eder, ödeme yapıldı, havale bekleniyor vs...
                  (1->Müşteri onayladı,
                  2->Ödeme yapıldı,
                  3->Site onayladı,
                  4->Müşteri siparişini adlı ve onayladı,
                  5->Sipariş tamamlandı)
    """
    id = PrimaryKey(int, auto=True)
    data_status_ref = Required('DataStatus')
    web_user_ref = Required(WebUser)
    sub_orders_set = Set('SubOrder')
    stage = Required(int, size=8, default=0)
    shipping_address_ref = Required(Address, reverse='shipped_orders_set')
    invoicing_address_ref = Required(Address, reverse='invoiced_orders_set')

    @property
    def products_price(self):
        return coalesce(
            select(op.unit_price * op.quantity for op in OrderProduct if op.sub_order_ref.order_ref == self).sum(), 0
        )

    @property
    def shipping_price(self):
        return 0

    @property
    def is_free_shipping(self):
        return False

    @property
    def total_price(self):
        return self.shipping_price + self.products_price

    @property
    def payment_method(self):
        return "Online ödeme"

    @property
    def order_status_message(self):
        if self.stage == 1:
            return "Ödeme bekleniyor"
        if self.stage == 2:
            return "Sipariş onay bekliyor"
        if self.stage == 3:
            return "Sipariş onaylandı"
        if self.stage == 3:
            return "Müşteri onayı bekleniyor"
        if self.stage == 5:
            return "Sipariş tamamlandı"


class Printable3dModel(db.Entity):
    id = PrimaryKey(int, auto=True)
    title = Optional(str)
    description_html = Optional(str)
    file_path = Optional(str)
    photos_set = Set('Photo')
    comments_set = Set('Comment')
    data_status_ref = Required('DataStatus')
    product_ref = Required(Product)

    @property
    def point(self):
        return coalesce(select(c.point for c in self.comments_set).avg(), 0.0)

    @property
    def main_photo(self):
        return self.photos_set[0] if self.photos_set else Photo[1]


class OrderProduct(db.Entity):
    id = PrimaryKey(int, auto=True)
    product_name = Required(str, 100)
    quantity = Required(int)
    unit_price = Required(float)
    product_ref = Required(Product)
    sub_order_ref = Required('SubOrder')


class ProductCategory(db.Entity):
    id = PrimaryKey(int, auto=True)
    title_key = Required(str)
    products_set = Set(Product)
    sub_categories_set = Set('ProductCategory', reverse='parent_category_ref')
    parent_category_ref = Optional('ProductCategory', reverse='sub_categories_set')

    def sub_categories(self):
        ret = [self]
        for sub_category in self.sub_categories_set:
            ret += sub_category.sub_categories()

        return ret

    def products(self, sort_by=None):
        categories = self.sub_categories()
        ret = select(p for p in Product if p.product_category_ref in categories)
        if sort_by:
            ret = ret.sort_by(sort_by)
        return ret

    @property
    def url_title(self):
        return self.title_key.casefold().replace(" ", "-")


class Store(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, 100, unique=True)
    short_name = Required(str, 20, unique=True)
    about_html = Optional(str)
    explanation_html = Optional(str)
    phone_number = Required(str, 20)
    email = Required(str, 254)
    data_status_ref = Required('DataStatus')
    comments_set = Set('Comment')
    products_set = Set(Product)
    sub_orders_set = Set('SubOrder')
    address_ref = Required(Address)
    store_authorizations_set = Set('StoreAuthorization')


class Comment(db.Entity):
    id = PrimaryKey(int, auto=True)
    point = Required(int, size=8, unsigned=True)
    title = Required(str, 100)
    message = Required(str)
    data_status_ref = Required('DataStatus')
    to_store_ref = Optional(Store)
    to_printable3d_model_ref = Optional(Printable3dModel)
    to_product_ref = Optional(Product)


class Country(db.Entity):
    id = PrimaryKey(int, auto=True)
    country = Required(str, 30, unique=True)
    cities_set = Set('City')


class City(db.Entity):
    id = PrimaryKey(int, auto=True)
    city = Required(str, 30)
    districts_set = Set('District')
    country_ref = Required(Country)


class District(db.Entity):
    id = PrimaryKey(int, auto=True)
    district = Required(str, 40)
    addresses_set = Set(Address)
    city_ref = Required(City)


class ProductOption(db.Entity):
    id = PrimaryKey(int, auto=True)
    product_ref = Required(Product)
    color = Optional(str)
    size = Optional(str)
    price = Required(float)
    stock = Required(int, unsigned=True)
    sold = Required(int, default=0, unsigned=True)
    discount_percent = Optional(int, size=8, unsigned=True)
    discount_quantity = Optional(int, size=8, unsigned=True)


class ProductFeature(db.Entity):
    id = PrimaryKey(int, auto=True)
    title = Required(str)
    product_feature_values_set = Set('ProductFeatureValue')


class Photo(db.Entity):
    id = PrimaryKey(int, auto=True)
    file_path = Optional(str)
    printable_3d_model_ref = Optional(Printable3dModel)
    product_ref = Optional(Product)


class ProductFeatureValue(db.Entity):
    id = PrimaryKey(int, auto=True)
    product_ref = Required(Product)
    product_feature_ref = Required(ProductFeature)
    value = Required(str)


class DataStatus(db.Entity):
    id = PrimaryKey(int, auto=True)
    creator_ref = Required(WebUser, reverse='created_set')
    creation_time = Required(datetime, default=lambda: datetime.now())
    confirmer_ref = Optional(WebUser, reverse='confirmed_set')
    confirmation_time = Optional(datetime)
    editor_ref = Optional(WebUser, reverse='edited_set')
    edit_time = Optional(datetime)
    deletor_ref = Optional(WebUser, reverse='deleted_set')
    deletion_time = Optional(datetime)
    store_ref = Optional(Store)
    comment_ref = Optional(Comment)
    printable_3d_model_ref = Optional(Printable3dModel)
    product_ref = Optional(Product)
    customer_sub_order_ref = Optional('SubOrder', reverse='customer_data_status_ref')
    store_sub_order_ref = Optional('SubOrder', reverse='store_data_status_ref')
    order_ref = Optional(Order)


class ProductLabel(db.Entity):
    id = PrimaryKey(int, auto=True)
    label = Required(str)
    products_set = Set(Product)


class ShoppinList(db.Entity):
    id = PrimaryKey(int, auto=True)
    title = Required(str)
    web_user_ref = Required(WebUser)
    products_set = Set(Product)


class CartProduct(db.Entity):
    id = PrimaryKey(int, auto=True)
    product_ref = Required(Product)
    quantity = Required(int)
    web_user_ref = Required(WebUser)


class SubOrder(db.Entity):
    """
    :param stage: Siparişin hangi durumda olduğunu ifade eder, ödeme yapıldı, havale bekleniyor vs...
                  (1->Müşteri onayı,
                  2->Ödeme yapıldı,
                  3->Site onayı,
                  4->Mağaza onayı,
                  5->Kargoya verildi,
                  6->Teslimat tamamlandı
                  7->Müşteri onayı,
                  8->Paranın mağazaya teslimi)
    """
    id = PrimaryKey(int, auto=True)
    order_products_set = Set(OrderProduct)
    customer_data_status_ref = Required(DataStatus, reverse='customer_sub_order_ref')
    store_data_status_ref = Optional(DataStatus, reverse='store_sub_order_ref')
    store_ref = Required(Store)
    order_ref = Required(Order)
    shipping_information_for_invoice_ref = Optional('ShippingTracking', reverse='sub_order_for_invoice_ref')
    shipping_information_for_products_ref = Optional('ShippingTracking', reverse='sub_order_for_products_ref')
    stage = Required(int, size=8, default=0)


class ShippingTracking(db.Entity):
    id = PrimaryKey(int, auto=True)
    delivery_time = Optional(datetime)
    shipping_company = Required(str)
    shipping_tracking_number = Required(str)
    status = Required(int)
    sub_order_for_products_ref = Optional(SubOrder, reverse='shipping_information_for_products_ref')
    sub_order_for_invoice_ref = Optional(SubOrder, reverse='shipping_information_for_invoice_ref')


class StoreAuthorization(db.Entity):
    id = PrimaryKey(int, auto=True)
    authorization = Required(str, 50)
    is_admin = Required(bool, default=False)
    store_ref = Required(Store)
    web_users_set = Set(WebUser)


class VisitorLog(db.Entity):
    id = PrimaryKey(int, auto=True)
    no_of_visits = Optional(int, unsigned=True)
    ip_address = Optional(str, 20)
    requested_url = Optional(str)
    referer_page = Optional(str)
    page_name = Optional(str)
    query_string = Optional(str)
    user_agent = Optional(str)
    is_unique = Required(str, default="0")
    access_date = Required(datetime, default=lambda: datetime.now())
    web_user_ref = Optional(WebUser)


if os.getenv('DEBUG') == "TRUE":
    # SQLite
    db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
else:
    # PostgreSQL
    db.bind(provider="postgres", dsn=os.getenv('DATABASE_URL'))

db.generate_mapping(create_tables=True)

if __name__ == '__main__':
    with db_session:
        if not Country.get(country='Türkiye'):
            from pyexcel_ods3 import get_data

            data = get_data("Ilce_Listesi.ods")

            country = Country(country="Türkiye")
            city = None
            for key in data.keys():
                print(key)
                for line in data[key][:-4]:
                    if len(line) == 0:
                        continue

                    if len(line) == 4 and line[1] == '' and line[2] == '':
                        city = City(city=line[0], country_ref=country)
                        continue

                    for cell in line:
                        if cell == "":
                            continue
                        d = District(district=cell, city_ref=city)

        if WebUser.select(lambda w: w.is_admin == True):
            print("db pass")
            pass
        else:
            webuser = WebUser(email="admin@printerush.com",
                              password_hash="$pbkdf2-sha256$29000$zDlHiHEOAQBASMlZK8V4bw$au7qZNqL3z0Q0C9upWm9rzGQ10eW8p/Fc3ahvAvxYKY",
                              is_admin=True)
            magaza = WebUser(email="magaza@printerush.com",
                             password_hash="$pbkdf2-sha256$29000$zDlHiHEOAQBASMlZK8V4bw$au7qZNqL3z0Q0C9upWm9rzGQ10eW8p/Fc3ahvAvxYKY",
                             is_admin=True, account_type=1)
            addr = Address(title="store address", first_name="fn", last_name="ln", address_detail="ad",
                           phone_number="pn", invoice_type=0, district_ref=d)
            store1 = Store(name="PrinteRush", short_name="PrinteRush", phone_number="+905392024175",
                           email="store@printerush.com", address_ref=addr,
                           data_status_ref=DataStatus(creator_ref=magaza,
                                                      confirmer_ref=webuser, confirmation_time=datetime.now())
                           )
            magaza_admin_yetkisi = StoreAuthorization(authorization="Kurucu", is_admin=True, store_ref=store1,
                                                      web_users_set=[magaza])
            root = ProductCategory(title_key="PrinteRush")
            aydinlatma = ProductCategory(title_key="Aydınlatma", parent_category_ref=root)
            ProductCategory(title_key="Masa lambası", parent_category_ref=aydinlatma)
            ProductCategory(title_key="Abajur", parent_category_ref=aydinlatma)
            ProductCategory(title_key="Avize", parent_category_ref=aydinlatma)
            saat = ProductCategory(title_key="Saat", parent_category_ref=root)
            ProductCategory(title_key="Masa saati", parent_category_ref=saat)
            ProductCategory(title_key="Duvar saati", parent_category_ref=saat)
            ProductCategory(title_key="Saat", parent_category_ref=root)
            ProductCategory(title_key="Kamera ekipmanları", parent_category_ref=root)
            ProductCategory(title_key="Ev dekorasyonu", parent_category_ref=root)
            ProductCategory(title_key="Aksesuar", parent_category_ref=root)
            ProductCategory(title_key="Mutfak gereçleri", parent_category_ref=root)
            ProductCategory(title_key="Hobi", parent_category_ref=root)
            ProductCategory(title_key="Elektronik", parent_category_ref=root)
            ProductCategory(title_key="Oyuncak", parent_category_ref=root)

            # category1 = ProductCategory(title_key="Aydınlatma", parent_category_ref=root)
            # category1_1 = ProductCategory(title_key="Masa Lambası", parent_category_ref=category1)
            # category1_2 = ProductCategory(title_key="Tavan Lambası", parent_category_ref=category1)
            photo1 = Photo(file_path="printerush.com/static/images/1.jpg")
            # product1 = Product(name="Ürün 1", description_html="Product 1 açıklaması",
            #                    short_description_html="<b>Product</b> 1 sort",
            #                    store_ref=store1, product_category_ref=category1_1,
            #                    data_status_ref=DataStatus(creator_ref=magaza))
            # Comment(point=4, title="comment 1 title of product 1", message="comment1 of product 1 comment of product 1",
            #         to_product_ref=product1, data_status_ref=DataStatus(creator_ref=webuser))
            # Comment(point=5, title="comment 2 title of product 1", message="comment2 of product 1 comment of product 1",
            #         to_product_ref=product1, data_status_ref=DataStatus(creator_ref=webuser))
            # Comment(point=5, title="comment 3 title of product 1", message="comment3 of product 1 comment of product 1",
            #         to_product_ref=product1, data_status_ref=DataStatus(creator_ref=webuser))
            # ProductOption(product_ref=product1, price=10.50, stock=15)
            #
            # ProductOption(product_ref=Product(name="Ürün 2", description_html="Product 2 açıklaması",
            #                                   short_description_html="<b>Product</b> 2 sort",
            #                                   store_ref=store1, product_category_ref=category1_2,
            #                                   data_status_ref=DataStatus(creator_ref=magaza)
            #                                   ),
            #               price=100, stock=15)
