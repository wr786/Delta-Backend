from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

# 会话表
class ConvInfo(db.Model):
    __tablename__ = 'conv_info'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, notnull=True)
    name = db.Column(db.String(100))
    conType = db.Column(db.Integer) # 1=单聊，2=群聊
    convLongId = db.Column(db.String(100), unique=True, index=True)

    def __init__(self, **kwargs):
        super(ConvInfo, self).__init__(**kwargs)

# 消息表
class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, notnull=True)
    sender = db.Column(db.Integer) # , db.ForeignKey('user.id'))
    convId = db.Column(db.Integer, db.ForeignKey('conv_info.id'))
    content = db.Column(db.String(1000))
    # 本来应该还要考虑消息有序性问题，但考虑到我们的服务QPS很低，直接用id排序得了

    def __init__(self, **kwargs):
        super(Message, self).__init__(**kwargs)

# 会话设置表，虽然好像现在没什么要设置的
class ConvSetting(db.Model):
    __tablename__ = 'conv_setting'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, notnull=True)
    uid = db.Column(db.Integer)
    convId = db.Column(db.Integer, db.ForeignKey('conv_info.id'))
    createTime = db.Column(db.DateTime, default=datetime.now)
    # readTilMid = db.Column(db.Integer)  # 已读计数

    def __init__(self, **kwargs):
        super(ConvSetting, self).__init__(**kwargs)