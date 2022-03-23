from flask import render_template, redirect, request, flash, session
from flask_app import app
from flask_app.models.mod_user import User
from flask_app.models.mod_recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'id' in session:
        return redirect('/dashboard')
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.valid_register(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }
    user_id = User.new_user(data)
    session['id'] = user_id
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    if not User.valid_login(request.form):
        return redirect('/')
    user_id = User.get_email(request.form)
    session['id'] = user_id.id
    return redirect('/dashboard')

@app.route('/dashboard')
def welcome():
    if 'id' not in session:
        return redirect('/')
    data = {
        'id': session["id"]
        }
    recipe = Recipe.get_all_recipes()
    user = User.get_user(data)
    return render_template('dashboard.html', user=user, all_recipes=recipe)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have signed off', 'logout')
    return redirect('/')
