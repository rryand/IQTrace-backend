from mongoengine import Document, StringField, BooleanField, DateField, IntField

class User(Document):
  email = StringField(required=True, unique=True)
  password = StringField(required=True)
  is_admin = BooleanField(default=False)
  first_name = StringField(required=True, max_length=50)
  last_name = StringField(required=True, max_length=50)
  contact_number = StringField(required=True)
  birthday = DateField(required=True)

class Entry(Document):
  user_id = StringField(required=True)
  room_number = IntField(required=True)
  timestamp = DateField(required=True)

class Room(Document):
  number = IntField(required=True, unique=True)
  name = StringField(unique=True)

  meta = {
    'indexes': [
      'number'
    ]
  }
