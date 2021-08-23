from datetime import date
from pydantic import BaseModel

class User(BaseModel):
  email: str
  first_name: str
  last_name: str
  contact_number: str
  birthday: date

class UserIn(User):
  password: str

class UserOut(User):
  id: str
