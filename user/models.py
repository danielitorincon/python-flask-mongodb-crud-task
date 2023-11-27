from flask import Flask, jsonify, request, session, redirect, url_for
from passlib.hash import pbkdf2_sha256
from app import db

from bson import ObjectId


import uuid

class User:

    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200

    def signup(self):

        print(request.form)
        
        #CREATE THE USER OBJECT
        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form['name'],
            "email": request.form['email'],
            "password": request.form['password']
        }

        #ENCRYPT PASSWORD
        user['password'] = pbkdf2_sha256.encrypt(user['password'])  

        #CHECK FOR EXISTING EMAIL ADDRESS
        if db.users.find_one({ "email": user['email'] }):  
            return jsonify({ "error": "Email address already in use" }), 400

        if db.users.insert_one(user):
            return self.start_session(user)

        return jsonify({ "error": "Signup failed" }), 400

    def signout(self):
        session.clear()
        return redirect('/')
    
    def login(self):
        user = db.users.find_one({
            "email": request.form['email']
        })
        
        if user and pbkdf2_sha256.verify(request.form['password'], user['password']):
           
            return self.start_session(user)
        
        return jsonify({ "error": "Invalid login credentials" }), 401

class Task:

    def add_task(self):
        user_id = session['user']['_id']  # Obtén el _id del usuario desde la sesión

        task = {
            "user_id": user_id,  # Asocia la tarea al usuario
            "nombre": request.form['nombre'],
            "detalles": request.form['detalles'],
            "fecha_entrega": request.form['fecha_entrega']
        }

        print("Task to be inserted:", task)  # Agrega esta línea para depuración

        try:
            result = db.tasks.insert_one(task)  # Asegúrate de usar db.tasks en lugar de db.task
            print("Insertion result:", result.inserted_id)  # Agrega esta línea para depuración
            return redirect("/dashboard")
        except Exception as e:
            print("Error during insertion:", str(e))  # Agrega esta línea para depuración
            return jsonify({ "error": "Error durante la inserción de la tarea" }), 500

    def get_user_tasks(self):
        user_id = session['user']['_id']
        tasks = db.tasks.find({"user_id": user_id})
        return tasks


    def delete_task(self, task_id):
        user_id = session['user']['_id']
        db.tasks.delete_one({"_id": ObjectId(task_id), "user_id": user_id})

    def get_task_by_id(self, task_id):
        return db.tasks.find_one({"_id": ObjectId(task_id)})

    def edit_task(self, task_id, nombre, detalles, fecha_entrega):
        user_id = session['user']['_id']
        result = db.tasks.update_one(
            {"_id": ObjectId(task_id), "user_id": user_id},
            {"$set": {"nombre": nombre, "detalles": detalles, "fecha_entrega": fecha_entrega}}
        )
        return result.modified_count > 0
