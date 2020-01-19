import requests
import json 

def client(text,title,table):  
    '''客户端调用webserver'''
    url = "http://192.168.1.105:8081/ner/"
    inputdata = {"sessid":"R01",
                "query":text,
                "table":table}
    req = requests.post(url,data=json.dumps(inputdata))
    result = json.loads(req.text)
    return result 

table = "None"
title = "None"
while True:
    text = input("Enter: ")
    text = text.replace(" ","")
    if text == "exit":
        break 
    result = client(text,title,table)
    table = result["answer"]
    title = result["title"]
    print(result)