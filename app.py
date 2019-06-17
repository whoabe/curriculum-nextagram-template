import os
import config
from flask import Flask, render_template, request, flash, redirect, url_for
from models.base_model import db
from models.user import User
import peeweedbevolve
from flask_login import current_user, login_user, logout_user
from models.user import User
from flask_login import LoginManager
from werkzeug.security import check_password_hash


#login_manager calls the LoginManger function


web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

app = Flask('NEXTAGRAM', root_path=web_dir)

login_manager = LoginManager()
login_manager.init_app(app)


if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc

@login_manager.user_loader
    # This callback is used to reload the user object from the user ID stored in the session
def load_user(user_id):
    return User.get_or_none(User.id == user_id)

@app.route("/")
def index():
    return render_template('home.html')

@app.route("/login")
def login_x():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    #checks if the current user is authenticated, if yes, redirect to the homepage, else proceeds to the sign in page
    return render_template('sign_in.html')

@app.route('/login_form', methods = ['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.get_or_none(User.username == username)
    #returns the user id or None

    if user == None:
        flash("Invalid username")
        return redirect(url_for('login_x'))
    elif not check_password_hash(user.password, password):
            flash("Invalid password")
            return redirect(url_for('login_x'))

    login_user(user)
    flash("Logged in")
    return redirect(url_for('home'))
    #need to implement this into the homepage


@app.route('/logout', methods = ['GET'])
def logout():
    logout_user()
    flash("Logged out")
    return redirect(url_for('home'))