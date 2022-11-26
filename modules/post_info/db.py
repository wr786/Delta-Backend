from flask_sqlalchemy import SQLAlchemy
from ..utils import db
from datetime import datetime

class PostInfo(db.Model):
   # 表名
   __tablename__ = 'post_info'
   # 字段
   id = db.Column('post_info_id', db.Integer, primary_key=True, autoincrement=True)
   user_id = db.Column('user_info_id', db.Integer)
   headline = db.Column(db.String(100))
   tags = db.Column(db.String(100), index=True)
   price_and_number = db.Column(db.Float)
   info = db.Column(db.String(200))
   picture = db.Column(db.String(5000)) 
   # createTime = db.Column(db.DateTime, default=datetime.now)

   def __init__(self, **kwargs):
        super(PostInfo, self).__init__(**kwargs)

class Comment(db.Model):
    __tablename__ = 'comment'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pid = db.Column(db.Integer, index=True)
    sender = db.Column(db.Integer, index=True)
    content = db.Column(db.String(500))
    createTime = db.Column(db.DateTime, default=datetime.now, index=True)

    def __init__(self, **kwargs):
        super(Comment, self).__init__(**kwargs)