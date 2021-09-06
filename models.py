from datetime import date
from pydantic import BaseModel

class User(BaseModel):
  email: str

class UserOut(User):
  first_name: str
  last_name: str
  contact_number: str
  birthday: date

class UserIn(UserOut):
  password: str

class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  username: str
