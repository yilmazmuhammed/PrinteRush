import json

from flask import url_for
from werkzeug.datastructures import MultiDict


class LayoutPI:
    def __init__(self, title):
        self.title = title + " | PrinteRush"
        self.translation = get_translation()
        # if current_user.is_authenticated:
        #     self.none = None


class FormPI(LayoutPI):
    def __init__(self, form, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form = form
        self.errors = []
        for field in form:
            self.errors += field.errors


def flask_form_to_dict(request_form: MultiDict, exclude):
    result = {
        key: request_form.getlist(key)[0] if len(request_form.getlist(key)) == 1 else request_form.getlist(key)
        for key in request_form
    }

    result2 = {}
    for key in result:
        if not result[key] == "" and key not in exclude:
            result2[key] = result[key]
        # else:
        #     print("Message 1: Boş string pop'landı. key =", key, "->", result[key], "(views/yardimci.py)")

    result2.pop('submit', None)
    result2.pop('csrf_token', None)

    return result2


LANGUAGES = ['tr_TR', 'en_US']
translation = {}


def set_translation(language=None):  # language = session.get('language')
    global translation
    default_language = 'tr_TR'

    select_translation = {}
    if language is not None and language in LANGUAGES:
        with open(url_for('static', filename='languages/%s/translations.json' % language), 'r') as f:
            select_translation = json.load(f)
    with open('./printerush/static/languages/%s/translations.json' % default_language, 'r') as f:
        translation = json.load(f)
    translation.update(select_translation)
    return translation


def get_translation():
    global translation
    if len(translation) == 0:
        set_translation()
    return translation
