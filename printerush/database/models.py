import os
from datetime import datetime

from flask_login import UserMixin
from pony.orm import *

db = Database()


class WebUser(db.Entity, UserMixin):
    id = PrimaryKey(int, auto=True)
    first_name = Optional(str, 40)
    last_name = Optional(str, 40)
    username = Required(str, 20, unique=True)
    email = Required(str, 254, unique=True)
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
    comments_set = Set('Comment')
    addresses_set = Set('Address')

    def get_id(self):
        return self.id\

    @property
    def is_active(self):
        return self._is_active


class Product(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    explanation_html = Optional(str)
    photos_set = Set('Photo')
    comments_set = Set('Comment')
    store_ref = Required('Store')
    printiable3d_models_set = Set('Printiable3dModel')
    product_options_set = Set('ProductOption')
    product_feature_values_set = Set('ProductFeatureValue')
    product_category_ref = Required('ProductCategory')


class ProductBrand(db.Entity):
    id = PrimaryKey(int, auto=True)


class Address(db.Entity):
    id = PrimaryKey(int, auto=True)
    title = Optional(str)
    name = Optional(str)
    surname = Optional(str)
    phone_number = Optional(str)
    invoice_type = Optional(str)
    company_name = Optional(str)
    tax_number = Optional(str)
    tax_office = Optional(str)
    district_ref = Required('District')
    web_user_ref = Required(WebUser)
    store_ref = Optional('Store')


class ShoppingCart(db.Entity):
    id = PrimaryKey(int, auto=True)


class Order(db.Entity):
    id = PrimaryKey(int, auto=True)


class Printiable3dModel(db.Entity):
    id = PrimaryKey(int, auto=True)
    title = Optional(str)
    explanation = Optional(str)
    model_path = Optional(str)
    photos_set = Set('Photo')
    data_status_ref = Required('DataStatus')
    product_ref = Required(Product)


class OrderedProduct(db.Entity):
    id = PrimaryKey(int, auto=True)


class ProductCategory(db.Entity):
    id = PrimaryKey(int, auto=True)
    title = Optional(str)
    products_set = Set(Product)
    sub_categories_set = Set('ProductCategory', reverse='parent_category_ref')
    parent_category_ref = Required('ProductCategory', reverse='sub_categories_set')


class Store(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    explanation = Optional(str)
    about = Optional(str)
    phone_number = Optional(str)
    email = Optional(str)
    comments_set = Set('Comment')
    products_set = Set(Product)
    address_ref = Required(Address)


class Comment(db.Entity):
    id = PrimaryKey(int, auto=True)
    point = Optional(str)
    title = Optional(str)
    content = Optional(str)
    data_status_ref = Required('DataStatus')
    to_store_ref = Optional(Store)
    by_web_user_ref = Required(WebUser)
    to_product_ref = Optional(Product)


class Country(db.Entity):
    id = PrimaryKey(int, auto=True)
    cities_set = Set('City')


class City(db.Entity):
    id = PrimaryKey(int, auto=True)
    districts_set = Set('District')
    country_ref = Required(Country)


class District(db.Entity):
    id = PrimaryKey(int, auto=True)
    addresses_set = Set(Address)
    city_ref = Required(City)


class ProductOption(db.Entity):
    id = PrimaryKey(int, auto=True)
    product_ref = Required(Product)
    color = Optional(str)
    size = Optional(str)
    price = Optional(str)
    stock = Optional(str)
    discount_percent = Optional(str)
    discount_quantity = Optional(str)


class ProductFeature(db.Entity):
    id = PrimaryKey(int, auto=True)
    title = Optional(str)
    product_feature_values_set = Set('ProductFeatureValue')


class Photo(db.Entity):
    id = PrimaryKey(int, auto=True)
    photo_path = Optional(str)
    printiable3d_model_ref = Optional(Printiable3dModel)
    product_ref = Optional(Product)


class ProductFeatureValue(db.Entity):
    id = PrimaryKey(int, auto=True)
    product_ref = Required(Product)
    product_feature_ref = Required(ProductFeature)
    value = Optional(str)


class DataStatus(db.Entity):
    id = PrimaryKey(int, auto=True)
    creator_ref = Required(WebUser, reverse='created_set')
    creation_time = Optional(str)
    confirmer_ref = Required(WebUser, reverse='confirmed_set')
    confirmation_time = Optional(str)
    editor_ref = Required(WebUser, reverse='edited_set')
    edit_time = Optional(str)
    deletor_ref = Required(WebUser, reverse='deleted_set')
    deletion_time = Optional(str)
    comments_set = Optional(Comment)
    printiable3d_models_set = Optional(Printiable3dModel)


# # PostgreSQL
# url = os.getenv("DATABASE_URL")
# user = url.split('://')[1].split(':')[0]
# password = url.split('://')[1].split(':')[1].split('@')[0]
# host = url.split('://')[1].split(':')[1].split('@')[1]
# port = url.split('://')[1].split(':')[2].split('/')[0]
# database = url.split('://')[1].split(':')[2].split('/')[1]
# db.bind(provider='postgres', user=user, password=password, host=host, database=database, port=port)

# SQLite
db.bind(provider='sqlite', filename='database.sqlite', create_db=True)

set_sql_debug(True)

db.generate_mapping(create_tables=True)
