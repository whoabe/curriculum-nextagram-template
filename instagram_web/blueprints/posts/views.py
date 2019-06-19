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

posts_blueprint = Blueprint('posts',
                            __name__,
                            template_folder='templates')


@posts_blueprint.route('/<id>', methods=["GET"])
def image_form(id):
    #shows the form to upload images
    return render_template('posts/new_post.html', user = current_user)

@posts_blueprint.route('/<id>', methods=['POST'])
def image_upload():
	# A 
    #  We check the request.files object for a user_file key. (user_file is the name of the file input on our form). If it’s not there, we return an error message.

    if "user_file" not in request.files:
        flash("No user_file key in request.files")
        return render_template('posts/image_form.html', user = current_user)

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
        return render_template('posts/image_form.html', user = current_user)

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
            flash("image added")
            return render_template('posts/image_form.html', user = current_user)
        # return str(output)


    else:
        flash('wrong content type')
        return render_template('posts/image_form.html', user = current_user)