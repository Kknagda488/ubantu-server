

from flask import render_template, jsonify,request, flash, redirect, url_for,session,Flask
from app import app,db
from app.models.user import User
import re 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user,LoginManager
from flask_mail import Mail, Message


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'kknagda488@gmail.com'
app.config['MAIL_PASSWORD'] = 'cpyozwlnpynpihch'
app.config['MAIL_DEFAULT_SENDER'] = 'krishnajcr72004@gmail.com'
    
mail = Mail(app)
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
@app.route('/admin/confirm/<int:user_id>')
def admin_confirm(user_id):
    # Find the user with the given ID
    user = User.query.get(user_id)

    if user:
        user.approved = True
        db.session.commit()
        return 'User approved and data stored in the database.'

    return 'Invalid confirmation link.'
def send_confirmation_email_to_admin(name, email):
    user = User.query.filter_by(email=email).first()
    confirm_link = f"http://http://127.0.0.1:3000/admin/confirm/{user}"
    msg = Message('New User Registration', recipients=['admin@example.com'])
    msg.html = render_template('admin_confirmation_email.html', name=name, email=email, confirm_link=confirm_link)
    mail.send(msg)
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        send_confirmation_email_to_admin(name, email)
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            send_confirmation_email_to_admin(name, email)
            new_user = User(email=email, name=name, password=generate_password_hash(
                password1, method='sha256'), approve=admin_confirm(User.query.get(id)))
            db.session.add(new_user)
            db.session.commit()
            send_confirmation_email_to_admin(name, email)

            return 'Registration successful! Please wait for admin approval.'

    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@app.route('/am', methods=['GET'])
def testAM():
    return jsonify({'result': "sucess"})
