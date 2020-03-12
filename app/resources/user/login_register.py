from datetime import datetime,timedelta

import base64
import jwt
from flask import current_app
from flask import make_response
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.orm import load_only
from werkzeug.security import check_password_hash

from app import redis_client
from app import redis_client_verify
from libs.captcha.captcha import captcha
from models.users import Users
from utils.constants import JWT_EXPIRE
from utils.jwt_util import generate_jwt


class RegisterResource(Resource):
    def post(self):
        return {"data":"are you ok!"}






class LoginResource(Resource):
    def post(self):
        parser = RequestParser()
        parser.add_argument('username',required=True,location='json')
        parser.add_argument('password',required=True,location='json')
        # parser.add_argument('imageCode',required=True,location='json')
        args = parser.parse_args()

        # imageCode = args.imageCode
        username = args.username
        password = args.password

        # server_image_code = redis_client_verify.get("image_code")
        # if imageCode != server_image_code:
        #     return {"message":"error","data":"验证码错误！"}
        try:
            #MySQL中取出该用户，验证密码
            user = Users.query.options(load_only(Users.userId,Users.passWord)).filter(Users.username==username).first()
        except Exception as e:
            print(e)
            current_app.logger.error(e)
            return {"message": "error", 'data': "获取用户信息失败！"}

        if not check_password_hash(user.passWord,password):
            return {"message":"error",'data':"用户名或密码错误！"}

        # 生成token 返回
        # token = generate_jwt({"userId":Users.userId},expiry=datetime.utcnow() + timedelta(hours=JWT_EXPIRE))
        token = jwt.encode({"userid":user.userId,"exp":datetime.utcnow() + timedelta(hours=JWT_EXPIRE)},"key",algorithm='HS256')
        return {"token":token.decode()}





class ImageCodeResource(Resource):

    def get(self):
        # 1.生成图形验证码
        text, image = captcha.generate_captcha()
        key = 'image_code'
        redis_client_verify.setex(key, 300, text)
        response = make_response(image)
        response.headers['Content-Type'] = "image/jpg"
        # 4.返回图片
        return response