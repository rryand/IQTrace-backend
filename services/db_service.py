from mongoengine import connect
from mongoengine.errors import NotUniqueError, DoesNotExist

from schemas import User, Room
from exceptions import EmailIsAlreadyTaken, RoomNumberIsAlreadyTaken, UserDoesNotExist

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
  
  def get_user_id_from_email(self, email) -> str:
    user = self.get_user_from_email(email)
    return str(user.pk)
  
  def get_users(self):
    return User.objects.to_json()
  
  def delete_user(self, id) -> None:
    try:
      return User.objects.get(id=id).delete()
    except DoesNotExist:
      raise UserDoesNotExist(f"User {id} does not exist")
  
  def create_room(self, room):
    new_room = Room(**room)
    try:
      new_room.save()
    except NotUniqueError:
      raise RoomNumberIsAlreadyTaken(
        f"Room number {room['number']} is already taken.")
    return str(new_room.pk)
  
  def get_rooms(self):
    return Room.objects.to_json()
