from flask import jsonify
from app import create_app

# 创建应用

app = create_app('dev')


@app.route('/')
def route_map():
    """定义根路由, 显示所有的路由规则"""

    return jsonify({rule.endpoint: rule.rule for rule in app.url_map.iter_rules()})


