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
    is_private = pw.BooleanField(default=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    @hybrid_property
    def following(self):
    # query other users through the "relationship" table
    #this returns a list of users that the user is following
        from models.following import Relationship
        return (User
            .select()
            .join(Relationship, on=Relationship.to_user)
            .where((Relationship.from_user == self) & (Relationship.approved == True))
            .order_by(User.username))
            
    @hybrid_property
    def followers(self):
        # this returns a list of users that are following this user
        from models.following import Relationship
        return (User
            .select()
            .join(Relationship, on=Relationship.from_user)
            .where(Relationship.to_user == self)
            .order_by(User.username))
#    def validate(self):
#       duplicate_stores = Store.get_or_none(Store.name == self.name)

#     if duplicate_stores:
#         self.errors.append('Store name not unique')


    
    profile_image = pw.CharField(null = True)
    # can use default = to a string to set it as a deafault for everyone


    @hybrid_property
    def profile_image_url(self):
        if self.profile_image:
            return Config.S3_LOCATION + self.profile_image
        else:
            return "https://www.vemco.com/wp-content/uploads/2012/09/image-banner2.jpg"


# Now, you can access profile image url like this:
# user.profile_image_url

# if not hybrid property, need to access it as a method
# user.profile_image_url()