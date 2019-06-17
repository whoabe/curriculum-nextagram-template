from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(BaseModel, UserMixin):
    username = pw.CharField(unique = True, null = False)
    email = pw.CharField(unique=False, null = False)
    password = pw.CharField(unique = False, null = False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    
    