
from . import db

class HistoryDialogue(db.Model):
    __tablename__ = "historical_dialogue_table"

    id = db.Column(db.Integer,primary_key=True,doc="id")
    time = db.Column(db.String,doc="时间")
    session_id = db.Column(db.String,doc="会话id")
    username = db.Column(db.String,doc="用户名")
    data = db.Column(db.String,doc="数据")
    question = db.Column(db.String,doc="问句")

