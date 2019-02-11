# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
import MySQLdb  # 2019-02-06 mmesas
import MySQLdb.cursors  # 2019-02-06 mmesas
import sys


reload(sys)  # 2019-02-06 mmesas
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
app.config.from_object('config_app')

db = SQLAlchemy(app)

# conexion a la base de datos con MySQLdb

connectiondb = MySQLdb.connect(host='localhost',
                               user='sa_soluciones',
                               passwd='soluciones2018',
                               db='soluciones_db',
                               cursorclass=MySQLdb.cursors.DictCursor,
                               use_unicode=True,
                               charset='utf8')


Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

migrate = Migrate(app, db)
# >>> flask db migrate / para traer los cambios
# >>> flask db upgrade / para hacer commit a los cambios

mail = Mail(app)

from app import views
