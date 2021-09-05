from datetime import date
from pydantic import BaseModel

class User(BaseModel):
  email: str

class UserCredentials(User):
  password: str

class UserOut(User):
  first_name: str
  last_name: str
  contact_number: str
  birthday: date

class UserIn(UserOut):
  password: str
