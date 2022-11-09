from argparse import Namespace
from mailbox import mboxMessage
from socket import socket
# from tkinter.font import names
from flask import Flask
from flask_sockets import Sockets
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
sockets = Sockets(app)


# test
@sockets.route('/echo')
def echo_socket(ws):
    while not ws.closed:
        message = ws.receive()
        print(message)
        ws.send(message)


@sockets.route('/post')
def new_post(ws):
    while not ws.closed:
        message = ws.receive()
        flag = add_post_info(message['headline'], message['tags'], message['info'], message['picture'])
        if flag:
            ws.send({'result':'Post Success'})
        else:
            ws.send({'result':'Post Failure'})

@app.route('/')
def hello():
    return 'Hello World!'



# @sockets.route('/show') # list应该也有
# def show_post(message):
#     res = search_post_info(tags=message['tags'])
#     ret = []
#     flag = True # TODOLIST: 判断是否还有下一个page
#     for per in res:
#         ret.append((per.id, per.picture))
#         if len(ret) == 15:
#             break
#     emit('post_info_response', {'result': 'Search Success', 'lst': ret, 'page_id': 1, 'first_page': True, 'last_page': flag})


# @sockets.route('/open')
# def open_post(message):
#     res = search_post_info(id=message['id'])
#     if res == []:
#         print('No such id!')
#         emit('post_info_response', {'result':'Open Post Failure', 'id':None, 'headline':None, 'tags':None, 'info':None, 'picture':None})
#     elif len(res) > 1:
#         print('Same id for post info!')
#         emit('post_info_response', {'result':'Open Post Failure', 'id':None, 'headline':None, 'tags':None, 'info':None, 'picture':None})
#     else:
#         res = res[0] # 肯定只有一个
#         emit('post_info_response', {'result':'Open Post Success', 'id': res.id, 'headline': res.headline, 'tags': res.tags, 'info': res.info, 'picture': res.picture})


# @sockets.route('/turn')
# def turn_page(message):
#     ret = []
#     emit('post_info_response', {'result': 'Change Page Success', 'lst': ret})

if __name__ == '__main__':
    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5001), app, handler_class=WebSocketHandler)
    server.serve_forever()
