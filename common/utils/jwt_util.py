import jwt
from flask import current_app


def generate_jwt(payload, expiry, secret=None):
    _payload = {'exp': expiry}
    _payload.update(payload)
    if not secret:
        # secret = current_app.config['JWT_SECRET']
        secret = "wjtest"
    token = jwt.encode(_payload, secret)
    return token.decode()



def verify_jwt(token, secret=None):
    if not secret:
        secret = current_app.config['JWT_SECRET']
    try:
        payload = jwt.decode(token, secret)
    except jwt.PyJWTError:
        payload = None
    return payload
