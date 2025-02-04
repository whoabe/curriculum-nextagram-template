#initializes your app, creating a flask app instance 
from app import app
from flask import render_template
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.posts.views import posts_blueprint
from instagram_web.blueprints.donations.views import donations_blueprint
from instagram_web.blueprints.follows.views import follows_blueprint

from flask_assets import Environment, Bundle
from .util.assets import bundles
from google_oauth import oauth


assets = Environment(app)
assets.register(bundles)


oauth.init_app(app)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(posts_blueprint, url_prefix="/posts")
app.register_blueprint(donations_blueprint, url_prefix="/donations")
app.register_blueprint(follows_blueprint, url_prefix="/follows")

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404   


@app.route("/")
def home():
    return render_template('home.html')

