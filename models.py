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
  survey: Optional[dict] = {}

class UserIn(UserOut):
  password: str

class Room(BaseModel):
  number: int
  name: Optional[str] = None

class Timelog(BaseModel):
  user_id: str
  room_number: int
  timestamp: datetime

class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  username: str
