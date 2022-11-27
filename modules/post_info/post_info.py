from flask import request, flash, url_for, redirect, render_template, Blueprint
import pymysql
pymysql.install_as_MySQLdb()
from .db import *

post_info = Blueprint('post_info', __name__, url_prefix='/post_info')

# 插入数据
def add_post_info(user_id, headline, tags, price_and_number, info, picture):
   try:
      cur_info = PostInfo()
      cur_info.user_id = user_id
      cur_info.headline = headline
      cur_info.tags = tags
      cur_info.price_and_number = price_and_number
      cur_info.info = info
      cur_info.picture = picture
      db.session.add(cur_info)
      db.session.commit()
      print('Successfully add id=%d post info!' % cur_info.id)
      return True

   except Exception as e:
      db.session.rollback() # 回滚
      print('[Error]', e, 'in add info')
      return False


# 查询数据
# 返回两个值：一个是查询结果 一个是这个tag所有的post_info数量
def search_post_info(id=None, tags=None,  key_words=None, user_id=None, limit=15, offset=0):
   if id != None: # id精确查询
      try:
         return PostInfo.query.filter_by(id=id).order_by(PostInfo.createTime.desc()).limit(limit).offset(offset).all(), PostInfo.query.filter_by(id=id).count()
      except Exception as e:
         print('[Error]', e, 'in search info: Id search')
         return [], 0
   elif tags != None: # tags查询
      try:
         return PostInfo.query.filter(PostInfo.tags.like(tags+'%')).order_by(PostInfo.createTime.desc()).limit(limit).offset(offset).all(), PostInfo.query.filter(PostInfo.tags.like(tags+'%')).count()
      except Exception as e:
         print('[Error]', e, 'in search info: Tags search')
         return [], 0
   elif key_words: # key words查询 是一个list
      try: 
         re_str = '%'
         for word in key_words:
            re_str = re_str + word + '%'
         re_str += '%'
         return PostInfo.query.filter(PostInfo.headline.like(re_str)).order_by(PostInfo.createTime.desc()).limit(limit).offset(offset).all(), PostInfo.query.filter(PostInfo.headline.like(re_str)).count()
      except Exception as e:
         print('[Error]', e, 'in search info: Key Words search')
         return [], 0
   elif user_id: # 查询用户发布的post
      try: 
         return PostInfo.query.filter_by(user_id=user_id).order_by(PostInfo.createTime.desc()).limit(limit).offset(offset).all(), PostInfo.query.filter_by(user_id=user_id).count()
      except Exception as e:
         print('[Error]', e, 'in search info: User_id search')
         return [], 0
   else:
      try:
         return PostInfo.query.order_by(PostInfo.createTime.desc()).limit(limit).offset(offset).all(), PostInfo.query.count()
      except Exception as e:
         print('[Error]', e, 'in search info: No-limit search')
         return [], 0
   
   
# 删除数据
def delete_post_info(id):
   try:
      cur_info = PostInfo.query.filter_by(id=id).first()
   except Exception as e:
      print('[Error]', e, 'in delete info: Search info error')
      return False

   try:
      if cur_info == None:
         raise ValueError
      else:
         db.session.delete(cur_info)
         db.session.commit()
         print('Successfully delete id=%d post info!' % id)
         return True
   except Exception as e:
      if e != ValueError:
         db.session.rollback() # 回滚
      print('[Error]', e, 'in delete info: No such post info')
      return False
   


# 修改数据
def change_post_info(id, headline=None, tags=None, price_and_number=None, info=None, picture=None): # cannot change user_id
   try:
      cur_info = PostInfo.query.filter_by(id=id).first()
   except Exception as e:
      print('[Error]', e, 'in change info: Search info Error')
      return False

   try:
      if cur_info == None:
         raise ValueError
      else:
         if headline:
            cur_info.headline = headline
         if tags: # 标准的Str
            cur_info.tags = tags
         if price_and_number:
            cur_info.price_and_number = price_and_number
         if info:
            cur_info.info = info
         if picture:
            cur_info.picture =picture
         db.session.commit()
         print('Successfully change id=%d post info!' % id)
         return True
   except Exception as e:
      if e != ValueError:
            db.session.rollback() # 回滚
      print('[Error]', e, 'in change info: No such post info')
      return False




