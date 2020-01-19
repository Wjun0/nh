import time

from lxml.html import etree
import pandas as pd
import requests



class Tieba(object):
    def __init__(self,name):
        self.url = "https://tieba.baidu.com/f?ie=utf-8&kw=%s&fr=search"%name

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36"
        }


    def get_data(self,url,):
        resp = requests.get(url,headers=self.headers)
        return resp.content.decode()

    def parse_data(self,data):
        data = data.replace('<!--','').replace('-->','')
        html = etree.HTML(data)

        #获取需要的数据    <Element li at 0x27ab496fac8>对象
        el_list = html.xpath('//li[@class=" j_thread_list clearfix"]/div')

        next_url_list = html.xpath('//a[@class="next pagination-item "]/@href')

        time.sleep(1)
        return el_list,next_url_list


    def save_data(self,data):
        # <Element li at 0x27ab496fac8> 对象就可以继续用xpath进行解析
        for i in data:
            title = i.xpath('./div[2]/div/div/a/@title')
            url = i.xpath('./div[2]/div/div/a/@href')

            file = 'baudu.csv'
            data = pd.DataFrame({"title": title, "url": url})
            data.to_csv(file, index=False, mode='a+', header=False)


    def run(self):
        #url
        #headers

        while True:
            #发送请求
            data = self.get_data(self.url)

            #从相应中提取数据
            data_list,next_url_list = self.parse_data(data)

            #保存数据
            self.save_data(data_list)

            #结束判断
            if len(next_url_list) == 0:
                break

            # 替换url
            self.url = 'https:' + next_url_list[0]


if __name__ == '__main__':
    tieba = Tieba('王军')

    tieba.run()




