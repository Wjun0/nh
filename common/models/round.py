from . import db


class RoundInfo(db.Model):
    __tablename__ = 'round_history'

    roundName = db.Column(db.String, primary_key=True, doc="用户名")
    roundID = db.Column(db.String, doc="roundID")
    roundCondic = db.Column(db.String, doc="round查询条件")
    starTime = db.Column(db.String, doc='查询开始时间')
    endTime = db.Column(db.String, doc='查询结束时间')
    roundKey = db.Column(db.String, doc='round唯一标识')
    query = db.Column(db.String, doc="问句")
    tableInfo = db.Column(db.String, doc="查询信息")
