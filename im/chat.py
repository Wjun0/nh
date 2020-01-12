from server import sio
from flask import Request


@sio.on('chat',namespace='/api/chat')
def on_chat(sid, data):

    # 接收数据
    print("用户发送的数据: %s" % data)

    response = data

    # 将AI的回复返回给客户端
    sio.emit('chat', response, room=sid)





@sio.on('connect')
def on_connect(sid, envroin):
    """连接时触发
    """
    request = Request(envroin)
    sio.enter_room(sid)


@sio.on('disconnect')
def on_disconnect(sid):
    # 断开连接后, 退出所有的房间
    for room in sio.rooms():
        sio.leave_room(sid, room)
