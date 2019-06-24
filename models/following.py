from models.base_model import BaseModel
import peewee as pw
from models.user import User
from playhouse.hybrid import hybrid_property

class Relationship(BaseModel):
    from_user = pw.ForeignKeyField(User)
    #user ID
    to_user = pw.ForeignKeyField(User)
    #follower
    approved = pw.BooleanField(default=False)

    @hybrid_property
    def is_approved(self):
        return True if self.approved else False




    # @hybrid_property
    # def profile_image_url(self):
    #     if self.profile_image:
    #         return Config.S3_LOCATION + self.profile_image
    #     else:
    #         return "https://www.vemco.com/wp-content/uploads/2012/09/image-banner2.jpg"


# Now, you can access profile image url like this:
# user.profile_image_url

# if not hybrid property, need to access it as a method
# user.profile_image_url()