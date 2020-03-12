import datetime
import json
import time

import requests
from flask import current_app, g
from flask_restful import Resource
from flask_restful.inputs import natural
from flask_restful.reqparse import RequestParser
from sqlalchemy import and_
from sqlalchemy.orm import load_only

from models import db
from models.history import HistoryDialogue
from app import redis_client
from models.round import RoundInfo
from models.session import SessionInfo
from utils.decorators import login_required


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
def get_data(query):
    url = "http://10.4.1.217:8822/api/get_ner"
    r = requests.post(url, json={"query":query})
    data = {}
    if r.status_code == 200:
        data = json.loads((r.text))
    return data


    # url = "http://192.168.1.105:8081/ner/"
    # result = requests.post(url, data=json.dumps(inputdata))
    # data = {}
    # if result.status_code == 200:
    #     data = json.loads(result.text)

    # return data



class ChatResource(Resource):
    '''聊天'''
    method_decorators = [login_required]
    def post(self):
        starTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

        parser = RequestParser()
        parser.add_argument('type',required=True,location='json')
        parser.add_argument('sesskey',required=True,location='json')
        parser.add_argument('question',required=True,location='json')
        parser.add_argument('roundkey',location='json')
        args = parser.parse_args()

        question = args.question
        sesskey = args.sesskey
        type = args.type
        roundkey = args.roundkey

        if not roundkey:
            roundkey = "R1"


        name = ["张三盗窃电动⻋", "张三盗窃电动⻋", "张三盗窃电动⻋", "张三盗窃电动⻋", "张三盗窃电动⻋", "张三盗窃电动⻋", "张三盗窃电动⻋", "张三盗窃电动⻋", "张三盗窃电动⻋",
                "张三盗窃电动⻋"]
        bamj = ["邹⼩⻥", "邹⼩⻥", "邹⼩⻥", "邹⼩⻥", "邹⼩⻥", "邹⼩⻥", "邹⼩⻥", "邹⼩⻥", "邹⼩⻥", "邹⼩⻥"]
        ajxz = ["盗窃案", "盗窃案", "盗窃案", "盗窃案", "盗窃案", "盗窃案", "盗窃案", "盗窃案", "盗窃案", "盗窃案"]
        place = ["深圳市南⼭区粤海街道科苑路23号讯美科技⼴场3栋23A", "深圳市南⼭区粤海街道科苑路23号讯美科技⼴场3栋23A", "深圳市南⼭区粤海街道科苑路23号讯美科技⼴场3栋23A",
                 "深圳市南⼭区粤海街道科苑路23号"]
        people = ["张⼩⾬", "张⼩⾬", "张⼩⾬", "张⼩⾬", "张⼩⾬", "张⼩⾬", "张⼩⾬", "张⼩⾬", "张⼩⾬", "张⼩⾬"]

        table = {"案件ID": ["A83", "B45", "A32", "A79", "B98", "C23", "A24", "A25", "A26", "B78"],
                 "案件名称": name,
                 "案发时间": ["2018.07.02 14:23", "2018.07.02 14:23", "2018.07.02 14:23", "2018.07.02 14:23",
                          "2018.07.02 14:23", "2018.07.02 14:23", "2018.07.02 14:23", "2018.07.02 14:23",
                          "2018.07.02 23:34"],
                 "案发地点": place,
                 "办案⺠警": bamj,
                 "案件性质": ajxz,
                 "报警⼈": people,
                 "联系电话": ["13522511892", "13522511892", "13522511892", "13522511892", "13522511892", "13522511892",
                          "13522511892", "13522511892", "13522511892", "13522511892"]
                 }

        datasource = ["本地", "浙江省"]
        Rcondic = {"F1": "查询主类：案件", "F2": "案发时间：2020-02-19", "F3": "案件地址：南山区"}

        roundinfo = {"roundkey":roundkey,"roundID":roundkey,"Rcondic":Rcondic,"datasource":datasource}
        roundinfo_list = []
        try:
            s = SessionInfo.query.options(load_only(SessionInfo.sessKey,SessionInfo.sessCondic,SessionInfo.number,SessionInfo.roundInfo)).\
                filter(SessionInfo.sessKey == sesskey).first()
            if s:
                r = json.loads(s.roundInfo)
                r.append(roundinfo)
                SessionInfo.query.options(load_only(SessionInfo.sessKey)).filter(SessionInfo.sessKey ==s.sessKey).\
                    update(
                    {"endTime":time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),
                     "number":s.number + 1,
                     "roundInfo":json.dumps(r)}
                )
            else:
                roundinfo_list.append(roundinfo)

                data = SessionInfo(sessName = sesskey,
                                   sessID = sesskey,
                                   sessCondic = json.dumps(Rcondic),
                                   sessKey = sesskey,
                                   starTime = starTime,
                                   endTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),
                                   number = 1,
                                   owner = g.userid,
                                   roundInfo = json.dumps(roundinfo_list))
                db.session.add(data)
                db.session.commit()
        except Exception as e:
            current_app.logger.error(e)
            return {"message":"error","data":"数据库保存错误！"}

        # 将算法返回的数据保存到数据库
        try:
            data = RoundInfo(
                roundName = "案件筛选",
                roundID = roundkey,
                roundCondic = json.dumps(Rcondic),
                starTime = starTime,
                endTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),
                roundKey = roundkey,
                query = question,
                tableInfo = table
            )
            db.session.add(data)
            db.session.commit()

        except Exception as e:
            current_app.logger.error(e)
            return {"message":"error","data":"数据库保存失败！"}

        result = {
            "RoundID": roundkey,
            "query": "查⼀下深圳这三个⽉的犯罪记录",
            "RoundName": "案件筛选",
            "qtime": "2020021801",
            "roundKey": roundkey,
            "Rcondic": Rcondic,
            "datasource": datasource,
            "tablelLen": "10",
            "tableName": "案件信息表",
            "table": table
        }
        try:
            data = json.dumps(result)
            redis_client.hset(sesskey,roundkey,data)
        except Exception as e:
            current_app.logger.erroer(e)
            return {"message":"error","data":"redis保存失败"}


        return result


        # if session_id == "RR":
        #
        #     # 获取算法数据
        #     inputdata = {"sessid": 'R0',
        #                  "query": question,
        #                  "table": "None"}
        #
        #     try:
        #         # result = get_data(inputdata)
        #         result = get_data(question.strip())
        #
        #     except Exception as e:
        #         current_app.logger.error(e)
        #         return {'message': '服务未启动'}
        #
        #     #将数据保存到redis
        #     session_id = session_id[0] + str(1)
        #
        #     try:
        #         save_result_to_redis(result,session_id)
        #     except Exception as e:
        #         current_app.logger.error(e)
        #         return {'message': "error","data": "请求失败"}, 400
        #
        #
        #     # 将数据保存到mysql
        #     save_history_to_mysql(session_id,result,question)
        #
        #     return result
        #
        # else:
        #     # 否则基于session_id查询
        #
        #     # 向redis 取出相应的问题和session_id,调用算法获取数据
        #     redis_data = redis_client.hget(session_id,session_id)
        #
        #     table = "None"
        #     if redis_data:
        #         table = json.loads(redis_data)
        #
        #     inputdata = {"sessid": session_id,
        #                  "query": question,
        #                  "table": table}
        #
        #     try:
        #         result = get_data(inputdata)
        #     except Exception as e:
        #         current_app.logger.error(e)
        #         return {'message': '服务未启动'}
        #
        #     #将查询结果保存到redis
        #     try:
        #         session_id = result["sessID"]
        #         save_result_to_redis(result,session_id)
        #     except Exception as e:
        #         current_app.logger.error(e)
        #         return {'message': "error","data": "未获取到数据"}, 400
        #
        #     #将查询结果保存到mysql
        #     save_history_to_mysql(session_id, result, question)
        #
        #     return result


#今日查询
class SearchTodayResource(Resource):
    method_decorators = [login_required]
    def get(self):
        userid = g.userid
        searchstartTime = time.strftime("%Y-%m-%d 0:0:0",time.localtime())
        searchendTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

        try:
            data = SessionInfo.query.filter(and_(SessionInfo.endTime>searchstartTime,SessionInfo.endTime<searchendTime,SessionInfo.owner==userid)).all()
        except Exception as e:
            current_app.logger.error(e)
            return {"message":"error","data":"时间操作有误！"}

        datalist = []
        for i in data:
            dic = {
                "sessID":i.sessID,
                "sessName":i.sessName,
                "sessCondic":json.loads(i.sessCondic),
                "qtime": i.starTime.isoformat().replace('T',' '),
                "sesskey":i.sessKey,
                "roundInfo":json.loads(i.roundInfo)
            }
            datalist.append(dic)

        return datalist



#历史查询
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

