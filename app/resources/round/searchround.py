from flask_restful import Resource
from flask_restful.reqparse import RequestParser


class SearchRoundResource(Resource):
    def post(self):
        parser = RequestParser()
        parser.add_argument('sesskey',required=True,location='json')
        parser.add_argument('roundkey',required=True,location='json')
        args = parser.parse_args()

        sesskey = args.sesskey
        roundkey = args.roundkey


        name = ["张三盗窃电动⻋","张三盗窃电动⻋","张三盗窃电动⻋","张三盗窃电动⻋","张三盗窃电动⻋","张三盗窃电动⻋","张三盗窃电动⻋","张三盗窃电动⻋","张三盗窃电动⻋","张三盗窃电动⻋"]
        bamj = ["邹⼩⻥","邹⼩⻥","邹⼩⻥","邹⼩⻥","邹⼩⻥","邹⼩⻥","邹⼩⻥","邹⼩⻥","邹⼩⻥","邹⼩⻥"]
        ajxz = ["盗窃案","盗窃案","盗窃案","盗窃案","盗窃案","盗窃案","盗窃案","盗窃案","盗窃案","盗窃案"]
        place = ["深圳市南⼭区粤海街道科苑路23号讯美科技⼴场3栋23A","深圳市南⼭区粤海街道科苑路23号讯美科技⼴场3栋23A","深圳市南⼭区粤海街道科苑路23号讯美科技⼴场3栋23A","深圳市南⼭区粤海街道科苑路23号"]
        people = ["张⼩⾬","张⼩⾬","张⼩⾬","张⼩⾬","张⼩⾬","张⼩⾬","张⼩⾬","张⼩⾬","张⼩⾬","张⼩⾬"]

        table = {"案件ID":["A83","B45","A32","A79","B98","C23","A24","A25","A26","B78"],
 			    "案件名称":name,
                "案发时间":["2018.07.02 14:23","2018.07.02 14:23","2018.07.02 14:23","2018.07.02 14:23","2018.07.02 14:23","2018.07.02 14:23","2018.07.02 14:23","2018.07.02 14:23","2018.07.02 23:34"],
 	            "案发地点":place,
 	            "办案⺠警":bamj,
 	            "案件性质":ajxz,
 	            "报警⼈":people,
                "联系电话":["13522511892","13522511892","13522511892","13522511892","13522511892","13522511892","13522511892","13522511892","13522511892","13522511892"]
                 }

        datasource = ["本地","浙江省"]
        Rcondic = {"F1":"查询主类：案件","F2":"案发时间：2020-02-19","F3":"案件地址：南山区"}
        return {
 			"RoundID":"R1",
 			"query": "查⼀下深圳这三个⽉的犯罪记录",
 			"RoundName": "案件筛选",
 			"qtime": "2020021801",
 			"roundKey": "user20200109s1r1",
 			"Rcondic": Rcondic,
			"datasource": datasource,
 			"tablelLen": "10",
 			"tableName":"案件信息表",
 			"table":table
            }


