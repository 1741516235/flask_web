#encoding:utf-8
import os
DEBUG = True
SECRET_KEY = os.urandom(24)
HOSTNAME = '127.0.0.1'
PORT = 3306
DATABASE = 'demo'
USERNAME = 'root'
PASSWORD = 'root'
DB_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset = utf8mb4'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI