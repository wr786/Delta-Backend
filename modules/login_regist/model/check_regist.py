from ..lrconfig import conn
import re

cur = conn.cursor()

def add_user(username, email, password):
    try:
        conn.ping(reconnect=True)
        sql = "INSERT INTO user(username, email, password) VALUES ('%s','%s','%s')" %(username, email, password)
        cur.execute(sql)
        conn.commit()  # 对数据库内容有改变，需要commit()
        print('add_user success')
    except Exception as e:
        print('[Error]', e, 'in add_user')
        return

def check_pku(email):
    try:
        pattern= r'^[0-9a-zA-Z_-]+@stu.pku.edu.cn$'
        if re.match(pattern,email):
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