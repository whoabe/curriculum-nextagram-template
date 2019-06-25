from flask import Blueprint, jsonify, request
from models.user import User
from models.post import Post

posts_api_blueprint = Blueprint('posts_api',
                             __name__,
                             template_folder='templates')


@posts_api_blueprint.route('/<id>/', methods=['GET'])
def asd(id):
    user = User.get_by_id(id)
    if user:
        post = Post.select().where(Post.user_id == user.id)
        return jsonify(post[0].image)
    return "BYE"
