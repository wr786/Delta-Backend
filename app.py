from argparse import Namespace
from functools import total_ordering
from mailbox import mboxMessage
from socket import socket
from sre_parse import ESCAPES
# from tkinter.font import names
from flask import Flask,session
from flask_socketio import SocketIO, emit
import config
from modules.post_info import post_info, db
from modules.post_info import add_post_info, search_post_info, delete_post_info, change_post_info
from modules.login_regist import login_blue
from modules.login_regist import regist_blue
from modules.login_regist import getsesinfo_blue
from modules.login_regist import logout_blue
from modules.user_info_function import add_user_info,search_user_info,delete_user_info,change_user_info

app = Flask(__name__)
app.secret_key=config.SECRET_KEY
# register blueprint
app.register_blueprint(post_info)
app.register_blueprint(login_blue)
app.register_blueprint(regist_blue)
app.register_blueprint(getsesinfo_blue)
app.register_blueprint(logout_blue)
# load config file
app.config.from_object(config)
db.init_app(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def test():
    return "Hello World!"

@socketio.on('Add Post Info', namespace='/post')
def new_post(message):
    print("test")
    flag = add_post_info(message['headline'], message['tags'], float(message['price_and_number']), message['info'], message['picture'])
    if flag:
        emit('post_info_response', {'result':'Post Success'})
    else:
        emit('post_info_response', {'result':'Post Failure'})



@socketio.on('Search Post Info', namespace='/list') # list应该也有
def show_post(message):
    limit = 15
    res, total_page = search_post_info(tags=message['tags'], limit=limit, offset=(message['cur_page']-1)*15)
    if total_page == 0:
            emit('post_info_response', {'result': 'Search Failure', 'lst': [], 'cur_page': message['cur_page'], 'total_page': total_page})
    else:
        total_page = total_page // limit + 1
        ret = []
        for per in res:
            ret.append({'post_id': per.id, 'title': per.headline, 'imgUrl': per.picture})
        emit('post_info_response', {'result': 'Search Success', 'lst': ret, 'cur_page': message['cur_page'], 'total_page': total_page})


@socketio.on('Search for Another Page', namespace='/list')
def change_page(message):
    limit = 15
    res, total_page = search_post_info(tags=message['tags'], limit=limit, offset=(message['cur_page']-1)*15)
    if total_page == 0:
            emit('post_info_response', {'result': 'Change Page Failure', 'lst': [], 'cur_page': message['cur_page'], 'total_page': total_page})
    else:
        total_page = total_page // limit + 1
        ret = []
        for per in res:
            ret.append({'post_id': per.id, 'title': per.headline, 'imgUrl': per.picture})
        emit('post_info_response', {'result': 'Change Page Success', 'lst': ret, 'cur_page': message['cur_page'], 'total_page': total_page})


@socketio.on('Open Post Info', namespace='/detail')
def open_post(message):
    res, _ = search_post_info(id=message['id'])
    if res == []:
        print('No such id!')
        emit('post_info_response', {'result':'Open Post Failure', 'id':None, 'headline':None, 'tags':None, 'price_and_number': None, 'info':None, 'picture':None})
    elif len(res) > 1:
        print('Same id for post info!')
        emit('post_info_response', {'result':'Open Post Failure', 'id':None, 'headline':None, 'tags':None, 'price_and_number': None, 'info':None, 'picture':None})
    else:
        res = res[0] # 肯定只有一个
        emit('post_info_response', {'result':'Open Post Success', 'id': res.id, 'headline': res.headline, 'tags': res.tags, 'price_and_number': res.price_and_number, 'info': res.info, 'picture': res.picture})


#新增用户信息
@socketio.on('Add User Info', namespace='/user_list')
def new_user(message):
    flag = add_user_info(message['id'], message['name'], message['email'], message['info'], message['picture_url'])
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
         emit('user_info_response',{'result': 'Search User Info Success', 'id': res.id, 'name': res.name, 'email': res.email, 'info': res.info, 'picture_url': res.picture_url})
    else:
         emit('user_info_response',{'result': 'Search User Info Failure', 'id': None, 'name': None, 'email': None, 'info': None, 'picture_url': None})

#修改用户信息
@socketio.on('Change User Info', namespace='/user_list')
def change_user_info(message):
    flag = change_user_info(id=message['id'],name=message["name"],email=message["email"],info=message["info"],picture_url=message["picture_url"])
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



if __name__ == '__main__':
    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()
    socketio.run(app, port=5001, debug=True)
