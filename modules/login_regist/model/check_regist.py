from ..connect import conn
import re
import hashlib
from ...user_info_function import add_user_info
from ..db import *

cur = conn.cursor()

def add_user(username, email, password):
    try:
        conn.ping(reconnect=True)
        encrypted=encrypt(password)
        cur_account = AccountInfo()
        cur_account.username = username
        cur_account.password = password
        cur_account.email = email
        # 注册成功时自动生成对应用户
        flag = add_user_info(cur_account.id, username, email) # password 从注册表找暂时
        if flag:
            db.session.add(cur_account)
            db.session.commit() # 对数据库内容有改变，需要commit()
            print('[Info] register and add_user success')
            return True
        else:
            print('[Error] in add_user')
            raise NotImplementedError
    except Exception as e:
        print('[Error]', e, 'in register and add_user')
        return False

def check_pku(email):
    try:
        pattern1= r'^[0-9a-zA-Z_-]+@stu.pku.edu.cn$'
        pattern2= r'^[0-9a-zA-Z_-]+@pku.edu.cn$'
        if re.match(pattern1,email) or re.match(pattern2,email):
            return True
        else:
            return False
    except Exception as e:
        print('[Error]', e, 'in check_pku')
        return False


def regist_null(username,email,password):
    try:
        if(username=='' or email==''or password==''):
            return True
        else:
            return False
    except Exception as e:
        print('[Error]', e, 'in regist_null')
        return False


def encrypt(pwd): 
    sha = hashlib.sha256(pwd.encode('utf-8'))
    encrypted = sha.hexdigest()
    return encrypted       