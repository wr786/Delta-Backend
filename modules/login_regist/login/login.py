from flask import Blueprint,request,render_template,redirect
from model.check_regist import add_user
from model.check_login import getinfo,is_existed,exist_user,is_null

login_blue=Blueprint('login',__name__,url_prefix='/login')

@login_blue.route('/',method='POST')
def user_login():
    if request.method=='POST':  # 注册发送的请求为POST请求
        email = request.form['email']
        password = request.form['password']
        if is_null(email,password):
            login_massage = "账号和密码必填"
            return login_massage
            #return render_template('login.html', message=login_massage)
        elif is_existed(email, password):
            login_massage = "登录成功"
            info=getinfo(email)     #获得账户信息 info[0]=username  info[1]=id ,暂时用id代替token？
            return 0            #0=登录成功
            # return render_template('index.html', email=email)
        elif exist_user(email):
            login_massage = "密码错误，请输入正确密码"
            return 2             #2=密码错误
            #return render_template('login.html', message=login_massage)
        else:
            login_massage = "不存在该用户，请先注册"
            return 1               #1=不存在该用户
            #return render_template('login.html', message=login_massage)
    return        
    #return render_template('login.html')