from mongoengine import connect
from mongoengine.errors import NotUniqueError, DoesNotExist

from schemas import User
from exceptions import EmailIsAlreadyTaken, UserDoesNotExist

class DBService:
  def initialize_db(self) -> None:
    print("initializing db...")
    connect("iqtrace")

  def create_user(self, user) -> str:
    new_user = User(**user)
    try:
      new_user.save()
    except NotUniqueError:
      raise EmailIsAlreadyTaken(f"{user['email']} is aleady taken")
    return str(new_user.pk)
  
  def get_user_from_email(self, email) -> User:
    user = User.objects.get(email=email)
    return user
  
  def get_users(self) -> str:
    return User.objects.to_json()
  
  def delete_user(self, id) -> None:
    try:
      return User.objects.get(id=id).delete()
    except DoesNotExist:
      raise UserDoesNotExist(f"User {id} does not exist")
