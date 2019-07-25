# -*- coding: utf-8 -*-
import sys
import pymysql  # 2019-07-25 mmesas: Cambio de mysql-python a pymysql
import pymysql.cursors # 2019-07-25 mmesas: Cambio de mysql-python a pymysql

# from importlib import reload

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate


# reload(sys)  # 2019-02-06 mmesas
# sys.setdefaultencoding('utf-8')

app = Flask(__name__)
app.config.from_object('config_app.DevelopConfig')

db = SQLAlchemy(app)

# conexion a la base de datos con MySQLdb
connectiondb = pymysql.connect(
    host='127.0.0.1',
    port=33060,
    user=app.config['DB_USER'],
    passwd=app.config['DB_PASS'],
    db=app.config['DB_NAME'],
    cursorclass=pymysql.cursors.DictCursor,
    charset='utf8mb4')


Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

migrate = Migrate(app, db)
# >>> flask db migrate / para traer los cambios
# >>> flask db upgrade / para hacer commit a los cambios

mail = Mail(app)

from app import views
