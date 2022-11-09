from argparse import Namespace
from mailbox import mboxMessage
from socket import socket
# from tkinter.font import names
from flask import Flask
from flask_socketio import SocketIO, emit
from views import test
import config
from modules.post_info import post_info, db
from modules.post_info import add_post_info, search_post_info, delete_post_info, change_post_info


app = Flask(__name__)
# register blueprint
app.register_blueprint(test.test)
app.register_blueprint(post_info)
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
    total_page //= limit
    ret = []
    for per in res:
        ret.append((per.id, per.picture))
    emit('post_info_response', {'result': 'Search Success', 'lst': ret, 'cur_page': message['cur_page'], 'total_page': total_page})


@socketio.on('Open Post Info', namespace='/detail')
def open_post(message):
    res = search_post_info(id=message['id'])
    if res == []:
        print('No such id!')
        emit('post_info_response', {'result':'Open Post Failure', 'id':None, 'headline':None, 'tags':None, 'info':None, 'picture':None})
    elif len(res) > 1:
        print('Same id for post info!')
        emit('post_info_response', {'result':'Open Post Failure', 'id':None, 'headline':None, 'tags':None, 'info':None, 'picture':None})
    else:
        res = res[0] # 肯定只有一个
        emit('post_info_response', {'result':'Open Post Success', 'id': res.id, 'headline': res.headline, 'tags': res.tags, 'info': res.info, 'picture': res.picture})


@socketio.on('Search for Another Page', namespace='/list')
def change_page(message):
    ret = []
    emit('post_info_response', {'result': 'Change Page Success', 'lst': ret})

if __name__ == '__main__':
    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()
    socketio.run(app, port=5001, debug=True)