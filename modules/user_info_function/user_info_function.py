from flask import request, flash, url_for, redirect, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()

user_info = Blueprint('user_info', __name__, url_prefix='/user_info')

db = SQLAlchemy()

class UserInfo(db.Model):
   # 表名
   __tablename__ = 'user_info'
   # 字段
   id = db.Column('user_info_id', db.Integer, primary_key = True)
   name = db.Column(db.String(50))
   email = db.Column(db.String(50))
   info = db.Column(db.String(200))
   picture_url = db.Column(db.String(200))

   def __init__(self, id, name, email,info, picture_url):
      self.id = id
      self.name = name
      self.email = email
      self.info = info
      self.picture_url = picture_url


# 插入数据
def add_post_info( id, name, email,info, picture_url):
   try:
      cur_info = UserInfo( id, name, email,info, picture_url)
      db.session.add(cur_info)
      db.session.commit()
   except Exception as e:
      print('[Error]', e, 'in add info')
      return 

   print('Successfully add id=%d post info!' % id)


# 查询数据
def search_post_info(id=None,  name=None, email=None, info=None, picture_url=None):
   if id != None: # id精确查询
      try:
         return UserInfo.query.filter_by(id=id).all()
      except Exception as e:
         print('[Error]', e, 'in search info: Id search')
         return []
   else:
      try:
         return UserInfo.query.all()
      except Exception as e:
         print('[Error]', e, 'in search info: No-limit search')
         return []



# 删除数据
def delete_post_info(id):
   try:
      cur_info = UserInfo.query.filter_by(id=id).first()
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
def change_post_info(id,  name=None, email=None, info=None, picture_url=None):
   try:
      cur_info = UserInfo.query.filter_by(id=id).first()
   except Exception as e:
      print('[Error]', e, 'in change info: Search info Error')
      return
   try:
      if cur_info == None:
         raise ValueError
      else:
         if name: # 标准的Str
            cur_info.name = name
         if email:
            cur_info.email = email
         if info:
            cur_info.info = info
         if picture_url:
            cur_info.picture_url =picture_url
   except Exception as e:
      print('[Error]', e, 'in change info: No such post info')
      return
   db.session.commit()

   print('Successfully change id=%d post info!' % id)