from flask import redirect, render_template, session, request, flash
from flask_app import app
from flask_app.models.post import Post
from flask_app.models.comment import Comment
from flask_app.models.user import User


@app.route('/create/comment/<int:id>', methods=['POST'])
def create_comment(id):
    if 'user_id' not in session:
        return redirect('logout')
    data = {
        'comment': request.form['comment'],
        'user_id': session['user_id'],
        'post_id': id
    }
    Comment.save(data)
    return redirect('/dashboard')


#Deletes Comment
@app.route('/delete/comment/<int:id>')
def delete_comment(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': id
    }
    Comment.delete(data)
    return redirect('/dashboard')