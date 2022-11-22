from flask import Blueprint,request,session
from flask_mail import Message,Mail
from flask_cache import Cache
from .model.check_login import exist_user,getinfo
from .model.check_regist import check_pku
import json
import string
import random
sendemail_blue=Blueprint('sendemail',__name__,url_prefix='/sendemail')
mail=Mail()
cache=Cache()

@sendemail_blue.route('/',methods=["GET","POST"])
def sendemail():
    try:
        if request.method == 'POST':
            source = list(string.ascii_letters)
            source.extend(map(lambda x: str(x), range(0, 10)))
            captcha = "".join(random.sample(source, 6))
            data=json.loads(request.data)
            email=data.get('email')
            dict={}
            if exist_user(email):
                dict['sendemail_code']='1'
                dict['sendemail_message']='fail:email has been registered'
                return dict                        #1=用户已存在
            elif not check_pku(email):
                dict['sendemail_code']='2'
                dict['sendemail_massage']='fail:email adress must be @stu.pku.edu.cn or @pku.edu.cn'
                return dict              #2=不是PKU邮箱
            msg=Message("pku_delta验证码",recipients=[email])
            msg.body="验证码是：%s" % captcha
            mail.send(msg)
            dict['sendemail_code']='0'
            dict['sendemail_message']='success: send an email'
            print("send captcha=%s to %s" % (captcha,email))
            cache.set(email,captcha,timeout=1000)  #captcha expired in 1000s
            cap=cache.get(email)
            print("get captcha again : %s captcha: %s"%(email,cap))        
            #cat=cache.get("name")
            #print("name %s" % cat.decode('utf-8'))
            #car=cache.get("noname")
            #print("noname %s" %car)
            return dict
    except Exception as e:
        print('[Error]', e, 'in sendemail')
        return
    return 'sendemail'
