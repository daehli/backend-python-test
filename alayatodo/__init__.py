from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


# configuration
DATABASE = '/tmp/alayatodo.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{0}'.format(DATABASE)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

import alayatodo.views