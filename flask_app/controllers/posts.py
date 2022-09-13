from flask import redirect, render_template, session, request, flash
from flask_app import app
from flask_app.models.post import Post
from flask_app.models.user import User
from flask_app.models.comment import Comment


#Creat new post
@app.route('/create/post', methods=['POST'])
def create_post():
    if 'user_id' not in session:
        return redirect('logout')
    if not Post.validate_post(request.form):
        return redirect('/dashboard')
    data = {
        'details': request.form['details'],
        'user_id': session['user_id']
    }
    Post.save(data)
    return redirect('/dashboard')


#Deletes Post
@app.route('/delete/post/<int:id>')
def delete_post(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': id
    }
    Post.delete(data)
    return redirect('/dashboard')