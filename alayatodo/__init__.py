from flask import Flask, g
import sqlite3
import os
# configuration

app = Flask(__name__)

if os.environ['PRODUCTION']:
  app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
  SECRET_KEY = os.environ['SECRET_KEY']
  app.config.from_object(os.environ['APP_SETTINGS'])
  DEBUG = False

else:
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/alayatodo.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
  SECRET_KEY = 'development key'
  USERNAME = 'admin'
  PASSWORD = 'default'
  DEBUG = True
  app.config.from_object(__name__)


import alayatodo.views
