
from flask import request,g

# from utils.jwt_util import verify_jwt
import jwt

def get_userinfo():
    header = request.headers.get("Authorization")
    g.userid = None
    if header and  header.startswith("Jwt"):
        token = header[4:]
        payload = jwt.decode(token,"key",algorithms='HS256')
        if payload:
            g.userid = payload.get('userid')
