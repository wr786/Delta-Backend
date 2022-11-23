from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 账户表
class AccountInfo(db.Model):
    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, notnull=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    email = db.Column(db.String(255), index=True)