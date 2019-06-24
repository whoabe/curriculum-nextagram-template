from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.user import User
from models.following import Relationship
from config import Config
from models.post import Post
from flask_wtf.csrf import CSRFProtect
from flask_login import login_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user
from werkzeug.utils import secure_filename
from helpers import upload_file_to_s3, gateway

import braintree

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
def index_users():
    #want to show all the users and their posts

    if current_user.is_authenticated:
        user_query = Post.select().join(User, on = (Post.user_id == User.id)).join(Relationship, on = (User.id == Relationship.to_user_id)).where((Relationship.approved == True) & (Relationship.from_user_id == current_user.id)).order_by(Post.updated_at.desc())


        # following = User.select().join(Relationship, on=(User.id == Relationship.to_user_id)).where((Relationship.approved == True) & (Relationship.from_user_id == current_user.id))

        # user_posts = following.prefetch(Post.select().order_by(Post.updated_at))

        #need to have logic that sets approved to true if the profile is not private
        #also have logic that sets approved to false one the user sets their profile to 

    else: 
            #means that no one is logged in, so return posts from public users
        user_query = Post.select().join(User, on = (Post.user_id == User.id)).where(User.is_private == False).order_by(Post.updated_at.desc())

    return render_template('users.html', user = user_query)

# -----------------------------------------------------------------


@users_blueprint.route('/<id>/edit', methods=["GET"])
@login_required
def edit(id):
    #shows the form to edit
    
    return render_template('users/user_edit.html', user = current_user)


@users_blueprint.route('/<id>', methods=['POST'])
@login_required
def update(id):
    is_private = request.form['privacy']
    password = request.form['password']
    user = User.get_by_id(id)
    if check_password_hash(user.password, password):
        #update the user
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['new_password'])
        #new_password is pulled from the html jinja

        result = User.update(username =username, password=password, email=email, is_private = privacy).where(User.id == user.id).execute()

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
    #user profile page
    user = User.get_by_id(id)

    client_token = gateway.client_token.generate()

    #followers = Followers.to_user_id == user.id
    followers = user.followers
    # User.select().join(Relationship, on=(User.id == Relationship.from_user_id)).where(Relationship.to_user_id == user.id)

    #following
    # approved must be true in order for the user to be following the person
    following = user.following
    # User.select().join(Relationship, on=(User.id == Relationship.to_user_id)).where(Relationship.from_user_id == user.id, Relationship.approved == True)

    # if user.is_private == False or if user in user.following:
    # else:
        
        # need to find if the relationship has been approved
        # need to find the relationship based on the user id
        # if Relationship.approved == True, then allow pepole to see this profile 

    #query for posts
    post_query = Post.select().where(Post.user_id == user.id).order_by(Post.updated_at.desc())

    return render_template('users/profile_page.html', user = user, client_token = client_token, followers = followers, following = following, post_query = post_query)


    #showing the profile page with the donate form

    # client_token = gateway.client_token.generate()
    # # client_token = gateway.client_token.generate()
    # return render_template('users.profile_page.html', client_token=client_token)

# -----

@users_blueprint.route('/<id>/follow', methods = ["POST"])
def following(id):
    user = User.get_by_id(id)
    if user != current_user and current_user not in user.followers:
        # if the user is not the current user and if the current user is not already a follower of this user
        relationship = Relationship(from_user = current_user.id, to_user = user.id)
        if relationship.save():
            flash("You are following user: " +user.username)
            return redirect(url_for('users.profile_page',id=user.id))

@users_blueprint.route('/<id>/unfollow', methods = ["POST"])
def unfollowing(id):
    user = User.get_by_id(id)
    x = Relationship.get_or_none(from_user = current_user.id, to_user = user.id)
    if x:
        x.delete_instance()
        flash("You are not following user: " +user.username +"anymore")
        return redirect(url_for('users.profile_page',id=user.id))
    return redirect(url_for('users.profile_page',id=user.id))


# ----------------------------------------------------
#  for the payment button
# these are just example view functions

TRANSACTION_SUCCESS_STATUSES = [
    braintree.Transaction.Status.Authorized,
    braintree.Transaction.Status.Authorizing,
    braintree.Transaction.Status.Settled,
    braintree.Transaction.Status.SettlementConfirmed,
    braintree.Transaction.Status.SettlementPending,
    braintree.Transaction.Status.Settling,
    braintree.Transaction.Status.SubmittedForSettlement
]

# @users_blueprint.route('/checkouts/new', methods=['GET'])
# def new_checkout():
#     client_token = gateway.client_token.generate()
#     # client_token = gateway.client_token.generate()
#     return render_template('users.profile_page.html', client_token=client_token)




@users_blueprint.route('/checkouts', methods=['POST'])
def create_checkout():
    result = gateway.transaction.sale({
        'amount': request.form['amount'],
        'payment_method_nonce': request.form['payment_method_nonce'],
        'options': {
            "submit_for_settlement": True
        }
    })

    if result.is_success or result.transaction:
        return redirect(url_for('users.show_checkout',transaction_id=result.transaction.id))
    else:
        for x in result.errors.deep_errors: flash('Error: %s: %s' % (x.code, x.message))
        return redirect(url_for('users.profile_page'))
        #need to change this url_for view function


@users_blueprint.route('/checkouts/<transaction_id>', methods=['GET'])
def show_checkout(transaction_id):
    
    transaction = gateway.transaction.find(transaction_id)
    result = {}
    if transaction.status in TRANSACTION_SUCCESS_STATUSES:
        result = {
            'header': 'Sweet Success!',
            'icon': 'success',
            'message': 'Your test transaction has been successfully processed. See the Braintree API response and try again.'
        }
    else:
        result = {
            'header': 'Transaction Failed',
            'icon': 'fail',
            'message': 'Your test transaction has a status of ' + transaction.status + '. See the Braintree API response and try again.'
        }

    return render_template('users/show.html', transaction=transaction, result=result)
    #goes back to the user profile page

# @users_blueprint.route("/client_token", methods=["GET"])
# def client_token():
#   return gateway.client_token.generate()

# @users_blueprint.route("/checkout", methods=["POST"])
# def create_purchase():
#   nonce_from_the_client = request.form["payment_method_nonce"]
#   # Use payment method nonce here...