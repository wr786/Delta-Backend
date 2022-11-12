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
   id = db.Column('post_info_id', db.Integer, primary_key = True, autoincrement = True)
   headline = db.Column(db.String(100))
   tags = db.Column(db.String(100))
   price_and_number = db.Column(db.Float)
   info = db.Column(db.String(200))
   picture = db.Column(db.String(5000)) 

# 插入数据
def add_post_info(headline, tags, price_and_number, info, picture):
   try:
      cur_info = PostInfo()
      cur_info.headline = headline
      cur_info.tags = tags
      cur_info.price_and_number = price_and_number
      cur_info.info = info
      cur_info.picture = picture
      db.session.add(cur_info)
      db.session.commit()
   except Exception as e:
      db.session.rollback() # 回滚
      print('[Error]', e, 'in add info')
      return 

   print('Successfully add id=%d post info!' % cur_info.id)


# 查询数据
def search_post_info(id=None, tags=None, limit=15, offset=0):
   if id != None: # id精确查询
      try:
         return PostInfo.query.filter_by(id=id).limit(limit).offset(offset).all(), PostInfo.query.filter_by(id=id).count()
      except Exception as e:
         print('[Error]', e, 'in search info: Id search')
         return [], 0
   elif tags != None:
      try:
         return PostInfo.query.filter(PostInfo.tags.like(tags+'%')).limit(limit).offset(offset).all(), PostInfo.query.filter(PostInfo.tags.like(tags+'%')).count()
      except Exception as e:
         print('[Error]', e, 'in search info: Tags search')
         return [], 0
   else:
      try:
         return PostInfo.query.limit(limit).offset(offset).all(), PostInfo.query.count()
      except Exception as e:
         print('[Error]', e, 'in search info: No-limit search')
         return [], 0
   
   

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
      if e != ValueError:
         db.session.rollback() # 回滚
      print('[Error]', e, 'in delete info: No such post info')
      return
   
   print('Successfully delete id=%d post info!' % id)

# 修改数据
def change_post_info(id, tags=None, price_and_number=None, info=None, picture=None):
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
         if price_and_number:
            cur_info.price_and_number = price_and_number
         if info:
            cur_info.info = info
         if picture:
            cur_info.picture =picture
         db.session.commit()
   except Exception as e:
      if e != ValueError:
            db.session.rollback() # 回滚
      print('[Error]', e, 'in change info: No such post info')
      return

   print('Successfully change id=%d post info!' % id)



