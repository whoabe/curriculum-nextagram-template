from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from config import Config
from playhouse.hybrid import hybrid_property

class User(BaseModel, UserMixin):
    username = pw.CharField(unique = True, null = False)
    email = pw.CharField(unique=False, null = False)
    password = pw.CharField(unique = False, null = False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

#    def validate(self):
#       duplicate_stores = Store.get_or_none(Store.name == self.name)

#     if duplicate_stores:
#         self.errors.append('Store name not unique')


    
    profile_image = pw.CharField(null = True)
    # can use default = to a string to set it as a deafault for everyone


    @hybrid_property
    def profile_image_url(self):
        return Config.S3_LOCATION + self.profile_image
# Now, you can access profile image url like this:
# user.profile_image_url

# if not hybrid property, need to access it as a method
# user.profile_image_url()