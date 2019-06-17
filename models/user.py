from models.base_model import BaseModel
import peewee as pw


class User(BaseModel):
    username = pw.CharField(unique = True, null = False)
    email = pw.CharField(unique=False, null = False)
    password = pw.CharField(unique = False, null = False)