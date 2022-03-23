from flask_app import app
from flask_app.controllers import con_users, con_recipes

if __name__ == '__main__':
    app.run(debug=True)