from flask import request, flash, url_for, redirect, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()

user_info = Blueprint('user_info', __name__, url_prefix='/user_info')

from ..utils import db


class UserInfo(db.Model):
   # 表名
   __tablename__ = 'user_info'
   # 字段
   id = db.Column('user_info_id', db.Integer, primary_key = True, autoincrement=True)
   name = db.Column(db.String(50))
   email = db.Column(db.String(50))
   info = db.Column(db.String(200))
   picture_url = db.Column(db.String(200))


# 插入数据
def add_user_info(name, email, info=None, picture_url=None):
   try:
      cur_info = UserInfo()
      cur_info.name = name
      cur_info.email = email
      cur_info.info = info
      cur_info.picture_url = picture_url
      db.session.add(cur_info)
      db.session.commit()
      print('Successfully add id=%d user info!' % cur_info.id)
      return True
   except Exception as e:
      print('[Error]', e, 'in add user info')
      return False



# 查询数据
def search_user_info(id=None,  name=None, email=None, info=None, picture_url=None):
   if id != None: # id精确查询
      try:
         return UserInfo.query.filter_by(id=id).all()
      except Exception as e:
         print('[Error]', e, 'in search user: Id search')
         return []
   else:
      try:
         return UserInfo.query.all()
      except Exception as e:
         print('[Error]', e, 'in search user: No-limit search')
         return []



# 删除数据
def delete_user_info(id):
   try:
      cur_info = UserInfo.query.filter_by(id=id).first()
   except Exception as e:
      print('[Error]', e, 'in delete user: Search user error')
      return False

   try:
      if cur_info == None:
         raise ValueError
      else:
         db.session.delete(cur_info)
         db.session.commit()
         print('Successfully delete id=%d user info!' % id)
         return True
   except Exception as e:
      print('[Error]', e, 'in delete user: No such user info')
      return False


# 修改数据
def change_user_info(id,  name=None, email=None, info=None, picture_url=None):
   try:
      cur_info = UserInfo.query.filter_by(id=id).first()
   except Exception as e:
      print('[Error]', e, 'in change user info: Search info Error')
      return False

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
         db.session.commit()
         print('Successfully change id=%d user info!' % id)
         return True
   except Exception as e:
      print('[Error]', e, 'in change user info: No such user info')
      return False

