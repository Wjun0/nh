import json

import requests
import tesserocr
from redis import StrictRedis


def get_ner(query):
    url = "http://10.4.1.217:8822/api/get_ner"
    data = {"query": query}
    r = requests.post(url, json=data)
    print(json.loads(r.text))
    return json.loads(r.text)



def test_tessorocr():
    from PIL import Image
    image = Image.open('0.jpg')
    image = image.convert('L')
    threshold = 210
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    image = image.point(table,'1')
    result = tesserocr.image_to_text(image)
    print(result)


if __name__ == '__main__':
    # redis_client = StrictRedis(host="10.4.1.217",port=6377)
    #
    # redis_client.set("wangjun","hello",200)
    # data = redis_client.get("wangjun")
    #
    # print(data)image

    # get_ner('深圳大冲都市花园的邹鸿岳')

    test_tessorocr()