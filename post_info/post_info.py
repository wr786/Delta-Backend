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
   try:
      cur_info = PostInfo(id, tags, info, picture_url)
      db.session.add(cur_info)
      db.session.commit()
   except Exception as e:
      print('[Error]', e, 'in add info')
      return 

   print('Successfully add id=%d post info!' % id)


# 查询数据
def search_post_info(id=None, tags=None, info=None, picture_url=None):
   if id != None: # id精确查询
      try:
         return PostInfo.query.filter_by(id=id).all()
      except Exception as e:
         print('[Error]', e, 'in search info: Id search')
         return []
   elif tags != None: # tags模糊查询 tags这里应该是list
      for tag in tags:
         tag = '%'+tag+'%'
      try:
         return PostInfo.query.filter(tags).all()
      except Exception as e:
         print('[Error]', e, 'in search info: Tags search')
         return []
   else:
      try:
         return PostInfo.query.all()
      except Exception as e:
         print('[Error]', e, 'in search info: No-limit search')
         return []
   
   

# 删除数据
def delete_post_info(id):
   try:
      cur_info = PostInfo.query.filter_by(id=id).first()
   except Exception as e:
      print('[Error]', e, 'in delete info: Search info error')
   try:
      if cur_info == None:
         raise ValueError
      else:
         db.session.delete(cur_info)
         db.session.commit()
   except Exception as e:
      print('[Error]', e, 'in delete info: No such post info')
      return
   
   print('Successfully delete id=%d post info!' % id)

# 修改数据
def change_post_info(id, tags=None, info=None, picture_url=None):
   try:
      cur_info = PostInfo.query.filter_by(id=id).first()
   except Exception as e:
      print('[Error]', e, 'in change info: Search info Error')
      return
   try:
      if cur_info == None:
         raise ValueError
      else:
         if tags: # 标准的Str
            cur_info.tags = tags
         if info:
            cur_info.info = info
         if picture_url:
            cur_info.picture_url =picture_url
   except Exception as e:
      print('[Error]', e, 'in change info: No such post info')
      return
   db.session.commit()

   print('Successfully change id=%d post info!' % id)



