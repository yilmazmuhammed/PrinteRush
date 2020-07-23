from flask import Blueprint

db_bp = Blueprint('db_bp', __name__, static_folder='static', static_url_path='assets')
