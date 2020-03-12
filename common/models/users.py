from . import db

class Users(db.Model):
    __tablename__ = "users"

    userId = db.Column(db.Integer,primary_key=True,doc="用户id")
    username = db.Column(db.String,doc="用户名")
    passWord = db.Column(db.String,doc="密码")
    cardId = db.Column(db.String,doc="身份证号")
    group = db.Column(db.String,doc="部门")
    phone = db.Column(db.String,doc="电话")
    type = db.Column(db.String,doc="类型")
    regTime = db.Column(db.String,doc="注册时间")
    auditTime = db.Column(db.String,doc="审核时间")
    auditor = db.Column(db.String,doc="审核人")
    reason = db.Column(db.String,doc="审核原因")
    rights = db.Column(db.String,doc="权限")

