from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class User:
    db = "carproject_schema"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.car_make = data['car_make']
        self.car_model = data['car_model']
        self.car_year = data['car_year']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.posts = []

    #Saves new user
    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password, car_make, car_model, car_year) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(car_make)s, %(car_model)s, %(car_year)s);"
        return connectToMySQL(cls.db).query_db(query,data)



    #Gets all from users
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM users;'
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users

    #Gets user by ID
    @classmethod
    def get_by_id(cls,data):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    #Gets user by email
    @classmethod
    def get_by_email(cls,data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])


    #Updates user account
    @classmethod
    def update(cls,data):
        query = 'UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, car_make=%(car_make)s, car_model=%(car_model)s, updated_at=NOW() WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query,data)

    #Validate Registration
    @staticmethod
    def validate_register(user):
        is_valid = True 
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL(User.db).query_db(query,user)
        if len(results) >= 1:
            flash('Email already in use, please try another.','register')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid email, please try again.','register')
            is_valid = False
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters","register")
            is_valid= False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters","register")
            is_valid= False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid= False
        if user['password'] != user['confirm_password']:
            flash("Passwords don't match","register")
            is_valid= False
        if len(user['car_make']) < 3:
            flash("Car make must be at least 3 characters","register")
            is_valid= False
        if len(user['car_model']) < 3:
            flash("Car model must be at least 3 characters","register")
            is_valid= False
        if len(user['car_year']) != 4:
            flash("Please enter a vaild year","register")
            is_valid= False
        return is_valid

    @staticmethod
    def validate_update(user):
        is_valid = True
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL(User.db).query_db(query,user)
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters","update")
            is_valid= False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters","update")
            is_valid= False
        if len(user['car_make']) < 3:
            flash("Car make must be at least 3 characters","update")
            is_valid= False
        if len(user['car_model']) < 3:
            flash("Car model must be at least 3 characters","update")
            is_valid= False
        if len(user['car_year']) != 4:
            flash("Please enter a vaild year","update")
            is_valid= False
        return is_valid