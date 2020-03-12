from flask import g, abort
from functools import wraps


def login_required(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
        if g.userid:
            return f(*args,**kwargs)
        else:
            abort(401)
    return wrapper


