from flask import Blueprint,request,render_template,redirect
from .model.check_regist import add_user,check_pku,regist_null
from .model.check_login import getinfo,is_existed,exist_user,login_null
import json
regist_blue=Blueprint('regist',__name__,url_prefix='/regist')

@regist_blue.route('/',methods=["GET","POST"])
def user_regist():
    if request.method == 'POST':
        try:
            data=json.loads(request.data)
            username=data['username']
            email = data['email']
            password = data['password']
            dict={}
            if regist_null(username,email,password):
                dict['regist_code']='-1'
                dict['regist_message']='fail:need username, email and password'
                return dict
            elif not check_pku(email):
                dict['regist_code']='2'
                dict['regist_message']='fail:email adress must be @stu.pku.edu.cn'
                return dict              #2=不是PKU邮箱
            elif exist_user(email):
                dict['regist_code']='1'
                dict['regist_message']='fail:email has been registered'
                return dict                        #1=用户已存在
            else:
                add_user(data['username'],data['email'], data['password'] )
                dict['regist_code']='0'
                dict['regist_message']='success:welcome to delta'
                return dict                       #0=注册成功   id为auto_increment
        except Exception as e:
            print('[Error]', e, 'in regist')
            return

    return "/regist"