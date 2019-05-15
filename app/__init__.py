# -*- coding: utf-8 -*-
import sys
import MySQLdb  # 2019-02-06 mmesas
import MySQLdb.cursors  # 2019-02-06 mmesas

from importlib import reload

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate


reload(sys)  # 2019-02-06 mmesas
# sys.setdefaultencoding('utf-8')

app = Flask(__name__)
app.config.from_object('config_app.ProductionConfig')

db = SQLAlchemy(app)

# conexion a la base de datos con MySQLdb

connectiondb = MySQLdb.connect(host='localhost',
                               user=app.config['DB_USER'],
                               passwd=app.config['DB_PASS'],
                               db=app.config['DB_NAME'],
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
