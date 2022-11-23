#数据库连接配置
import pymysql
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from config import HOST,PORT,PASSWORD,DATABASE,USERNAME

conn = pymysql.connect(
        host=HOST,
        port=PORT,
        user=USERNAME,
        password=PASSWORD,
        database=DATABASE
    )
