from flask import Blueprint
from flask_restful import Api

from app.resources.user.chat import ChatResource, HistoryResource, SearchTodayResource
from app.resources.user.login_register import ImageCodeResource, LoginResource, RegisterResource

# 创建蓝图对象
user_chat = Blueprint('chat', __name__)

# 创建api对象
user_api = Api(user_chat)

# 添加json外层包装
from utils.output import output_json
user_api.representation('application/json')(output_json)

# 添加类视图
user_api.add_resource(ChatResource,'/api/chat')
user_api.add_resource(HistoryResource,'/history')
user_api.add_resource(ImageCodeResource,'/imagecode')
user_api.add_resource(LoginResource,'/login')
user_api.add_resource(RegisterResource,'/register')
user_api.add_resource(SearchTodayResource,'/query/tody')



from . import test