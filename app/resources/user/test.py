import json,requests

from flask import jsonify
from requests import Session, Request
from werkzeug.security import check_password_hash

from app import redis_client
from . import user_chat


@user_chat.route('/test',methods=['get'])
def my_test():
    print('ok')
    dict = {"name":"张三"}

    redis_client.expire('Round2',1)  #设置0.01秒过期
    return jsonify(dict)


# 测试redis
@user_chat.route('/test/redis',methods=['get'])
def redis_test():
    result = redis_client.hget('admin02','R1')

    redis_client.hset('Round2','test1','{name:test1}')
    redis_client.hset('Round2','test2','{name:test2}')

    # print(json.loads(result))
    # data = requests.get('http://192.168.1.125:8000/test')
    # print(json.loads(data.content.decode()))

    s = Session()
    req = Request('GET',url='http://192.168.1.125:8000/test')
    prepped = s.prepare_request(req)

    resp = s.send(prepped)
    print(resp.status_code)
    print(json.loads(resp.content.decode()))

    return jsonify({"message":'ok'})


