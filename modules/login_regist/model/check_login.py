from lrconfig import conn
cur = conn.cursor()


def is_null(email,password):
	if(email==''or password==''):
		return True
	else:
		return False


def is_existed(email,password):
	conn.ping(reconnect=True)
	sql="SELECT * FROM user WHERE email ='%s' and password ='%s'" %(email,password)
	cur.execute(sql)
	result = cur.fetchall()
	if (len(result) == 0):
		return False
	else:
		return True

def exist_user(email):
	conn.ping(reconnect=True)
	sql = "SELECT * FROM user WHERE email ='%s'" % (email)
	cur.execute(sql)
	result = cur.fetchall()
	if (len(result) == 0):
		return False
	else:
		return True

def getinfo(email):
	conn.ping(reconnect=True)
	sql="SELECT * FROM user WHERE email ='%s'" % (email)
	cur.execute(sql)
	result=cur.fetchall() #tuple=(username，email，password，id)
	return result
