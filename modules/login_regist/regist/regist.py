from flask import Blueprint,request,render_template,redirect
from model.check_regist import add_user,check_pku
from model.check_login import getinfo,is_existed,exist_user,is_null

regist_blue=Blueprint('regist',__name__,url_prefix='/regist')

@regist_blue.route('/',method='POST')
def user_regist():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if is_null(email,password):
            login_massage = "账号和密码是必填"
            return login_massage
            #return render_template('register.html', message=login_massage)
        elif not check_pku(email):
            login_massage = "请使用PKU邮箱"
            return 2                          #2=不是PKU邮箱
        elif exist_user(email):
            login_massage = "用户已存在，请直接登录"
            return 1                          #1=用户已存在
            # return redirect(url_for('user_login'))
            # return render_template('register.html', message=login_massage)
        else:
            add_user(request.form['username'],request.form['email'], request.form['password'] )
            return 0                           #0=注册成功   id为auto_increment
            #return render_template('index.html', email=email)
    return
    #return render_template('register.html')