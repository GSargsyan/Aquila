from functools import wraps
from flask import g, redirect, session, request

from app import Players


REQ_AUTH_URLS = ('/game', '/home')


def login(pid):
    session['pid'] = pid


def authorize():
    if request.url not in REQ_AUTH_URLS:
        return True
    if 'pid' not in session:
        return False

    g.player = Players.find_by_id(session['pid'])
    return True
