from alayatodo import app, db
from alayatodo.models import Users, Todos
from flask import (
    g,
    redirect,
    render_template,
    request,
    session,
    jsonify,
    flash,
    abort
    )
import re

MAX_PER_PAGE = 10 

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
        session['user'] = user.serialize()
        session['logged_in'] = True
        flash('Success Login')
        return redirect('/todo')

    flash('Bad username or password')
    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    flash('You are logout')
    return redirect('/')


@app.route('/todo/<id>', methods=['GET'])
def todo(id):
    if not session.get('logged_in'):
        return redirect('/login')
    todo = Todos.query.filter_by(id=id,user_id=session['user']['id']).first()
    if todo:
        return render_template('todo.html', todo=todo)
    else:
        flash('No Task on this ID')
        return redirect('/todo')

@app.route('/todo/<id>/json', methods=['GET'])
def todo_to_json(id):
    if not session.get('logged_in'):
        return redirect('/login')
    todo = Todos.query.filter_by(id=id,user_id=session['user']['id']).first()
    if todo:
        todo = todo.serialize()
        return jsonify(todo)
    else:
        abort(404)


@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
@app.route('/todo/pages/<int:page>',methods=['GET'])
def pagination(page=1):
    if not session.get('logged_in'):
        return redirect('/login')
    page = Todos.query.filter_by(user_id=session['user']['id']).order_by(Todos.id.desc()).paginate(page,MAX_PER_PAGE,False)
    return render_template('todos.html',todos=page)

@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
def todos_POST():
    if not session.get('logged_in'):
        return redirect('/login')

    descriptionValue = request.form.get('description')
    if re.match(r'\w',descriptionValue):
        todo = Todos(user_id=session['user']['id'],description=descriptionValue,done=False)
        db.session.add(todo)
        db.session.commit()
        flash('Congratulation you have added a new task')
        return redirect('/todo')
    else :
        flash('You need to give a description to your task','error')
        return redirect('/todo')

        

@app.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    todo = Todos.query.filter_by(id=id,user_id=session['user']['id']).first()
    if todo: 
        db.session.delete(todo)
        db.session.commit()
        flash('You have delete a task')
        return redirect('/todo')
    else:
        abort(404)

@app.route('/todo/<id>/<done>',methods=['POST'])
def todo_is_done(id,done):  
    if not session.get('logged_in'):
        return redirect('/login')
    completed = False if re.match(r'true|yes',done,re.IGNORECASE) else True
    todo = Todos.query.filter_by(id=id,user_id=session['user']['id']).first()
    if todo:
        todo.done = completed
        db.session.commit()
        if completed:
            flash('You have done a task','info')
        else :
            flash('You have undo a task','info')
        return redirect('/todo')
    else:
        abort(404)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
