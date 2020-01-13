import os 
import re 
import numpy as np 
import codecs 
import json 
import random

class TFserver(object):
    def __init__(self):
        self.path = "./temp_table.json"

        def loaddata(fpath):
            alldata = []
            ff = codecs.open(fpath,'r','utf-8')
            for item in ff:
                elem = json.loads(item)
                alldata.append(elem)
            return alldata 
        
        self.alltable = loaddata(self.path)


    def get_sessionID(self,sessID):
        num = re.findall(r'\d+',sessID)[0]
        #num = filter(str.isdigit,sessID)[0]
        string = sessID.replace(num,"")
        sessionID = str(string)+str(int(num)+1)
        return sessionID

    def get_result(self,QApairs):

        query = QApairs["query"]
        sessID = QApairs["sessID"]
        #table = QApairs["table"]
        minid,maxid = 0, len(self.alltable)-1
        idx = random.randint(minid,maxid)
        temp = self.alltable[idx]

        #table = temp["table"]
        table = {}
        columns = temp["table"][0]
        values = temp["table"][1::]
        new_values = np.array(values).T
        for idx,col in enumerate(columns):
            table[col] = list(new_values[idx])

        title = temp["title"]
        info = temp["condiction"] 
        sessionID = self.get_sessionID(sessID)
        
        result = {"info": [info],
                  "title": title,
                  "sessID": sessionID,
                  "condiction":[('F0 查询类型','人员'),('F1 查询条件','身份证号'),('F2 监控时间','2019-01-02 12:23:45')],
                  "dataUrl": [("本地","https://baidu.com"),("省数据","https://google.com")],
                  "ansType": "0",
                  "answer": table}
        return result 


if __name__ == "__main__": 
    TF = TFserver()
    query = {"query":"查查邹鸿岳的身份证",
             "sessID":"Round2",
             "table": None}
    result = TF.get_result(query)
    print(result)