from flask import current_app
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from models import db
from models.session import SessionInfo
from utils.decorators import login_required



class AddSessionResource(Resource):
    method_decorators = [login_required]
    def post(self):
        parser = RequestParser()
        parser.add_argument('type',required=True,location='json')
        args = parser.parse_args()
        type = args.get('type')
        data = {}
        if type == "0":
            data = {
		        "status":"0",
		        "sessID":"S03",
		        "sessKey":"user20200120s3",
		        "roundInfo":[], #返回的roundInfo是空的list; 后期再讨论
	}
        return data




class DelSessionResource(Resource):
    method_decorators = [login_required]
    def delete(self,sesskey):
        try:
            SessionInfo.query.filter(SessionInfo.sessKey==sesskey).delete()
            db.session.commit()
        except Exception as e:
            current_app.logger.error(e)
            return {"message":"error","data":"delete faild"}

        return "success"
