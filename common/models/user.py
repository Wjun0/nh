from . import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer,primary_key=True,doc="用户id")
    name = db.Column(db.String,doc="用户名")
    email = db.Column(db.String,doc="邮箱")
    age = db.Column(db.String,doc="年龄")
