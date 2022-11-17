from flask import Blueprint,request,render_template,redirect,session
from ..model.check_regist import add_user
from ..model.check_login import getinfo,is_existed,exist_user,login_null
import json

logout_blue=Blueprint('logout',__name__,url_prefix='/logout')

@logout_blue.route('/',methods=["GET","POST"])
def user_logout():
    if request.method=="POST":
        try:
            data=json.loads(request.data)
            logout=data['logout']
            if logout=='True':
                session.clear()
                dict={}
                dict['logout_message']='success: logout'
                dict['logout_code']='1'
                return dict
            else:
                dict={}
                dict['logout_message']='fail: logout'
                dict['logout_code']='0'
                return dict
        except Exception as e:
            print('[Error]', e, 'in logout')
            return
    return    "/logout"    