HOST = 'xxxx' # localhost
PORT = 3306
DATABASE = 'xxxx'
USERNAME = 'xxxx'
PASSWORD = 'xxxxx'

DB_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?charset=utf8mb4"

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

SECRET_KEY = 'XXXXXXXXXXXX'

MAIL_SERVER='xxxxxxxxxx'
MAIL_PORT = 465
MAIL_USERNAME = 'xxxxxxxxxxxx'
MAIL_PASSWORD = 'xxxxxxxxxxxx'
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_DEFAULT_SENDER='xxxxxxxxxx'


# Redis数据库配置
CACHE_TYPE = 'redis'
CACHE_REDIS_HOST = 'xxxxxxxxxxx' # localhost
CACHE_REDIS_PORT = 6379
CACHE_REDIS_DB = ''
CACHE_REDIS_PASSWORD = ''