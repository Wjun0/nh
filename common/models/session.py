from models import db


class SessionInfo(db.Model):
    __tablename__ = 'session_history'

    sessName = db.Column(db.String, primary_key=True, doc="session名称")
    sessID = db.Column(db.String, doc="sessID")
    sessCondic = db.Column(db.String, doc="session查询条件")
    sessKey = db.Column(db.String, doc='round唯一标识')
    starTime = db.Column(db.String, doc='查询开始时间')
    endTime = db.Column(db.String, doc='查询结束时间')
    number = db.Column(db.String, doc='round数量')
    owner = db.Column(db.String, doc="查询用户")
    roundInfo = db.Column(db.String, doc="查询信息")