from passlib.hash import pbkdf2_sha256 as hasher

from printerush.assistant_func import get_translation
from printerush.auth.exceptions import UsernameAlreadyExist, EmailAlreadyExist, ThereIsNotWebUser
from printerush.database.models import WebUser


def db_add_web_user(json_webuser):
    translation = get_translation()['auth']['db']['db_add_web_user']
    if WebUser.get(username=json_webuser['username']):
        raise UsernameAlreadyExist(translation['username_already_exist'])
    elif WebUser.get(email=json_webuser['email']):
        raise EmailAlreadyExist(translation['email_already_exist'])

    json_webuser['password_hash'] = hasher.hash(json_webuser.pop('password'))
    return WebUser(**json_webuser)


def get_web_user(username) -> WebUser:
    wu = WebUser.get(username=username)
    if wu is None:
        raise ThereIsNotWebUser(get_translation()['istisnalar']['kullanici_yok'])
    return wu
