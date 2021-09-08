import json
from datetime import date

import pytest
from mongoengine import connect, disconnect
from mongoengine.errors import DoesNotExist

import services.db_service as db
from schemas import User, Room
from exceptions import (EmailIsAlreadyTaken, RoomDoesNotExist,
  RoomHasDuplicateNumberOrName, UserDoesNotExist)

@pytest.fixture
def user():
  return {
    'email': "ryan@gmail.com",
    'password': "password",
    'first_name': "Ryan",
    'last_name': "Dineros",
    'contact_number': "09294137458",
    'birthday': date(1996, 9, 16)
  }

@pytest.fixture
def room():
  return {
    'number': 16,
    'name': "My Room"
  }

@pytest.fixture(autouse=True)
def setup_db():
  connect("mongoenginetest", host="mongomock://localhost")

  yield

  disconnect()

def test__create_user__user_is_created(user, setup_db):
  id = db.create_user(user)

  assert User.objects.get(id=id)

def test__create_user__raise_if_email_is_taken(user, setup_db):
  db.create_user(user)
  
  with pytest.raises(EmailIsAlreadyTaken):
    db.create_user(user)

def test__delete_user__user_is_deleted(user, setup_db):
  other_user = user.copy()
  other_user['email'] = "ramses@yahoo.com"
  db.create_user(other_user)

  id = db.create_user(user)

  db.delete_user(id)

  with pytest.raises(DoesNotExist):
    User.objects.get(id=id)

def test__delete_user__nonexistent_user_raises_exception(user, setup_db):
  with pytest.raises(UserDoesNotExist):
    db.delete_user("6123361c16cce88331c423b1")

def test__create_room__creates_room(room, setup_db):
  id = db.create_room(room)

  assert Room.objects.get(id=id)

def test__create_room__raise_if_room_number_is_taken(room, setup_db):
  db.create_room(room)

  with pytest.raises(RoomHasDuplicateNumberOrName):
    db.create_room(room)

def test__get_rooms__gets_all_rooms(room, setup_db):
  db.create_room(room)
  rooms = json.loads(db.get_rooms())

  assert len(rooms) > 0
  assert rooms[0]['number'] == room['number']

def test__delete_room__room_is_deleted(room, setup_db):
  other_room = {
    'number': 1,
    'name': 'Other Room'
  }

  db.create_room(other_room)
  db.create_room(room)

  db.delete_room(room['number'])

  with pytest.raises(DoesNotExist):
    Room.objects.get(number=room['number'])

def test__delete_room__nonexistent_room_raises_exception(setup_db):
  with pytest.raises(RoomDoesNotExist):
    db.delete_room(16)
