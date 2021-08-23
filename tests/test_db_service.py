from datetime import date

import pytest
from mongoengine import connect, disconnect

from schemas import User
from services.db_service import DBService
from exceptions import EmailIsAlreadyTaken

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
