
import json,requests
import time
from datetime import datetime

from flask import jsonify
from requests import Session, Request

from app import redis_client, redis_client_verify

from models import db
from models.users import Users

from . import user_chat

from werkzeug.security import generate_password_hash,check_password_hash

@user_chat.route('/test/register')
def register():
    userId = "522422199412263654"
    cardId = "522422199412263654"
    username = "admin"
    password = "123456"
    group = "技术部"
    phone = "18212707348"
    type = '1'
    regTime = datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S')
    pd = generate_password_hash(password)

    try:
        data = Users(
            userId = userId,
            cardId = cardId,
            username = username,
            passWord = pd,
            group = group,
            phone = phone,
            type = type,
            regTime = regTime

        )
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        print(e)
        print('添加用户错误')

    return jsonify({"message":"ok"})








@user_chat.route('/test',methods=['get'])
def my_test():
    print('ok')
    dict = {"name":"张三","age":112}

    redis_client.expire('Round2',1)  #设置0.01秒过期
    return jsonify(dict)


# 测试redis
@user_chat.route('/test/redis',methods=['get'])
def redis_test():
    redis_client_verify.setex("admin",300,"admin")

    # redis_client.hset('Round2','test1','{name:test1}')
    # redis_client.hset('Round2','test2','{name:test2}')

    data = redis_client_verify.get("admin")
    print(data)
    # print(json.loads(result))
    # data = requests.get('http://192.168.1.125:8000/test')
    # print(json.loads(data.content.decode()))

    # s = Session()
    # req = Request('GET',url='http://192.168.1.125:8000/test')
    # prepped = s.prepare_request(req)

    # resp = s.send(prepped)
    # print(resp.status_code)
    # print(json.loads(resp.content.decode()))

    return jsonify({"message":'ok'})


