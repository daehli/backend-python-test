from flask_sqlalchemy import SQLAlchemy
from alayatodo import app

db = SQLAlchemy(app)

class Users(db.Model):
  id = db.Column('user_id', db.Integer, primary_key = True)
  password = db.Column('password', db.String(255), nullable =False)
  username = db.Column('username', db.String(25), nullable = False)

  def __repr__(self):
    return '<User %r>' % self.id

class todos(db.Model):
   id = db.Column('todo_id', db.Integer, primary_key = True)
   user_id = db.Column(db.Integer,db.ForeignKey(Users.id),nullable=False)
   description = db.Column(db.String(255),nullable=False)  
   done = db.Column(db.Boolean)

   def __repr__(self):
    return '<User %r>' % self.user_id
