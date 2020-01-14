import datetime
import json
import time

from flask import current_app
from flask_restful import Resource
from flask_restful.inputs import natural
from flask_restful.reqparse import RequestParser

from models import db
from models.history import HistoryDialogue
from models.user import User
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

        return {'message': "error",
                "data": "请求失败"}, 400


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



class ChatResource(Resource):
    '''聊天'''
    def post(self):
        parser = RequestParser()
        parser.add_argument('question',required=True,location='json')
        parser.add_argument('session_id',required=True,location='json')
        args = parser.parse_args()

        question = args.question
        session_id = args.session_id

        if session_id == "Round0":

            # 获取算法数据
            query = {"query": question,
                     "sessID": session_id,
                     "table": None}

            TF = TFserver()
            result = TF.get_result(query)

            #将数据保存到redis
            save_result_to_redis(result,session_id)

            # 将数据保存到mysql
            save_history_to_mysql(session_id,result,question)

            return result

        else:
            # 否则基于session_id查询

            # 向redis 取出相应的问题和session_id,调用算法获取数据
            redis_data = redis_client.hget(session_id,session_id)

            query = {"query": question,
                     "sessID": session_id,
                     "table": redis_data}

            TF = TFserver()
            result = TF.get_result(query)

            session_id = result.get('sessID')


            #将查询结果保存到redis
            save_result_to_redis(result,session_id)

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



