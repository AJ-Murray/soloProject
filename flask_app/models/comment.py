from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user, post

class Comment:
    db = 'carproject_schema'
    def __init__(self, data):
        self.id = data['id']
        self.comment = data['comment']
        self.user_id = data['user_id']
        self.post_id = data['post_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.maker = None


    @classmethod
    def save(cls, data):
        query = 'INSERT INTO comments (comment, user_id, post_id) VALUES (%(comment)s, %(user_id)s, %(post_id)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all_comments_with_posts(cls):
        query = 'SELECT * FROM comments JOIN posts ON comments.post_id = posts.id;'
        results = connectToMySQL(cls.db).query_db(query)
        all_comments = []
        for row in results:
            one_comment = cls(row)
            one_comment_post_details = {
                'id': row['posts.id'],
                'details': row['details'],
                'user_id': row['user_id'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            }
            post_data = post.Post(one_comment_post_details)
            one_comment.maker = post_data
            all_comments.append(one_comment)
        return all_comments


    #Deletes a Comment
    @classmethod
    def delete(cls,data):
        query = 'DELETE FROM comments WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query,data)



