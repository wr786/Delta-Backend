from flask import Blueprint,request,render_template,redirect,session
from ..model.check_regist import add_user
from ..model.check_login import getinfo,is_existed,exist_user,login_null

getsesinfo_blue=Blueprint('getsesinfo',__name__,url_prefix='/getsesinfo')

@getsesinfo_blue.route('/',methods=['GET','POST'])
def getsesinfo():
    if request.method=='POST':
        try:
            dict={}
            dict['username']=session.get('username')
            dict['email']=session.get('email')
            dict['userid']=session.get('userid')
            return dict
        except Exception as e:
            print('[Error]', e, 'in getsesinfo')
            return 
    return '/getsesinfo'