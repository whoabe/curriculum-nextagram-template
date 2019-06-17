import os
import config
from flask import Flask, render_template, request, flash, redirect, url_for
from models.base_model import db
from models.user import User
import peeweedbevolve

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

app = Flask('NEXTAGRAM', root_path=web_dir)

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

@app.route("/")
def index():
    return render_template('home.html')

        
@app.route("/new")
def x():
    return render_template('new.html')

@app.route("/new_form", methods = ["POST"])
def create():
    data = User(username=request.form['username'], email=request.form['email'], password = request.form['password'])

    if data.save():
        flash("flash saved")
        return redirect(url_for('x'))
        #goes to function x
    else:
        return render_template('new.html', username = request.form['username'], email =request.form['email'], password = request.form['password'])


