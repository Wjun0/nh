
from flask import jsonify
from werkzeug.security import check_password_hash

from . import user_chat


@user_chat.route('/test',methods=['get'])
def my_test():
    print('ok')
    dict = {"name":"张三"}
    return jsonify(dict)

