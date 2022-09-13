from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Post:
    db = 'carproject_schema'
    def __init__(self, data):
        self.id = data['id']
        self.details = data['details']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.maker = None


    @classmethod
    def save(cls, data):
        query = 'INSERT INTO posts (details, user_id) VALUES (%(details)s, %(user_id)s);'
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM posts'
        results = connectToMySQL(cls.db).query_db(query)
        posts = []
        for row in results:
            posts.append(cls(row))
        return posts

    #Gets all posts with user
    @classmethod
    def get_all_posts_with_user(cls):
        query = 'SELECT * FROM posts JOIN users ON posts.user_id = users.id;'
        results = connectToMySQL(cls.db).query_db(query)
        all_posts = []
        for row in results:
            one_post = cls(row)
            one_posts_creator_info = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'car_make': row['car_make'],
                'car_model': row['car_model'],
                'car_year': row['car_year'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            creator = user.User(one_posts_creator_info)
            one_post.maker = creator
            all_posts.append(one_post)
        return all_posts
    
    


    #Deletes a post
    @classmethod
    def delete(cls,data):
        query = 'DELETE FROM posts WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query,data)




    #Validate Post
    @staticmethod
    def validate_post(post):
        is_valid = True
        if len(post['details']) < 10:
            is_valid = False
            flash("Post must be at least 10 characters","post")
        return is_valid