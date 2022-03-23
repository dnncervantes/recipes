from flask_app.config.mysqlconnection import connectToMySQL
from.mod_user import User

db_log= 'recipes_db'

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_30 = data['under_30']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator_id = data['creator_id']

    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(db_log).query_db(query)
        recipes = []
        for row in results:
            recipes.append(cls(row))
        return recipes

    @classmethod
    def get_one_recipe(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(db_log).query_db(query,data)
        return cls(results[0])

    @classmethod
    def select_one_recipe(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(db_log).query_db(query,data)

    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, under_30 = %(under_30)s, date_made = %(date_made)s WHERE id = %(id)s"
        return connectToMySQL(db_log).query_db(query,data)

    @classmethod
    def save(cls,data):
        query = "INSERT INTO recipes (name, description, instructions, under_30, date_made, creator_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(under_30)s, %(date_made)s, %(creator_id)s);"
        return connectToMySQL(db_log).query_db(query,data)


    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(db_log).query_db(query,data)


    @classmethod
    def get_recipe_with_user(cls,data):
        query = "SELECT * FROM recipes LEFT JOIN users on recipes.creator_id = users.id WHERE recipes.id = %(id)s;"
        results = connectToMySQL(db_log).query_db(query, data)
        row = results[0]
        recipe = cls(row)
        user_data = {
            **row,
            "id": row['users.id'],
            "created_at": row['users.created_at'],
            "updated_at": row['users.updated_at']
        }
        recipe.user = User(user_data)
        return recipe
