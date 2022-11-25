from argparse import Namespace
from functools import total_ordering
from mailbox import mboxMessage
from socket import socket
from sre_parse import ESCAPES
# from tkinter.font import names
from flask import Flask,session
from datetime import timedelta

from modules.utils import config, db
from modules.post_info import post_blue
from modules.login_regist import AccountInfo
from modules.login_regist import login_blue, regist_blue, getsesinfo_blue, logout_blue
from modules.user_info_function import user_blue
from modules.login_regist import sendemail_blue
from modules.login_regist import mail,cache

app = Flask(__name__)
app.permanent_session_lifetime = timedelta(hours=1)  #session expired in 1 h
# register blueprint
app.register_blueprint(post_blue)
app.register_blueprint(user_blue)
app.register_blueprint(login_blue)
app.register_blueprint(regist_blue)
app.register_blueprint(getsesinfo_blue)
app.register_blueprint(logout_blue)
app.register_blueprint(sendemail_blue)
# load config file
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)
cache.init_app(app)

if __name__ == '__main__':
    with app.app_context():
    #     db.drop_all()
        db.create_all()
    app.run(port=5001, debug=True)
