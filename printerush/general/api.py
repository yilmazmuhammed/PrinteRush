from flask import Blueprint, jsonify

from printerush.bots.mail_bot import send_email
from printerush.common.assistant_func import get_translation

general_api_bp = Blueprint('general_api_bp', __name__)


@general_api_bp.route('/subscribe/<string:email>')
def subscribe_api(email):
    translation = get_translation()['general']['api']['subscribe_api']

    try:
        msg = translation["mail_msg"].format(email=email)
        send_email(["iletisim@printerush.com"], subject=translation["subject"], message=msg)
        return jsonify(result=True, msg=translation["success_msg"])
    except Exception as e:
        return jsonify(result=False, err_msg=str(e))
