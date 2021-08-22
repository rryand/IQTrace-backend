from mongoengine import Document, StringField, BooleanField

class User(Document):
  email: StringField(required=True)
  first_name: StringField(required=True, max_length=50)
  last_name: StringField(required=True, max_length=50)
  is_admin: BooleanField(default=False)
