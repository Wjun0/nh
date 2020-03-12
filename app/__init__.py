from flask import Flask
from os.path import *
import sys

from redis import StrictRedis

# 添加common路径到模块查询路径中
BASE_DIR = dirname(dirname(abspath(__file__)))
sys.path.insert(0, BASE_DIR + "/common")

from settings.default import config_dict


redis_client = None     # type:  StrictRedis
redis_client_verify = None

def create_flask_app(config_type):
    """创建Flask应用"""
    # 创建应用
    app = Flask(__name__)

    #跨域解决
    from flask_cors import CORS
    CORS(app,resources=r'/*')

    # 根据配置类型选择配置子类
    config_class = config_dict[config_type]
    # 先加载默认配置
    app.config.from_object(config_class)

    return app


def register_extensions(app):
    """注册组件"""
    # 初始化数据库组件
    from models import db
    db.init_app(app)

    global redis_client
    global redis_client_verify

    redis_client = StrictRedis(
        host=app.config['REDIS_HOST'],
        port=app.config['REDIS_PORT'],
        decode_responses=True)

    redis_client_verify = StrictRedis(
        host=app.config['REDIS_HOST'],
        port=app.config['REDIS_PORT'],
        decode_responses=True,
        db=1)


def register_blueprint(app:Flask):
    """注册蓝图对象"""
    from app.resources.user import user_chat
    app.register_blueprint(user_chat)

    from app.resources.session import user_session
    app.register_blueprint(user_session)

    from app.resources.round import user_round
    app.register_blueprint(user_round)


def create_app(config_type):
    """应用初始化"""
    # 创建Flask应用
    app = create_flask_app(config_type)
    # 初始化组件
    register_extensions(app)

    # 添加日志
    app.config['PROPAGATE_EXCEPTIONS'] = False      #设置传播异常
    from utils.log import create_logger
    create_logger(app)


    from utils.middlewares import get_userinfo
    app.before_request(get_userinfo)

    # 注册蓝图
    register_blueprint(app)

    return app
