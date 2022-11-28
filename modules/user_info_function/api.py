from flask import Blueprint,request,render_template,redirect,session
from .user_info_function import *
import json

user_blue=Blueprint('user',__name__,url_prefix='/user')

#新增用户信息
@user_blue.route('/add',methods=['POST'])
def new_user():
    message = json.loads(request.data)
    flag = add_user_info(
        message['id'], 
        message['name'], 
        message['email'], 
        message['info'], 
        message['picture']
    )
    if flag:
        return {'code': 0}
    else:
        return {'code': -1}


#查询用户信息
@user_blue.route('/', methods=['GET'])
def show_user_info():
    uid = int(request.args.get('uid'))
    res = search_user_info(id=uid)
    if res != None:
        return {'code': 0, 'id': res.id, 'name': res.name, 'email': res.email, 'info': res.info, 'picture': res.picture}
    else:
        return {'code': -1, "msg": f"User(uid={uid}) not found!"}


#修改用户信息
@user_blue.route('/edit',methods=['POST'])
def change_user_info():
    message = json.loads(request.data)
    flag = change_user_info(
        id=message['id'],
        name=message["new_name"],
        email=message["new_email"],
        info=message["new_info"],
        picture=message["new_picture"]
    )
    if flag:
        return {'code': 0}
    else:
        return {'code': -1}


#删除用户信息
@user_blue.route('/delete',methods=['POST'])
def delete_user():
    message = json.loads(request.data)
    flag = delete_user_info(id=message["id"])
    if flag:
        return {'code': 0}
    else:
        return {'code': -1}

