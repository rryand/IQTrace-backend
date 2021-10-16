from mongoengine import connect
from mongoengine.errors import NotUniqueError, DoesNotExist

from schemas import User, Room, Timelog
from exceptions import (EmailIsAlreadyTaken, RoomDoesNotExist,
  RoomHasDuplicateNumberOrName, UserDoesNotExist)


def initialize_db() -> None:
  print("initializing db...")
  connect("iqtrace")

def create_user(user) -> str:
  new_user = User(**user)
  try:
    new_user.save()
  except NotUniqueError:
    raise EmailIsAlreadyTaken(f"{user['email']} is aleady taken")
  return str(new_user.pk)

def get_user_from_email(email) -> User:
  try:
    user = User.objects.get(email=email)
  except DoesNotExist:
    return None
  return user

def get_user_id_from_email(email) -> str:
  user = get_user_from_email(email)
  return str(user.pk)

def get_users() -> str:
  return User.objects.to_json()

def delete_user(id) -> None:
  try:
    User.objects.get(id=id).delete()
  except DoesNotExist:
    raise UserDoesNotExist(f"User {id} does not exist.")

def update_user(email, user_data) -> str:
  user_db = get_user_from_email(email)
  user_db.update(**user_data)
  return str(user_db.pk)

def create_room(room) -> str:
  new_room = Room(**room)
  try:
    new_room.save()
  except NotUniqueError:
    raise RoomHasDuplicateNumberOrName(
      f"Room number {room['number']} or {room['name']} is already taken.")
  return str(new_room.pk)

def get_rooms():
  return Room.objects.to_json()

def get_room(room_num):
  try:
    return Room.objects.get(number=room_num)
  except:
    raise RoomDoesNotExist(f"Room {room_num} does not exist.")

def delete_room(room_num) -> None:
  get_room(room_num).delete()

def create_timelog(timelog) -> str:
  new_timelog = Timelog(**timelog)
  new_timelog.save()
  return str(new_timelog.pk)

def get_timelogs_from_room_number(room_num: int) -> list:
  get_room(room_num)
  timelogs_query = Timelog.objects(room_number=room_num).exclude('id').all()
  
  timelogs = []
  for timelog in timelogs_query:
    timelogs.append(timelog.to_mongo().to_dict())
  
  return timelogs
