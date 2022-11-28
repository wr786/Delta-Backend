from flask import Blueprint,request,render_template,redirect,session
from .model.check_regist import add_user,check_pku,regist_null
from .model.check_login import getinfo,is_existed,exist_user,login_null
from .model.check_cache import check_captcha
import json

regist_blue=Blueprint('regist',__name__,url_prefix='/regist')

@regist_blue.route('/',methods=["GET","POST"])
def user_regist():
    if request.method == 'POST':
        try:
            data=json.loads(request.data)
            username=data.get('username')
            email = data.get('email')
            password = data.get('password')
            captcha=data.get('captcha')
            captcha_skip=data.get('captcha_skip')                        #测试需要跳过captcha验证用,captcha_skip=True跳过验证,captcha_skip=False不跳过验证，部署时请删除本行
            print('user_regist:', username,email,password,captcha,captcha_skip)
            dict={}
            if regist_null(username,email,password):
                dict['regist_code']=-1
                dict['regist_message']='fail:need username, email and password'
                return dict
            elif not check_pku(email):
                dict['regist_code']=2
                dict['regist_message']='fail:email adress must be @stu.pku.edu.cn'
                return dict              #2=不是PKU邮箱
            elif exist_user(email):
                dict['regist_code']=1
                dict['regist_message']='fail:email has been registered'
                return dict                        #1=用户已存在
            elif not check_captcha(email,captcha) and not captcha_skip:   #测试需要跳过captcha验证用，部署时请删除 and 后半句
                dict['regist_code']=3
                dict['regist_message']='fail:captcha wrong or expired'
                return dict
            else:
                add_user(data['username'],data['email'], data['password'] )
                dict['regist_code']=0
                dict['regist_message']='success:welcome to delta'
                info=getinfo(email)
                session['username']=info[0]
                session['email']=info[1]
                session['userid']=info[3]
                session.permanent=True
                dict['userid']=info[3]
                return dict                       #0=注册成功   id为auto_increment
        except Exception as e:
            errmsg = f'[Error] {e} in regist'
            print(errmsg)
            return errmsg

    return "/regist"