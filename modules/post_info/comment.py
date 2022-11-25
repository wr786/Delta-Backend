from .db import *
from ..user_info_function import UserInfo
import datetime

def add_comment(pid, uid, content):
    try:
        comment = Comment()
        comment.pid = pid
        comment.sender = uid
        comment.content = content
        db.session.add(comment)
        db.session.commit()
        return 0
    except Exception as e:
        db.session.rollback()
        print(f'[Error] Add comment failure: uid={uid}, content={content}; {e}')
        return -1

def get_comments_by_user(uid):
    try:
        # user = UserInfo.query.filter(id=uid).one()
        # if user is None:
        #     raise KeyError('User not exist!')
        comments = Comment.query.filter_by(sender=uid).order_by(Comment.createTime.asc()).all()
        return 0, comments
    except Exception as e:
        print(f'[Error] Get comments failure: uid={uid}; {e}')
        return -1, 

def get_comments_by_post(pid):
    try:
        # post = PostInfo.query.filter(id=pid).one()
        # if post is None:
        #     raise KeyError('Post not exist!')
        comments = Comment.query.filter_by(pid=pid).order_by(Comment.createTime.asc()).all()
        return 0, comments
    except Exception as e:
        errmsg = f'[Error] Get comments failure: pid={pid}; {e}'
        print(errmsg)
        return -1, errmsg