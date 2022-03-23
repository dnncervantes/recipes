from flask import render_template, redirect, request, flash, session
from flask_app import app
from flask_app.models.mod_user import User
from flask_app.models.mod_recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

db_log = "recipes_db"

@app.route('/recipes/<int:id>')
def show(id):
    data = {"id" : id}
    context = {"id" : session['id']}
    return render_template("instructions.html", recipe=Recipe.get_recipe_with_user(data), user=User.get_user(context))

@app.route('/create/new')
def new_recipe():
    context = {"id" : session['id']}
    return render_template("create.html", user=User.get_user(context))

@app.route('/recipes/new', methods=['POST'])
def create():
    print(request.form)
    Recipe.save(request.form)
    return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):
    data = {"id" : id}
    context = {"id" : session['id']}
    recipe=Recipe.get_one_recipe(data)
    return render_template("edit.html", recipe=recipe, user=User.get_user(context))

@app.route('/recipes/<int:id>/update', methods=['POST'])
def update_recipe(id):
    print(request.form)
    Recipe.update_recipe(request.form)
    return redirect('/')

@app.route('/recipe/<int:id>/delete')
def delete(id):
    data = {
        "id" : id
    }
    Recipe.delete(data)
    return redirect('/')

