import requests
import json
import sys
import datetime
from functools import wraps

def timing(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = datetime.datetime.now()
        r = func(*args, **kwargs)
        end = datetime.datetime.now()
        print ('[{}] cost {}'.format(func.__name__, end - start))
        return r
    return wrapper

@timing
def get_result(query):
    """
    中控调用函数
    refer: 是否带有引用, 引用类问句还有点问题
    sess_id, table 暂时没用
    """
    url = "http://10.4.1.217:8855/api/get_query"
    r = requests.post(url, json={'query': query, 'sess_id': 0, 'table':'', 'refer':'', 'user':'wayne'})
    if r.status_code == 200:
        return json.loads(r.text)

def test(query):
    result = get_result(query)
    if result['code'] != 200:
        print (result['msg'])
        exit(0)
    print ('Query', query)
    print (query)
    print ('***NER***')
    for i in result['ner_entity']:
        print ('实体:',i['entity'], '类别:',i['type'])
    print ('***NER意图***')
    print (result['ner_intent'].strip())
    print ('***子图***')
    for t in json.loads(result['subgraph'])['table']:
        print (t)
    print ('***SQL***')
    print (result['sql'])
    print ("#"*100)
    print(result)

if __name__ == "__main__":
    query = '帮我查查嘉兴的王军'
    # test(query)
    # query = '浙江嘉兴大冲都市花园的张三三'
    # test(query)
    # query = sys.argv[1]
    ls = [{"id":"id"}]
    j = json.dumps(ls)
    print(j)
    k = json.loads(j).append({"name":"test"})
    q = json.loads(j)
    q.append({"name":"test"})
    print(q)
    print(k)
    print(ls)

