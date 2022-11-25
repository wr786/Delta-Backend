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
from modules.user_info_function import add_user_info, search_user_info, delete_user_info, change_user_info
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


################ User Info WebSocket Begin ################
#新增用户信息
@socketio.on('Add User Info', namespace='/user_list')
def new_user(message):
    flag = add_user_info(message['id'], message['name'], message['email'], message['info'], message['picture'])
    if flag:
        emit('user_info_response', {'result':'Add User Info Success'})
    else:
        emit('user_info_response', {'result':'Add User Info Failure'})


#查询用户信息
@socketio.on('Search User Info', namespace='/user_list')
def show_user_info(message):
    res = search_user_info(id=message['id'])
    if len(res)==1:    #精确ID查询应当只有一个对应用户信息
         res = res[0]
         emit('user_info_response',{'result': 'Search User Info Success', 'id': res.id, 'name': res.name, 'email': res.email, 'info': res.info, 'picture': res.picture})
    else:
         emit('user_info_response',{'result': 'Search User Info Failure', 'id': None, 'name': None, 'email': None, 'info': None, 'picture': None})


#修改用户信息
@socketio.on('Change User Info', namespace='/user_list')
def change_user_info(message):
    flag = change_user_info(id=message['id'],name=message["new_name"],email=message["new_email"],info=message["new_info"],picture=message["new_picture"])
    if flag:
        emit('user_info_response', {'result':'Change User Info Success'})
    else:
        emit('user_info_response', {'result':'Change User Info Failure'})


#删除用户信息
@socketio.on('Delete User Info', namespace='/user_list')
def delete_user(message):
    flag = delete_user_info(id=message["id"])
    if flag:
      emit('user_info_response', {'result': 'Delete User Info Success'})
    else:
      emit('user_info_response', {'result': 'Delete User Info Failure'})
################ User Info WebSocket End ################




if __name__ == '__main__':
    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()
    app.run(port=5001, debug=True)
