import os
import pathlib

from flask import current_app, url_for
from werkzeug.utils import secure_filename

from printerush.database.models import DataStatus, Comment, Photo


def db_add_comment(json_comment, creator_ref):
    # translation = get_translation()['product']['db']['db_add_comment']

    json_comment['data_status_ref'] = DataStatus(creator_ref=creator_ref)

    return Comment(**json_comment)


def db_add_photos(photos, **kwargs):
    ret = []
    root, leaf = 'other', ''
    if kwargs.get('product_ref'):
        root = 'product'
        leaf = str(kwargs.get('product_ref').id)

    for photo in photos:
        if not photo:
            continue
        filename = secure_filename(photo.filename)
        task = os.path.join('images', root, leaf)
        directory_path = os.path.join(current_app.config['UPLOADED_FILES'], task)
        pathlib.Path(directory_path).mkdir(exist_ok=True)
        photo.save(os.path.join(directory_path, filename))
        ret.append(Photo(file_path=url_for('db_bp.static', filename=os.path.join('files', task, filename)), **kwargs))

