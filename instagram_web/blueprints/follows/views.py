#follows view functions

from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.user import User
from models.post import Post
from models.following import Relationship
from flask_login import current_user

follows_blueprint = Blueprint('follows',
                            __name__,
                            template_folder='templates')


@follows_blueprint.route('/<id>/follow', methods = ["POST"])
def following(id):
    user = User.get_by_id(id)
    if user != current_user and current_user not in user.followers:
        # if the user is not the current user and if the current user is not already a follower of this user
        relationship = Relationship(from_user = current_user.id, to_user = user.id)

        if not user.is_private:
            relationship.approved = True

        # if relationship.is_approved:
        #     flash(f'You are now following {user.username}', 'success')
        #     return redirect(url_for('users.profile_page',id=user.id))
        # flash('Follow request sent! Please, wait for approval', 'success')
        # return redirect(url_for('users.profile_page',id=user.id))

        if relationship.save():
            flash("You are now following user: " +user.username)
            return redirect(url_for('users.profile_page',id=user.id))

            
@follows_blueprint.route('/<id>/unfollow', methods = ["POST"])
def unfollowing(id):
    user = User.get_by_id(id)
    x = Relationship.get_or_none(from_user = current_user.id, to_user = user.id)
    if x:
        x.delete_instance()
        flash("You are no longer following user: " +user.username)
        return redirect(url_for('users.profile_page',id=user.id))
    return redirect(url_for('users.profile_page',id=user.id))

