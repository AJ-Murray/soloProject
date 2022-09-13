from flask import redirect, render_template, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.post import Post
from flask_app.models.comment import Comment
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
#Add all class imports here (avoid circular imports)



#Renders Register page
@app.route('/')
def index():
    return render_template('index.html')

#Renders Login page
@app.route('/page/login')
def loginpage():
    return render_template('login.html')

#Redirects to Register page
@app.route('/page/register')
def registerpage():
    return redirect('/')

#Creates new user
@app.route('/register', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    data= {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password']),
        'car_make': request.form['car_make'],
        'car_model': request.form['car_model'],
        'car_year': request.form['car_year']
    }
    id = User.save(data)
    session['user_id'] = id
    
    return redirect('/dashboard')


#Logs user in
@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash('Invalid email.', 'login')
        return redirect('/page/login')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Invalid password', 'login')
        return redirect('/page/login')
    session['user_id'] = user.id
    return redirect('/dashboard')



#Check why it wont show first name
#Renders Dashboard
@app.route('/dashboard')
def dashbaord():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template('dashboard.html', user=User.get_by_id(data), all_posts=Post.get_all_posts_with_user(), all_comments=Comment.get_all_comments_with_posts())


@app.route('/edit/account/<int:id>')
def edit_page(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': id
    }
    return render_template('account.html', user=User.get_by_id(data), all_posts=Post.get_all_posts_with_user())


#Update Account
@app.route('/update/account', methods=['POST'])
def update_user():
    if 'user_id' not in session:
        return redirect('/logout')
    if not User.validate_update(request.form):
        return redirect('/edit/account/<int:id>')
    data = {
        'id': session['user_id'],
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'car_make': request.form['car_make'],
        'car_model': request.form['car_model'],
        'car_year': request.form['car_year']
    }
    User.update(data)
    return redirect('/dashboard')



#Logs user out
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')