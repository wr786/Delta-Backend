from flask import Blueprint,request,render_template,redirect,session
from .model.check_regist import add_user
from .model.check_login import getinfo,is_existed,exist_user,login_null
import json

login_blue=Blueprint('login',__name__,url_prefix='/login')

@login_blue.route('/',methods=["GET","POST"])
def user_login():
    if request.method=='POST':  # 注册发送的请求为POST请求
        try:
            data=json.loads(request.data)
            email = data.get('email')
            password = data.get('password')
            dict={}
            if login_null(email,password):
                dict['login_code']=-1
                dict['login_message']='fail:need email and password'
                return dict           #-1=需要邮箱和密码
            elif is_existed(email, password):
                info=getinfo(email)     #获得账户信息 
                dict['login_code']=0
                dict['login_message']='success: welcome back'
                dict['username']=info[0]
                dict['userid']=info[3]
                session['username']=info[0]
                session['email']=info[1]
                session['userid']=info[3]
                session.permanent=True
                return dict           #0=登录成功
            elif exist_user(email):
                dict['login_code']=2
                dict['login_message']='fail:wrong password'
                return dict             #2=密码错误
            else:
                dict['login_code']=1
                dict['login_message']='fail:no such account'
                return dict             #1=不存在该用户
        except Exception as e:
            print('[Error]', e, 'in login')
            return

    return    "/login"    