HOST = 'xxxx' # localhost
PORT = 'xxxx'
DATABASE = 'xxxx'
USERNAME = 'xxxx'
PASSWORD = 'xxxxx'

DB_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8mb4".format(username=USERNAME,password=PASSWORD, host=HOST,port=PORT, db=DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

SECRET_KEY = 'XXXXXXXXXXXX'