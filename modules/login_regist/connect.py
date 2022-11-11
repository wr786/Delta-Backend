#数据库连接配置
import pymysql
from ...config_demo import HOST,PORT,PASSWORD,DATABASE,USERNAME

conn = pymysql.connect(
        host=HOST,
        port=PORT,
        user=USERNAME,
        password=PASSWORD,
        database=DATABASE
    )
