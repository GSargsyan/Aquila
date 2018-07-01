from functools import wraps
from flask import g, redirect, session, request

from app import Players


REQ_AUTH_URLS = ('/game')


def authorize():
    if 'pid' in session:
        g.player = Players.find_by_id(session['pid'])
        return True

    if request.path in REQ_AUTH_URLS:
        return False

    return True
