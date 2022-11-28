from flask import request, flash, url_for, redirect, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy
import pymysql
from .db import *
pymysql.install_as_MySQLdb()

user_info = Blueprint('user_info', __name__, url_prefix='/user_info')


# 插入数据
def add_user_info(id, name, email, info='testInfo', picture='testPicture'):
   try:
      cur_info = UserInfo()
      cur_info.id=id
      cur_info.name = name
      cur_info.email = email
      cur_info.info = info
      cur_info.picture = picture
      db.session.add(cur_info)
      db.session.commit()
      print('Successfully add id=%d user info!' % cur_info.id)
      return True
   except Exception as e:
      print('[Error]', e, 'in add user info')
      return False



# 查询数据
def search_user_info(id=None,  name=None, email=None, info=None, picture=None):
   if id != None: # id精确查询
      try:
         return UserInfo.query.filter_by(id=id).first()
      except Exception as e:
         db.session.rollback() # 回滚
         print('[Error]', e, 'in search user: Id search')
         return None
   else:
      try:
         return UserInfo.query.all()
      except Exception as e:
         db.session.rollback() # 回滚
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
      if e != ValueError:
         db.session.rollback() # 回滚
      print('[Error]', e, 'in delete user: No such user info')
      return False


# 修改数据
def change_user_info(id,  name=None, email=None, info=None, picture=None):
   try:
      cur_info = UserInfo.query.filter_by(id=id).first()
   except Exception as e:
      print('[Error]', e, 'in change user info: Search user info Error')
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
         if picture:
            cur_info.picture =picture
         db.session.commit()
         print('Successfully change id=%d user info!' % id)
         return True
   except Exception as e:
      if e != ValueError:
            db.session.rollback() # 回滚
      print('[Error]', e, 'in change user info: No such user info')
      return False
   

# Follow某人
def star_user(fan_id, star_id):
   try:
      if StarsAndFans.query.filter_by(fan_id=fan_id, star_id=star_id).first(): # 已经存在follow了
         print('Already followed')
         raise ValueError
      else:
         cur_follow = StarsAndFans()
         cur_follow.fan_id = fan_id
         cur_follow.star_id = star_id
         print('Successfully add id=%d follow info!' % cur_follow.id)
         return True
   except Exception as e:
      print('[Error]', e, 'in add star user')
      return False


# 不再Follow某人
def not_star_user(fan_id, star_id):
   try:
      cur_follow = StarsAndFans.query.filter_by(fan_id=fan_id, star_id=star_id).first()
   except Exception as e:
      print('[Error]', e, ' in search follow')
      return False
      
   try:
      if cur_follow == None:
         raise ValueError
      else:
         db.session.delete(cur_follow)
         db.session.commit()
         print('Successfully delete id=%d follow!' % id)
         return True
   except Exception as e:
      if e != ValueError:
         db.session.rollback() # 回滚
      print('[Error]', e, 'in delete follow: No such follow')
      return False


# 查询Follow的users
def search_stars(id):
   try:
      assert(id != None)
      return StarsAndFans.query.filter_by(fan_id=id).all(), StarsAndFans.query.filter_by(fan_id=id).count()
   except Exception as e:
      db.session.rollback() # 回滚
      print('[Error]', e, 'in search stars: Id search')
      return None, 0


# 查询粉丝
def search_fans(id):
   try:
      assert(id != None)
      return StarsAndFans.query.filter_by(star_id=id).all(), StarsAndFans.query.filter_by(star_id=id).count()
   except Exception as e:
      db.session.rollback() # 回滚
      print('[Error]', e, 'in search fans: Id search')
      return None, 0

