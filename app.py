import os
import config
from config import Config
from flask import Flask, render_template, request, flash, redirect, url_for
from models.base_model import db    
from models.user import User
import peeweedbevolve
from flask_login import current_user, login_user, logout_user
from flask_login import LoginManager
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from helpers import upload_file_to_s3

from google_oauth import oauth


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

@app.route("/", methods = ['GET'])
def index():
    return render_template('home.html')

@app.route("/login", methods = ['GET'])
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
    return redirect(url_for('users.index_users'))

# ------------------------------------------------------------------------
@app.route('/upload', methods=["GET"])
def upload_form():
    #shows the form to upload user profile image
    return render_template('users/user_edit.html', user = current_user)
    # changed from upload.html to user_edit.html


@app.route("/", methods=["POST"])
def upload_file():

	# A 
    #  We check the request.files object for a user_file key. (user_file is the name of the file input on our form). If it’s not there, we return an error message.

    if "user_file" not in request.files:
        flash("No user_file key in request.files")
        return render_template('users/user_edit.html', user = current_user)

	# B
    # If the key is in the object, we save it in a variable called file.
    file    = request.files["user_file"]

    """
        These attributes are also available

        file.filename               # The actual name of the file
        file.content_type
        file.content_length
        file.mimetype

    """

	# C.
    # We check the filename attribute on the object and if it’s empty, it means the user sumbmitted an empty form, so we return an error message.
    if file.filename == "":
        flash("Please select a file")
        return render_template('users/user_edit.html', user = current_user)

	# D.
    # Finally we check that there is a file and that it has an allowed filetype (this is what the allowed_file function does, you can check it out in the flask docs).

    if file and 'image' in file.content_type:
        file.filename = secure_filename(file.filename)
        # secure_filename = Pass it a filename and it will return a secure version of it. This filename can then safely be stored on a regular file system and passed to os.path.join(). The filename returned is an ASCII only string for maximum portability.
        # output = upload_file_to_s3(file, Config.S3_BUCKET)
        upload_file_to_s3(file, Config.S3_BUCKET)
        user = current_user
        user.profile_image = str(current_user.id) + "-" + file.filename
        if user.save():
            flash("profile image updated")
            return render_template('users/user_edit.html', user = current_user)
        # return str(output)


    else:
        flash('wrong content type')
        return render_template('users/user_edit.html', user = current_user)


# --------------
# --------------
@app.route('/sessions/authorize/google', methods=['GET'])
def authorize():
    token = oauth.google.authorize_access_token()

    if token:
        email = oauth.google.get(
            'https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
        user = User.get_or_none(User.email == email)
        if not user:
            flash('No user registered with this Google Email!', 'danger')
            return redirect(url_for('sessions.new'))

    login_user(user)
    flash(f'Welcome back {user.username}')
    return redirect(url_for('users.index_users'))
    # return render_template('home.html')


# @app.route('/facebook_login', methods=['GET'])
# def facebook_login():
#     redirect_uri = url_for('sessions.facebook_authorize', _external=True)
#     return fb_oauth.facebook.authorize_redirect(redirect_uri, state=session['csrf_token'])


@app.route('/google_login', methods=['GET'])
def google_login():
    redirect_uri = url_for('authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)