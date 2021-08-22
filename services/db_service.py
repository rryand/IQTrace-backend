from mongoengine import connect
from schemas import User

class DBService:
  def initialize_db(self):
    print("initializing db...")
    connect("iqtrace")  

  def create_user(self, user):
    new_user = User(**user)
    new_user.save()
    return new_user.pk
  
  def get_users(self):
    return User.objects.to_json()
  
  def delete_user(self):
    return User.objects[0].delete()
