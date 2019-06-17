from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.user import User
from flask_wtf.csrf import CSRFProtect
from flask_login import login_user
from werkzeug.security import generate_password_hash
from flask_login import current_user

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
        flash("flash saved")
        return redirect(url_for('home'))
    else:
        return render_template('new.html', username = request.form['username'], email =request.form['email'], password = request.form['password'])

@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
