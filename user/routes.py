# Importa las bibliotecas y clases necesarias
from bson import ObjectId
from flask import render_template, redirect, url_for, request, jsonify, Flask, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from user.models import User, Task
from app import login_required

@app.route('/user/signup', methods=['POST'])
def signup():
    return User().signup()
    
@app.route('/user/signout')
def signout():
    return User().signout()

@app.route('/user/login', methods=['POST'])
def login():
    return User().login()

@app.route('/add_task', methods=['POST'])
def add_task():
    result = Task().add_task()
    return jsonify({"message": "Task added successfully"}), 200

@app.route('/dashboard/tasks', methods=['GET'])
@login_required
def get_user_tasks():
    tasks = Task().get_user_tasks()
    return jsonify([{"nombre": task["nombre"], "detalles": task["detalles"], "fecha_entrega": task["fecha_entrega"]} for task in tasks])


@app.route('/delete_task', methods=['POST'])
def delete_task():
    task_id = request.form.get('task_id')
    Task().delete_task(task_id)
    return jsonify({"message": "Task deleted successfully"}), 200


    user_id = session['user']['_id']

    nombre = request.form['nombre']
    detalles = request.form['detalles']
    fecha_entrega = request.form['fecha_entrega']

    task_model = Task()
    
    if task_model.edit_task(task_id, user_id, nombre, detalles, fecha_entrega):
        return jsonify({"message": "Task edited successfully"}), 200
    else:
        return jsonify({"error": "Task not found or user does not have permission to edit"}), 404


@app.route('/dashboard/')
@login_required
def dashboard():
    tasks = Task().get_user_tasks()
    return render_template('dashboard.html', tasks=tasks)

@app.route('/editar_tarea/<string:task_id>')
@login_required
def editar_tarea(task_id):
    task = Task().get_task_by_id(task_id)
    return render_template('editar_tarea.html', task=task)

@app.route('/edit_task/<string:task_id>', methods=['POST'])
def edit_task(task_id):
    user_id = session['user']['_id']
    nombre = request.form['nombre']
    detalles = request.form['detalles']
    fecha_entrega = request.form['fecha_entrega']

    task_model = Task()

    # Ajusta la llamada a edit_task eliminando el argumento user_id
    if task_model.edit_task(task_id, nombre, detalles, fecha_entrega):
        return redirect('/dashboard')
    else:
        return jsonify({"error": "Task not found or user does not have permission to edit"}), 404
