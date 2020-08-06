from printerush.database.models import VisitorLog


def add_visitor_log(**kwargs):
    # print(kwargs)
    return VisitorLog(**kwargs)
