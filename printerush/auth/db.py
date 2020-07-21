from passlib.hash import pbkdf2_sha256 as hasher

from printerush.common.assistant_func import get_translation
from printerush.auth.exceptions import EmailAlreadyExist
from printerush.database.models import WebUser


def db_add_web_user(json_webuser):
    translation = get_translation()['auth']['db']['db_add_web_user']

    if WebUser.get(email=json_webuser['email']):
        raise EmailAlreadyExist(translation['email_already_exist'])

    json_webuser['password_hash'] = hasher.hash(json_webuser.pop('password'))
    # TODO form'u ögeyi incele ile değiştirip üst yetkili webuser olulturma
    return WebUser(**json_webuser)


def get_webuser(**kwargs):
    ret = WebUser.get(**kwargs)
    return ret
