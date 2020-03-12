from flask import Blueprint
from flask_restful import Api

from app.resources.session.addsession import AddSessionResource

user_session = Blueprint('session',__name__)

api = Api(user_session)

# 添加json外层包装
from utils.output import output_json
api.representation('application/json')(output_json)


api.add_resource(AddSessionResource,'/add/session')