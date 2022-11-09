from ..lrconfig import conn
cur = conn.cursor()


def login_null(email,password):
	if(email==''or password==''):
		return True
	else:
		return False


def is_existed(email,password):
	try:
		conn.ping(reconnect=True)
		sql="SELECT * FROM user WHERE email ='%s' and password ='%s'" %(email,password)
		cur.execute(sql)
		result = cur.fetchall()
		if (len(result) == 0):
			return False
		else:
			return True
	except Exception as e:
		print('[Error]', e, 'in is_existed')
		return

def exist_user(email):
	try:
		conn.ping(reconnect=True)
		sql = "SELECT * FROM user WHERE email ='%s'" % (email)
		cur.execute(sql)
		result = cur.fetchall()
		if (len(result) == 0):
			return False
		else:
			return True
	except Exception as e:
		print('[Error]', e, 'in exist_user')
		return

def getinfo(email):
	try:
		conn.ping(reconnect=True)
		sql="SELECT * FROM user WHERE email ='%s'" % (email)
		cur.execute(sql)
		result=cur.fetchone() #tuple=(username，email，password，id)
		return result
	except Exception as e:
		print('[Error]', e, 'in getinfo')
		return
