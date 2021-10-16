from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel

class User(BaseModel):
  email: str

class UserOut(User):
  first_name: str
  last_name: str
  contact_number: str
  birthday: date
  survey: Optional[list] = []
  is_admin: bool = False
  face_encoding: Optional[list] = None

class UserIn(UserOut):
  password: str

class Room(BaseModel):
  number: int
  name: Optional[str] = None

class Timelog(BaseModel):
  user_email: str
  room_number: int
  timestamp: datetime

class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  username: str
