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
            # session_id等于0 新建会话

            # 获取算法数据
            query = {"query": question,
                     "sessID": session_id,
                     "table": None}

            TF = TFserver()
            result = TF.get_result(query)

            #将数据保存到redis
            # json_str_data = json.dumps(data_dict)
            # redis_client.hset('admin02','R1',json_str_data)

            # 将数据保存到mysql

            #生成日志
            # current_app.logger.error('errormessage')

            return result

        else:
            # 否则基于session_id查询
            query = {"query": question,
                     "sessID": session_id,
                     "table": None}

            TF = TFserver()
            result = TF.get_result(query)

            return result

        # his = HistoryDialogue(
        #     time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),
        #     session_id = "zs_1",
        #     username= "张三",
        #     data = {"username":"shangdan","age":"23"},
        #     question = question
        # )
        # try:
        #     db.session.add(his)
        #     db.session.commit()
        # except:
        #     db.session.rollback()
        #     return {'message':"error",
        #             "data":"添加数据失败"},400

        # 根据前端的数据调用相应的算法获取数据

        datas = db.session.execute("select * from historical_dialogue_table order by id desc").fetchone()
        result = {
            "id":datas.id,
            "time":str(datas.time),
            "session_id":datas.session_id,
            "username":datas.username,
            "data":datas.data,
            "question":datas.question
        }

        return result


    # 测试redis
    def get(self):
        result = redis_client.hget('admin02','R1')

        print(json.loads(result).get('question'))

        return {"data":result}


class HistoryResource(Resource):
    def post(self):
        parser = RequestParser()
        parser.add_argument('start',required=True,location='json')
        parser.add_argument('end',required=True,location='json')
        args = parser.parse_args()

        start_time = args.start
        end_time = args.end

        result = db.session.query(HistoryDialogue).filter(HistoryDialogue.time.between(start_time,end_time))

        data = {}
        for i in result:
            dict = {
                'time':str(i.time),
                'username':i.username,
                'data':i.data,
                'question':i.question,
                'session_id':i.session_id
            }
            data[i.id] = dict

        return data



