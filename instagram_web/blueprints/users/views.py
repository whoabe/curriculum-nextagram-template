from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.user import User
from config import Config
from models.images import Image
from flask_wtf.csrf import CSRFProtect
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user
from werkzeug.utils import secure_filename
from helpers import upload_file_to_s3

# csrf = CSRFProtect(app)

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template('users/new.html')



@users_blueprint.route('/sign_up', methods=['POST'])
def create():
    # data = User(username=request.form['username'], email=request.form['email'], password = request.form['password'])
    username = request.form['username']
    email = request.form['email']
    password = generate_password_hash(request.form['password'])

    # try:
    #     data(username, email, generate_password_hash(password)).save()
    # except:
    #     return render_template('new.html', username = request.form['username'], email =request.form['email'], password = request.form['password'])
    # return flash("user signed up")
    user = User(username =username, password=password, email=email)

    if user.save():
        login_user(user)
        flash("Sucessfully signed up")
        return redirect(url_for('home'))
    else:
        return render_template('new.html', username = request.form['username'], email =request.form['email'], password = request.form['password'])


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"





# --------------------------------------------------------------------


@users_blueprint.route('/<id>/edit', methods=["GET"])
def edit(id):
    #shows the form to edit
    #check if the user is logged in or not, if yes, get the user id
    return render_template('users/user_edit.html', user = current_user)


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    password = request.form['password']
    user = User.get_by_id(id)
    if check_password_hash(user.password, password):
        #update the user
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['new_password'])
        #new_password is pulled from the html jinja

        result = User.update(username =username, password=password, email=email).where(User.id == user.id).execute()

        if result:
            flash("Sucessfully updated")
            return redirect(url_for('home'))
        else:
            return render_template('new.html', username = request.form['username'], email =request.form['email'], password = request.form['password'])
            # return redirect(url_for('home'))
    else:
        flash("Invalid password")
        return render_template('users/user_edit.html', user = user)
    # ------------------------------------------------------------------

@users_blueprint.route('/<id>', methods=["GET"])
def profile_page(id):
    #shows the form to upload images
    return render_template('users/profile_page.html', user = current_user)