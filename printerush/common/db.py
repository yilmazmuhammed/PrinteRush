from printerush.database.models import DataStatus, Comment


def db_add_comment(json_comment, creator_ref):
    # translation = get_translation()['product']['db']['db_add_comment']

    json_comment['data_status_ref'] = DataStatus(creator_ref=creator_ref)

    return Comment(**json_comment)
