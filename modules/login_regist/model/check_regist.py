from lrconfig import conn
import re

cur = conn.cursor()

def add_user(username, email, password):
    # sql commands
    sql = "INSERT INTO user(username,email, password) VALUES ('%s','%s','%s')" %(username, email, password)
    # execute(sql)
    cur.execute(sql)
    # commit
    conn.commit()  # 对数据库内容有改变，需要commit()
    conn.close()

def check_pku(email):
    pattern= r'[a-z1-9][a-z1-9_]{2,14}[a-z0-9]@stu\.pku\.edu\.com$'
    if re.match(email,pattern):
        return True
    else:
        return False
