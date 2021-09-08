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
  user = User.objects.get(email=email)
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

def delete_room(room_num) -> None:
  try:
    Room.objects.get(number=room_num).delete()
  except DoesNotExist:
    raise RoomDoesNotExist(f"Room {room_num} does not exist.")

def create_timelog(timelog):
  new_timelog = Timelog(**timelog)
  new_timelog.save()
  return str(new_timelog.pk)
