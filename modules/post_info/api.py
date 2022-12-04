from flask import Blueprint,request,render_template,redirect,session
from .post_info import *
from .comment import *
from ..user_info_function import search_user_info
import json
from ..user_info_function import search_user_info

post_blue=Blueprint('post',__name__,url_prefix='/post')

#新增post
@post_blue.route('/add',methods=['POST'])
def new_post():
    message = json.loads(request.data)
    flag = add_post_info(
        int(message['user_id']), 
        message['headline'], 
        message['tags'][-1], 
        float(message['price_and_number']) if message['price_and_number'] != '' else 0, 
        message['info'], 
        message['picture']
    )
    if flag:
        return {'code': 0}
    else:
        return {'code': -1}


#根据tags搜索post
@post_blue.route('/list',methods=['GET'])
def show_post():
    message = {}
    message['tags'] = request.args.get('tags')
    message['cur_page'] = int(request.args.get('cur_page'))
    print('[Info] show_post: message=', message)
    limit = 15
    res, total_post = search_post_info(
        tags=message['tags'], 
        limit=limit, 
        offset=(message['cur_page']-1)*15
    )
    if total_post == 0:
        return {'code': -1, 'lst': [], 'cur_page': message['cur_page'], 'total_post': total_post}
    else:
        ret = []
        for per in res:
            ret.append({'post_id': per.id, 'title': per.headline, 'imgUrl': per.picture, 'createTime': per.createTime.strftime( '%Y-%m-%d %H:%M:%S' )})
        return {'code': 0, 'lst': ret, 'cur_page': message['cur_page'], 'total_post': total_post}


#搜索Post Info（by key words）
@post_blue.route('/key-list',methods=['GET'])
def search_by_key_words():
    message = {}
    message['key_words'] = request.args.get('key_words')
    message['cur_page'] = int(request.args.get('cur_page'))
    message['tags'] = request.args.get('tags')
    print("[Info]", 'search_by_key_words: ', message)
    limit = 15
    key_words = message['key_words'].split() # 根据空白符分隔
    res, total_post = search_post_info(
        tags=message['tags'],
        key_words=key_words,
        limit=limit, 
        offset=(message['cur_page']-1)*15
    )
    if total_post == 0:
        return {'code': -1, 'lst': [], 'cur_page': message['cur_page'], 'total_post': total_post}
    else:
        ret = []
        for per in res:
            ret.append({'post_id': per.id, 'title': per.headline, 'imgUrl': per.picture, 'createTime': per.createTime.strftime( '%Y-%m-%d %H:%M:%S' )})
        return {'code': 0, 'lst': ret, 'cur_page': message['cur_page'], 'total_post': total_post}


#打开一个post
@post_blue.route('/detail',methods=['GET'])
def open_post():
    pid = request.args.get('id')
    res, _ = search_post_info(id=pid)
    if res == []:
        print(f'[Error] No such id!: {pid}')
        return {'code': -1, 'id':None, 'headline':None, 'tags':None, 'price_and_number': None, 'info':None, 'picture':None, 'createTIme': None, 'user_id': None, 'user_name': None, 'user_picture': None}
    elif len(res) > 1:
        print(f'[Error] Same id for post info!: {pid}')
        return {'code': -1, 'id':None, 'headline':None, 'tags':None, 'price_and_number': None, 'info':None, 'picture':None, 'createTime': None, 'user_id': None, 'user_name': None, 'user_picture': None}
    else:
        res = res[0] # 肯定只有一个
        # 还要找到user的id、姓名和头像
        user = search_user_info(res.user_id)
        if user == None:
            print(f'[Error] None user post this! pid={pid}')
            return {'code': -1, 'id':None, 'headline':None, 'tags':None, 'price_and_number': None, 'info':None, 'picture':None, 'createTime': None, 'user_id': None, 'user_name': None, 'user_picture': None}
        return {'code': 0, 'id': res.id, 'headline': res.headline, 'tags': res.tags, 'price_and_number': res.price_and_number, 'info': res.info, 'picture': res.picture, 'createTime': res.createTime.strftime( '%Y-%m-%d %H:%M:%S' ), 'user_id': user.id, 'user_name': user.name, 'user_picture': user.picture}


#修改post
@post_blue.route('/change',methods=['POST'])
def change_post():
    message = json.loads(request.data)
    flag = change_post_info(
        id=message['id'], 
        headline=message['new_headline'], 
        tags=message["new_tags"], 
        price_and_number=message["new_price_and_number"], 
        info=message["new_info"], 
        picture=message["new_picture"]
    )
    if flag:
        return {'code': 0}
    else:
        return {'code': -1}


#删除Post Info
@post_blue.route('/delete',methods=['POST'])
def delete_post():
    message = json.loads(request.data)
    flag = delete_post_info(id=message['id'])
    if flag:
      return {'code': 0}
    else:
      return {'code': -1}


#查询用户的所有发布信息
@post_blue.route('/user_post',methods=['POST'])
def search_user_post():
    message = json.loads(request.data)
    limit = 15
    res, total_post = search_post_info(
        user_id=message['user_id'], 
        limit=limit, 
        offset=(message['cur_page']-1)*15
    )
    if total_post == 0:
        return {'code': -1, 'lst': [], 'cur_page': message['cur_page'], 'total_post': total_post, 'date': None, 'time': None, 'tags': None}
    else:
        ret = []
        for per in res:
            ret.append({'post_id': per.id, 'title': per.headline, 'imgUrl': per.picture, 'date': per.createTime.strftime( '%Y-%m-%d' ), 'time': per.createTime.strftime( '%H:%M:%S' ), 'tags': get_tag_name(per.tags[:2])})
        return {'code': 0, 'lst': ret, 'cur_page': message['cur_page'], 'total_post': total_post, 'date': None, 'time': None, 'tags': None}
        

@post_blue.route('/comment/add',methods=['POST'])
def _add_comment():
    data = json.loads(request.data)
    code = add_comment(int(data['pid']), int(data['uid']), data['content'])
    return {'code': code}


@post_blue.route('/comment/get', methods=['GET'])
def _get_comment():
    via = request.args.get('via')
    if via == 'post':
        code, comments = get_comments_by_post(int(request.args.get('pid')))
        ret = []
        for comment in comments:
            user = search_user_info(comment.sender)
            ret.append({
                'username': user.name,
                # 'userAvatar':  user.pictureUrl, # 等有头像功能再说
                'content': comment.content,
                'time': comment.createTime.strftime( '%Y-%m-%d %H:%M:%S' )  
            })
        return {"code": code, "comments": ret}
    elif via == 'user':
        code, comments = get_comments_by_user(int(request.args.get('uid')))
        ret = []
        for comment in comments:
            user = search_user_info(comment.sender)
            ret.append({
                'username': user.name,
                # 'userAvatar':  user.pictureUrl, # 等有头像功能再说
                'content': comment.content,
                'time': comment.createTime.strftime( '%Y-%m-%d %H:%M:%S' ) 
            })
        return {"code": code, "comments": ret}
    else:
        return {"code": -1, "message": "Invalid via param!"}
