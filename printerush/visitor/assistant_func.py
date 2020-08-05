from flask import request, session
from pony.orm import select

from printerush.database.models import VisitorLog
from printerush.visitor.db import add_visitor_log

DNT_TRACK = True  # False
IGNORE_IPS = {'127.0.0.1'}
IGNORE_IPS = {}


def is_tracking_allowed():
    # print(request.headers["DNT"])
    # if 'DNT' in request.headers and int(request.headers['DNT']) == 1:
    #     return False
    if request.remote_addr in IGNORE_IPS:
        return False
    except_parts = ["static", "assets", "api", "jsglue"]
    for part in except_parts:
        if part in request.path:
            return False
    return True


def track_session():
    if 'visitor_log_track_session' in session and session['visitor_log_track_session'] == True:
        return True
    else:
        return False


def track_visitor():
    if is_tracking_allowed():
        ip_address = request.remote_addr
        requested_url = request.url
        referer_page = request.referrer if request.referrer else ""
        page_name = request.path
        query_string = str(request.query_string)
        user_agent = request.user_agent.string

        print(referer_page == requested_url)
        print("track_session():", track_session())
        if track_session():
            visitor_log_id = session['visitor_log_id'] if 'visitor_log_id' in session else 0
            no_of_visits = session['visitor_log_no_of_visits']
            current_page = request.url
            previous_page = session['visitor_log_current_page'] if 'visitor_log_current_page' in session else ''
            print(previous_page, current_page)
            if previous_page != current_page:
                add_visitor_log(
                    ip_address=ip_address,
                    requested_url=requested_url,
                    referer_page=referer_page,
                    page_name=page_name,
                    query_string=query_string,
                    user_agent=user_agent,
                    no_of_visits=no_of_visits
                )
        else:
            session.modified = True

            try:
                log = add_visitor_log(
                    ip_address=ip_address,
                    requested_url=requested_url,
                    referer_page=referer_page,
                    page_name=page_name,
                    query_string=query_string,
                    user_agent=user_agent
                )
                log_id = log.id
                # print('log_id', log_id)

                if log:
                    a = select(no_of_visits for no_of_visits in VisitorLog).limit(1)
                    print(a)

                    count = 0
                    if a:
                        count += 1
                    else:
                        count = 1

                    log.no_of_visits = count

                    session['visitor_log_track_session'] = True
                    session['visitor_log_no_of_visits'] = count
                    session['visitor_log_current_page'] = requested_url
                else:
                    session['visitor_log_track_session'] = False
            except Exception as e:
                print(e)
                session['visitor_log_track_session'] = False
                # raise e
