from enum import unique
from mongoengine import Document, StringField, BooleanField, DateField

class User(Document):
  email = StringField(required=True, unique=True)
  is_admin = BooleanField(default=False)
  first_name = StringField(required=True, max_length=50)
  last_name = StringField(required=True, max_length=50)
  contact_number = StringField(required=True)
  birthday = DateField(required=True)
