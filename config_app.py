# -*- coding: utf-8 -*-
import os


class Config(object):
	DEBUG = False
	TESTING = False


class ProductionConfig(Config):

	DB_NAME = os.environ.get('DB_NAME')
	DB_USER = os.environ.get('DB_USER')
	DB_PASS = os.environ.get('DB_PASS')

	WTF_CSRF_ENABLE = True
	SECRET_KEY = os.environ.get('SECRET_KEY')

	SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@localhost/{}'.format(DB_NAME, DB_PASS, DB_NAME)
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 465
	MAIL_USE_SSL = True
	MAIL_USE_TLS = False
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
