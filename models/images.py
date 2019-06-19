from models.base_model import BaseModel
from models.user import User
import peewee as pw

# from flask_login import UserMixin
# from config import Config
# from playhouse.hybrid import hybrid_property

class Image(BaseModel):
    user = pw.ForeignKeyField(User, backref = 'images', on_delete='cascade')
    image = pw.CharField(null = True)
    # can use default = to a string to set it as a deafault for everyone


# @hybrid_property
# def profile_image_url(self):
#     return Config.S3_LOCATION + self.profile_image
# # Now, you can access profile image url like this:
# # user.profile_image_url

# # if not hybrid property, need to access it as a method
# # user.profile_image_url()
