from flask import Blueprint, jsonify
from models.user import User

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')



# 2
@users_api_blueprint.route('/', methods=['GET'])
def index():
    # output = []
    # user = User.select()
    # for i in user:
    #     user_data = {"id":i.id}
    #     output.append(user_data)
    # return jsonify(output)
    user = User.select()
    return jsonify([i.json_info for i in user])

