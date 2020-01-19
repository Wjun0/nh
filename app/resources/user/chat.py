import datetime
import json
import time

import requests
from flask import current_app
from flask_restful import Resource
from flask_restful.inputs import natural
from flask_restful.reqparse import RequestParser

from models import db
from models.history import HistoryDialogue
from app import redis_client
from utils.TfServer import TFserver



def save_history_to_mysql(session_id,result,question):
    data = HistoryDialogue(
        time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        session_id=session_id,
        username=session_id,
        data=json.dumps(result),
        question=question
    )
    try:
        db.session.add(data)
        db.session.commit()

    except Exception as e:
        current_app.logger.error(e)

        db.session.rollback()
        return {'message': "error",
                "data": "请求失败"}, 400


def save_result_to_redis(result,session_id):
    try:
        json_str_data = json.dumps(result)
        redis_client.hset(session_id,session_id,json_str_data)
    except Exception as e:
        current_app.logger.error(e)




def handle_time(start,end):
    if ':' in start:
        try:
            start_time = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            current_app.logger.error(e)
            return None,None
    else:
        try:
            start_time = datetime.datetime.strptime(start, '%Y-%m-%d')
        except Exception as e:
            current_app.logger.error(e)
            return None,None

    if ':'in end:
        try:
            end_time = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            current_app.logger.error(e)
            return None,None
    else:
        try:
            end = datetime.datetime.strptime(end, '%Y-%m-%d')
            end_time = end + datetime.timedelta(days=1)
        except Exception as e:
            current_app.logger.error(e)
            return None,None

    return start_time,end_time


def get_keyword(question,table):
    url = "http://49.233.73.250:8811/api/chat"
    data = None
    r = requests.post(url, json={'query': question, 'user': 'test', 'table':table}, verify=False)

    if r.status_code == 200:
        data = json.loads(r.text)['sql'].split('\n')[0].split(': ')[-1]

    return data



#获取算法的数据
def get_data(inputdata):
    url = "http://192.168.1.105:8081/ner/"
    result = requests.post(url, data=json.dumps(inputdata))
    data = {}
    if result.status_code == 200:
        data = json.loads(result.text)

    return data



class ChatResource(Resource):
    '''聊天'''
    def post(self):
        parser = RequestParser()
        parser.add_argument('question',required=True,location='json')
        parser.add_argument('session_id',required=True,location='json')
        args = parser.parse_args()

        question = args.question
        session_id = args.session_id

        if session_id == "RR":

            # 获取算法数据
            inputdata = {"sessid": 'R0',
                         "query": question,
                         "table": "None"}

            try:
                result = get_data(inputdata)

            except Exception as e:
                current_app.logger.error(e)
                return {'message': '服务未启动'}

            #将数据保存到redis
            session_id = session_id[0] + str(1)

            try:
                save_result_to_redis(result,session_id)
            except Exception as e:
                current_app.logger.error(e)
                return {'message': "error","data": "请求失败"}, 400


            # 将数据保存到mysql
            save_history_to_mysql(session_id,result,question)

            return result

        else:
            # 否则基于session_id查询

            # 向redis 取出相应的问题和session_id,调用算法获取数据
            redis_data = redis_client.hget(session_id,session_id)

            table = "None"
            if redis_data:
                table = json.loads(redis_data)

            inputdata = {"sessid": session_id,
                         "query": question,
                         "table": table}

            try:
                result = get_data(inputdata)
            except Exception as e:
                current_app.logger.error(e)
                return {'message': '服务未启动'}

            #将查询结果保存到redis
            try:
                session_id = result["sessID"]
                save_result_to_redis(result,session_id)
            except Exception as e:
                current_app.logger.error(e)
                return {'message': "error","data": "未获取到数据"}, 400

            #将查询结果保存到mysql
            save_history_to_mysql(session_id, result, question)

            return result



class HistoryResource(Resource):
    def post(self):
        parser = RequestParser()
        parser.add_argument('start',required=True,location='json')
        parser.add_argument('end',required=True,location='json')
        args = parser.parse_args()

        start = args.start
        end = args.end

        #时间处理
        start_time,end_time = handle_time(start,end)

        if start_time is None or end_time is None:
            return {'message':'error',"data":"时间格式错误"}

        result = db.session.query(HistoryDialogue).filter(HistoryDialogue.time.between(start_time,end_time))

        data_list = []
        for i in result:
            dict = {
                'time':str(i.time),
                'username':i.username,
                'data':json.loads(i.data),
                'question':i.question,
            }
            data_list.append(dict)

        return data_list



