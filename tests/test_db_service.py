from datetime import date

import pytest
from mongoengine import connect, disconnect
from mongoengine.errors import DoesNotExist

from schemas import User
from services.db_service import DBService
from exceptions import EmailIsAlreadyTaken, UserDoesNotExist

@pytest.fixture
def user():
  return {
    'email': "ryan@gmail.com",
    'first_name': "Ryan",
    'last_name': "Dineros",
    'contact_number': "09294137458",
    'birthday': date(1996, 9, 16)
  }

@pytest.fixture
def db_service():
  return DBService()

@pytest.fixture(autouse=True)
def setup_mongodb():
  connect("mongoenginetest", host="mongomock://localhost")

  yield

  disconnect()

def test__create_user__user_is_created(user, db_service, setup_mongodb):
  id = db_service.create_user(user)

  assert User.objects.get(id=id)

def test__create_user__raise_if_email_is_taken(user, db_service, setup_mongodb):
  db_service.create_user(user)
  
  with pytest.raises(EmailIsAlreadyTaken):
    db_service.create_user(user)

def test__delete_user__user_is_deleted(user, db_service, setup_mongodb):
  other_user = user.copy()
  other_user['email'] = "ramses@yahoo.com"
  db_service.create_user(other_user)

  id = db_service.create_user(user)

  db_service.delete_user(id)

  with pytest.raises(DoesNotExist):
    User.objects.get(id=id)

def test__delete_user__nonexistent_user_raises_exception(user, db_service, setup_mongodb):
  with pytest.raises(UserDoesNotExist):
    db_service.delete_user("6123361c16cce88331c423b1")
