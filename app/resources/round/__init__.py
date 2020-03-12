from flask import Blueprint
from flask_restful import Api

from app.resources.round.searchround import SearchRoundResource
from app.resources.round.changeround import  ChangeRoundResource
user_round = Blueprint('round',__name__)
user_api = Api(user_round)


from utils.output import output_json
user_api.representation('application/json')(output_json)


user_api.add_resource(SearchRoundResource,"/search/round")
user_api.add_resource(ChangeRoundResource,"/change/round")

