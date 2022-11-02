from flask import request, flash, url_for, redirect, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()

post_info = Blueprint('post_info', __name__, url_prefix='/post_info')

db = SQLAlchemy()

class PostInfo(db.Model):
   # 表名
   __tablename__ = 'post_info'
   # 字段
   id = db.Column('post_info_id', db.Integer, primary_key = True)
   tags = db.Column(db.String(100))
   info = db.Column(db.String(200))
   picture_url = db.Column(db.String(200)) 

   def __init__(self, id, tags, info, picture_url):
      self.id = id
      self.tags = tags
      self.info = info
      self.picture_url = picture_url


# 插入数据
def add_post_info(id, tags, info, picture_url):
   cur_info = PostInfo(id, tags, info, picture_url)
   db.session.add(cur_info)
   db.session.commit()

# 查询数据
def find_post_info(id=None, tags=None, info=None, picture_url=None):
   if id != None: # id精确查询
      return PostInfo.query.filter_by(id=id).all()
   if tags != None: # tags模糊查询 tags这里应该是list
      for tag in tags:
         tag = '%'+tag+'%'
      return PostInfo.query.filter(tags).all()
   else:
      return PostInfo.query.all()

# 删除数据
def find_post_info(id):
   cur_info = PostInfo.query.filter_by(id=id).first()
   db.session.delete(cur_info)
   db.session.commit()

# 修改数据
def change_post_info(id, tags=None, info=None, picture_url=None):
   cur_info = PostInfo.query.filter_by(id=id).first()
   if tags: # 标准的Str
      cur_info.tags = tags
   if info:
      cur_info.info = info
   if picture_url:
      cur_info.picture_url =picture_url
   
   db.session.commit()


