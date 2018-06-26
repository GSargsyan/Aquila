from functools import wraps
from flask import g

def authorize(f):
    @wraps(f)
    def require_auth(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return require_auth


def login(user_id):
    g.user_id = user_id
