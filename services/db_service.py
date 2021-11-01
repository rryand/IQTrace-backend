from mongoengine import connect
from mongoengine.queryset.visitor import Q
from mongoengine.errors import NotUniqueError, DoesNotExist

from schemas import User, Room, Timelog, Verification
from exceptions import (EmailIsAlreadyTaken, RoomDoesNotExist,
  RoomHasDuplicateNumberOrName, UserDoesNotExist, 
  VerificationAlreadyExists, VerificationItemDoesNotExist)


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

def get_user_from_email(email: str) -> User:
  email = email.replace(' ', '+').strip()
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

def get_users_with_symptoms() -> str:
  query = {}
  query2 = {}
  query['survey__exists'] = True
  query['survey__not__size'] = 0
  query2['temp__exists'] = True
  query2['temp__gte'] = 38.0
  queried_users = User.objects(Q(**query) | Q(**query2))

  users = []
  for user in queried_users:
    users.append(user.to_mongo().to_dict())

  return users

def delete_user(id) -> None:
  try:
    User.objects.get(id=id).delete()
  except DoesNotExist:
    raise UserDoesNotExist(f"User {id} does not exist.")

def update_user(email:str, user_data) -> str:
  email = email.replace(' ', '+').strip()
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

def get_timelogs() -> list:
  rooms = Room.objects

  timelogs = {}
  for room in rooms:
    room_timelogs = Timelog.objects(room_number=room.number)

    timelogs_list = []
    for room_timelog in room_timelogs:
      log = room_timelog.to_mongo().to_dict()
      log['timestamp'] = log['timestamp'].strftime("%Y-%m-%dT%H:%M:%S")
      timelogs_list.append(log)

    timelogs[room.number] = timelogs_list
  
  return timelogs


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

def create_verification(email: str) -> str:
  try:
    new_verification = Verification(email=email)
    new_verification.save()
  except NotUniqueError:
    raise VerificationAlreadyExists("Verification already exists")
  return str(new_verification.pk)

def delete_verification(pk: str) -> str:
  try:
    verification = Verification.objects.get(id=pk)
    email = verification.email
    verification.delete()
  except DoesNotExist:
    raise VerificationItemDoesNotExist("Email may already be verified.")
  return email
