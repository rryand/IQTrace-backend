from datetime import date
from typing import Optional

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

class Room(BaseModel):
  number: int
  name: Optional[str] = None

class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  username: str
