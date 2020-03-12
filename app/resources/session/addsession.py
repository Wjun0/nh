from flask_restful import Resource
from flask_restful.reqparse import RequestParser
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