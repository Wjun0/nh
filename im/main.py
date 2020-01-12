
from eventlet import monkey_patch
monkey_patch()

from server import app
import eventlet.wsgi


if __name__ == '__main__':
    # 监听端口
    socket = eventlet.listen(('192.168.1.125', 8001))
    # 启动服务器
    print('hello')
    import time
    print(time.localtime())
    eventlet.wsgi.server(socket, app)
