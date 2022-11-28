from flask_sqlalchemy import SQLAlchemy

from ..utils import db

# 账户表
class AccountInfo(db.Model):
    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, index=True)