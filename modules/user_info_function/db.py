from flask_sqlalchemy import SQLAlchemy
from ..utils import db


class UserInfo(db.Model):
   # 表名
   __tablename__ = 'user_info'
   # 字段
   id = db.Column('user_info_id', db.Integer, primary_key=True)
   name = db.Column(db.String(100))
   email = db.Column(db.String(100))
   info = db.Column(db.String(500))
   picture = db.Column(db.String(5000))


class StarsAndFans(db.Model):
    # 表名
    __tablename__ = 'follow_relationship'
    # 字段
    id = db.Column('follow_id', db.Integer, primary_key=True, autoincrement=True)
    star_id = db.Column(db.Integer)
    fan_id = db.Column(db.Integer)