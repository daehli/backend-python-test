from alayatodo import db

class Users(db.Model):
  __tablename__ = 'user'
  id = db.Column('user_id', db.Integer, primary_key = True)
  password = db.Column('password', db.String(255), nullable =False)
  username = db.Column('username', db.String(25), nullable = False)


  def __init__(self, password, username):
    self.password = password
    self.username = username

  def serialize(self):
    return {
      'id' : self.id,
    }
  def __repr__(self):
    return '<User %r>' % self.id

class Todos(db.Model):
   __tablename__ = 'todos'
   id = db.Column('todo_id', db.Integer, primary_key = True)
   user_id = db.Column(db.Integer,db.ForeignKey(Users.id),nullable=False)
   description = db.Column(db.String(255),nullable=False)  
   done = db.Column(db.Boolean)


   def __init__(self, user_id, description,done=False):
     self.user_id = user_id
     self.description = description
     self.done = done

   def serialize(self):
    return {
      'id' : self.id,
      'users' : self.user_id,
      'description': self.description,
      'done': self.done
    }