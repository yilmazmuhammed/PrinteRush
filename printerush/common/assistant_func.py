import json

from flask import url_for, g, session
from flask_login import current_user
from werkzeug.datastructures import MultiDict
from wtforms import SubmitField


class LayoutPI:
    def __init__(self, title, translation=None):
        self.title = title + " | PrinteRush"
        self.translation = get_translation() if not translation else translation
        g.languages = LANGUAGES
        if current_user.is_authenticated:
            g.shopping_cart = current_user.cart_products_set
        else:
            g.shopping_cart = session.get("shopping_cart", [])
        # if current_user.is_authenticated:
        #     self.none = None


class FormPI(LayoutPI):
    def __init__(self, form, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form = form
        self.errors = []


def flask_form_to_dict(request_form: MultiDict, exclude=[]):
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


LANGUAGES = {'tr_TR': 'Türkçe', 'en_US': 'English'}
global_translation = {}


def set_translation(language=None):  # language = session.get('language')
    global global_translation
    default_language = 'tr_TR'

    select_translation = {}
    if language is not None and language in LANGUAGES.keys():
        with open(url_for('static', filename='languages/%s/translations.json' % language), 'r') as f:
            select_translation = json.load(f)
    with open('./printerush/static/languages/%s/translations.json' % default_language, 'r') as f:
        global_translation = json.load(f)
    global_translation.update(select_translation)
    return global_translation


def get_translation():
    global global_translation
    if len(global_translation) == 0:
        set_translation()
    return global_translation


class Forms:
    @staticmethod
    def form_open(form_name, f_id=None, enctype=None, f_action=""):
        f_open = """<form action="%s" method="post" name="%s" """ % (f_action, form_name,)

        if f_id:
            f_open += """ id="%s" """ % (f_id,)
        if enctype:
            f_open += """ enctype="%s" """ % (enctype,)

        f_open += """class="main-form full">"""

        return f_open

    @staticmethod
    def form_close():
        return """</form>"""

    class SubmitField(SubmitField):
        def __call__(self, *args, **kwargs):
            ret = '<button name="' + self.id + '" type="submit" '
            for key, value in self.render_kw.items():
                ret += key + '="' + value + '" '
            ret += '>' + self.label.text + '</button>'
            return ret


def filtreleme_olustur(**kwargs):
    filtre = "lambda b: b"
    for key, value in kwargs.items():
        if key[:4] == 'min_':
            filtre += " and b.%s >= %s" % (key[4:], value,)
        elif key[:4] == 'max_':
            filtre += " and b.%s <= %s" % (key[4:], value,)
        # str olanların içince aramak için -> 'h' in 'ahmet'
        elif key[:3] == "in_":
            filtre += " and %s in b.%s" % (value, key[3:],)
        else:
            filtre += " and b.%s == %s" % (key, value,)
    print(filtre)
    return filtre
