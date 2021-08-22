from mongoengine import connect
from mongoengine.errors import NotUniqueError

from schemas import User
from exceptions import EmailIsAlreadyTaken

class DBService:
  def initialize_db(self):
    print("initializing db...")
    connect("iqtrace")  

  def create_user(self, user):
    new_user = User(**user)
    try:
      new_user.save()
    except NotUniqueError:
      raise EmailIsAlreadyTaken(f"{user['email']} is aleady taken")
    return new_user.pk
  
  def get_users(self):
    return User.objects.to_json()
  
  def delete_user(self):
    return User.objects[0].delete()
