#nanhu2.0
FROM python:3.6
WORKDIR /home/python/nanhu/
COPY requirements.txt ./
RUN pip install -r requirements.txt -i  http://pypi.douban.com/simple --trusted-host pypi.douban.com
COPY . .
CMD ["flask","run","app/main.py"]