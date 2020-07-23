from functools import wraps

from flask import g

from printerush.common.assistant_func import get_translation, LANGUAGES
from printerush.store.db import get_store
from printerush.store.requirement import store_login_required


class LayoutSPI:
    def __init__(self, title, translation=None):
        self.title = title + " | PrinteRush"
        self.translation = get_translation() if not translation else translation
        g.languages = LANGUAGES
        g.slt = get_translation()["store"]["layout"]


def store_pages_init(store_id):
    if store_id:
        g.store = get_store(store_id=store_id)
        g.slt = get_translation()["store"]["layout"]

