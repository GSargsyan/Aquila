from functools import wraps
from flask import g, redirect


def login(pid):
    session['pid'] = pid


def authorize():
    if 'pid' not in session:
        return redirect('login.html')
    g.player = players.find_by_id(session['pid'])
