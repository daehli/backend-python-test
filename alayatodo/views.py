from alayatodo import app
from alayatodo.models import db, Users, Todos
from flask import (
    g,
    redirect,
    render_template,
    request,
    session,
    jsonify,
    flash
    )


@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        readme = "".join(l.decode('utf-8') for l in f)
        return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_POST():
    username = request.form.get('username')
    password = request.form.get('password')

    user = Users.query.filter_by(username=username,password=password).first()
    if user:
        session['user'] = dict(user)
        session['logged_in'] = True
        return redirect('/todo')

    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect('/')


@app.route('/todo/<id>', methods=['GET'])
def todo(id):
    todo = Todos.query.filter_by(id=id).first()
    if todo:
        return render_template('todo.html', todo=todo)
    else:
        return redirect('/todo')


@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
def todos():
    if not session.get('logged_in'):
        return redirect('/login')
    db.engine.connect()
    todos = Todos.query.all()

    return render_template('todos.html', todos=todos)


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
def todos_POST():
    if not session.get('logged_in'):
        return redirect('/login')

    descriptionIsPresent = request.form.get('description')
    if descriptionIsPresent:
        todo = Todos(session['user']['id'],descriptionIsPresent)
        db.session.add(todo)
        db.session.commit()
        flash('Congratulation you have added a new task')
        return redirect('/todo')
    else :
        return flash('You need to give a description to your task','error')
        


@app.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    todo = Todos.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    flash('You have delete a task')
    return redirect('/todo')


@app.route('/todo/<id>/json', methods=['GET'])
def todo_to_json(id):
    todo = Todos.query.filter_by(id=id).first()
    if todo:
        todo = todo.serialize()
        print("Type : {0}, Value : {1}".format(type(todo),todo))
        return jsonify(todo)



@app.route('/todo/<id>/<done>',methods=['POST'])
def todo_is_done(id,done):  
    if not session.get('logged_in'):
        return redirect('/login')
    completed = False if done is True else True
    print("Type : {0}, value : {1}".format(type(completed),completed))
    todo = Todos.query.filter_by(id=id).first()
    todo.done = completed
    db.session.commit()
    if completed:
        flash('You have done a task','info')
    else :
        flash('You have undo a task','info')
    return redirect('/todo')
