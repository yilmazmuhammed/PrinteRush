from flask_login import UserMixin

from printerush.database.models import WebUser


# class FlaskUser(UserMixin, WebUser):
#     def __init__(self, username):
#         # self = WebUser.get(username=username)
#         # self.kullanici_adi = kullanici_adi
#         # wu = get_webuser(kullanici_adi=self.kullanici_adi)
#         # self.id = wu.id
#         # self.is_admin = wu.is_admin
#         pass
#
#     def get_id(self):
#         return self.id
#
#     @property
#     def is_active(self):
#         return self.is_active
