from flask import Blueprint,request,render_template,redirect,session
from .post_info import *
from .comment import *
from ..user_info_function import search_user_info
import json

post_blue=Blueprint('post',__name__,url_prefix='/post')

@post_blue.route('/add',methods=['POST'])
def new_post():
    message = json.loads(request.data)
    flag = add_post_info(
        0, 
        message['headline'], 
        message['tags'], 
        float(message['price_and_number']) if message['price_and_number'] != '' else 0, 
        message['info'], 
        message['picture']
    )
    if flag:
        return {'result':'Post Success'}
    else:
        return {'result':'Post Failure'}


@post_blue.route('/list',methods=['GET'])
def show_post():
    message = {}
    message['tags'] = request.args.get('tags')
    message['cur_page'] = int(request.args.get('cur_page'))
    limit = 15
    res, total_post = search_post_info(tags=message['tags'], limit=limit, offset=(message['cur_page']-1)*15)
    if total_post == 0:
        return {'result': 'Search Failure', 'lst': [], 'cur_page': message['cur_page'], 'total_post': total_post}
    else:
        ret = []
        for per in res:
            ret.append({'post_id': per.id, 'title': per.headline, 'imgUrl': per.picture})
        return {'result': 'Search Success', 'lst': ret, 'cur_page': message['cur_page'], 'total_post': total_post}


#搜索Post Info（by key words）
@post_blue.route('/key-list',methods=['GET'])
def search_by_key_words():
    message = {}
    message['key_words'] = request.args.get('key_words')
    message['cur_page'] = request.args.get('cur_page')
    # FOR DEBUG：message['cur_page'] = 1
    print('search_by_key_words: ', message)
    limit = 15
    key_words = message['key_words'].split() # 根据空白符分隔
    res, total_post = search_post_info(key_words=key_words, limit=limit, offset=(message['cur_page']-1)*15)
    if total_post == 0:
        return {'result': 'Search Failure', 'lst': [], 'cur_page': message['cur_page'], 'total_post': total_post}
    else:
        ret = []
        for per in res:
            ret.append({'post_id': per.id, 'title': per.headline, 'imgUrl': per.picture})
        return {'result': 'Search Success', 'lst': ret, 'cur_page': message['cur_page'], 'total_post': total_post}


@post_blue.route('/detail',methods=['GET'])
def open_post():
    pid = request.args.get('id')
    res, _ = search_post_info(id=pid)
    if res == []:
        print(f'No such id!: {pid}')
        return {'result':'Open Post Failure', 'id':None, 'headline':None, 'tags':None, 'price_and_number': None, 'info':None, 'picture':None}
    elif len(res) > 1:
        print(f'Same id for post info!: {pid}')
        return {'result':'Open Post Failure', 'id':None, 'headline':None, 'tags':None, 'price_and_number': None, 'info':None, 'picture':None}
    else:
        res = res[0] # 肯定只有一个
        return {'result':'Open Post Success', 'id': res.id, 'headline': res.headline, 'tags': res.tags, 'price_and_number': res.price_and_number, 'info': res.info, 'picture': res.picture}


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
        return {'result':'Change Post Info Success'}
    else:
        return {'result':'Change Post Info Failure'}


#删除Post Info
@post_blue.route('/delete',methods=['POST'])
def delete_post():
    message = json.loads(request.data)
    flag = delete_post_info(id=message['id'])
    if flag:
      return {'result': 'Delete Post Info Success'}
    else:
      return {'result': 'Delete Post Info Failure'}


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
                'username': user.username,
                # 'userAvatar':  user.pictureUrl, # 等有头像功能再说
                'content': comment.content,
                'time': comment.createTime
            })
        return {"code": code, "comments": ret}
    elif via == 'user':
        code, comments = get_comments_by_user(int(request.args.get('uid')))
        ret = []
        for comment in comments:
            user = search_user_info(comment.sender)
            ret.append({
                'username': user.username,
                # 'userAvatar':  user.pictureUrl, # 等有头像功能再说
                'content': comment.content,
                'time': comment.createTime
            })
        return {"code": code, "comments": ret}
    else:
        return {"code": -1, "message": "Invalid via param!"}