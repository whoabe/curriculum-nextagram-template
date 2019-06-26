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

    
    profile_image = pw.CharField(default = "default-profile.png", null = False)


    @hybrid_property
    def profile_image_url(self):
        if self.profile_image:
            return Config.S3_LOCATION + self.profile_image
        else:
            return "https://www.vemco.com/wp-content/uploads/2012/09/image-banner2.jpg"


    @hybrid_property
    def json_info(self):
        return {
            'id': self.id,
            'profileImage': self.profile_image_url,
            'username': self.username
        }  