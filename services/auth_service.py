from datetime import datetime, timedelta
from typing import Optional

import bcrypt
from jose import jwt
from jose.exceptions import JWTError
from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer

from models import TokenData

SECRET_KEY = "0e520a7811280d5782872ce234dace277a3e652f306aeade5635a3dae3b5bb43"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

def generate_hashed_password(password: str):
  return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password: str, hashed_password: str):
  return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def authenticate_user(get_user_func, username, password):
  user = get_user_func(username)
  if not user:
    return False

  is_correct_pwd = verify_password(password, user.password)
  if not is_correct_pwd:
    return False
  
  return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
  to_encode = data.copy()

  if expires_delta:
    expire = datetime.utcnow() + expires_delta
  else:
    expire = datetime.utcnow() + timedelta(minutes=15)

  to_encode.update({'exp': expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

async def get_token_data(token: str = Depends(oauth2_scheme)):
  credentials_exception = HTTPException(
    status_code = 401,
    detail = "Could not validate credentials.",
    headers = { 'WWW-Authenticate': "Bearer" }
  )

  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get('sub')
    if username is None:
      raise credentials_exception
    token_data = TokenData(username=username)
  except JWTError:
    raise credentials_exception
  
  return token_data
