from app import app
from flask_cors import CORS

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

## API Routes ##
#1
from instagram_api.blueprints.posts.views import posts_api_blueprint

#2
from instagram_api.blueprints.users.views import users_api_blueprint



#1 images
app.register_blueprint(posts_api_blueprint, url_prefix='/api/v1/posts')


#2 users
app.register_blueprint(users_api_blueprint, url_prefix='/api/v1/users')

