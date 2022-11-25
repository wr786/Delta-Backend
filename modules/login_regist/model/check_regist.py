from ..connect import conn
import re
import hashlib
from ...user_info_function import add_user_info

cur = conn.cursor()

def add_user(username, email, password):
    try:
        conn.ping(reconnect=True)
        encrypted=encrypt(password)
        sql = "INSERT INTO user(username, email, password) VALUES ('%s','%s','%s')" %(username, email, encrypted)
        cur.execute(sql)
        # 注册成功时自动生成对应用户
        flag = add_user_info(username, email) # password 从注册表找暂时
        if flag:
            print('add_user success')
            conn.commit()  # 对数据库内容有改变，需要commit()
            print('register and add_user success')
        else:
            print('add_user error')
            raise NotImplementedError
    except Exception as e:
        print('[Error]', e, 'in register and add_user')
        return

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
        return


def regist_null(username,email,password):
    try:
        if(username=='' or email==''or password==''):
            return True
        else:
            return False
    except Exception as e:
        print('[Error]', e, 'in regist_null')
        return

def encrypt(pwd): 
    sha = hashlib.sha256(pwd.encode('utf-8'))
    encrypted = sha.hexdigest()
    return encrypted       