from alayatodo.models import Todos, Users
from alayatodo import db

def init_fixture():
  user1 = Users(username="user1",password="user1")
  user2 = Users(username="user2",password="user2")
  user3 = Users(username="user3",password="user3")


  db.session.add(user1)
  db.session.add(user2)
  db.session.add(user3)

  db.session.commit()

  todo1 = Todos(user_id=1,description='Vivamus tempus',done=False)
  todo2 = Todos(user_id=1,description='lorem ac odio',done=False)
  todo3 = Todos(user_id=1,description='Ut congue odio',done=False)
  todo4 = Todos(user_id=1,description='Sodales finibus',done=False)
  todo5 = Todos(user_id=2,description='Accumsan nunc vitae',done=False)
  todo6 = Todos(user_id=2,description='Lorem ipsum',done=False)
  todo7 = Todos(user_id=2,description='In lacinia est',done=False)
  todo8 = Todos(user_id=1,description='Vivamus tempus',done=False)
  todo9 = Todos(user_id=1,description='Odio varius gravida',done=False)

  db.session.add(todo1)
  db.session.add(todo2)
  db.session.add(todo3)
  db.session.add(todo4)
  db.session.add(todo5)
  db.session.add(todo6)
  db.session.add(todo7)
  db.session.add(todo8)
  db.session.add(todo9)

  db.session.commit()