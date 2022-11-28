from ..connect import conn
import hashlib
from ..db import *
cur = conn.cursor()

def login_null(email,password):
	if(email==''or password==''):
		return True
	else:
		return False



def is_existed(email,password):
	try:
		conn.ping(reconnect=True)
		encrypted=encrypt(password)
		account = AccountInfo.query.filter_by(email=email, password=encrypted).one()
		print('is_existed:', account)
		if account == None:
			return False
		else:
			return True
	except Exception as e:
		print('[Error]', e, 'in is_existed')
		return

def exist_user(email):
	try:
		account = AccountInfo.query.filter_by(email=email).one()
		if account == None:
			return False
		else:
			return True
	except Exception as e:
		print('[Error]', e, 'in exist_user')
		return

def exist_name(username):
	try:
		account = AccountInfo.query.filter_by(username=username).one()
		if account == None:
			return False
		else:
			return True
	except Exception as e:
		print('[Error]', e, 'in exist_user')
		return

def getinfo(email):
	try:
		account = AccountInfo.query.filter_by(email=email).one()
		return (account.username, account.email, account.password, account.id)
	except Exception as e:
		print('[Error]', e, 'in getinfo')
		return

def encrypt(pwd): 
    sha = hashlib.sha256(pwd.encode('utf-8'))
    encrypted = sha.hexdigest()
    return encrypted       