from models.base_model import BaseModel
from models.user import User
import peewee as pw

# from flask_login import UserMixin
from config import Config
from playhouse.hybrid import hybrid_property

class Post(BaseModel):  
    user = pw.ForeignKeyField(User, backref = 'posts', on_delete='cascade')
    image = pw.CharField(null = True)
    caption = pw.CharField(null = True)
    # can use default = to a string to set it as a deafault for everyone

    @hybrid_property
    def post_image_url(self):
        return Config.S3_LOCATION + self.image
# # Now, you can access profile image url like this:
# # user.profile_image_url

# # if not hybrid property, need to access it as a method
# # user.profile_image_url()
