import json
from datetime import timedelta

import uvicorn
from fastapi import FastAPI, HTTPException, Depends, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordRequestForm

import settings
import services.auth_service as auth
import services.file_service as file_service
import services.db_service as db
from models import UserOut, UserIn, Token, TokenData, Room, Timelog
from exceptions import (EmailIsAlreadyTaken, RoomHasDuplicateNumberOrName,
  ImageDoesNotExist, UserDoesNotExist, RoomDoesNotExist)

app = FastAPI()

db.initialize_db()

@app.get('/')
async def root():
  return {'message': "hello world!"}

@app.get('/users')
async def get_users(token_data: TokenData = Depends(auth.get_token_data)):
  users = db.get_users()
  return json.loads(users)

@app.post('/users/register', response_model=UserOut, status_code=201)
async def register_user(user: UserIn):
  try:
    new_user = user.copy()
    new_user.password = auth.generate_hashed_password(user.password)
    id = db.create_user(new_user.dict())
  except EmailIsAlreadyTaken as err:
    raise HTTPException(status_code= 403, detail=str(err))
  except Exception as err:
    raise HTTPException(status_code=500, detail=str(err))
  else:
    response = {
      'id': id,
      **new_user.dict(),
    }
  return response

@app.post('/users/login', response_model=Token)
async def login(credentials: OAuth2PasswordRequestForm = Depends()):
  user = auth.authenticate_user(db.get_user_from_email, credentials.username, credentials.password)
  if not user:
    raise HTTPException(status_code=400, detail="Incorrect email or password")

  access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = auth.create_access_token(
    data = { 'sub': user.email },
    expires_delta = access_token_expires
  )

  return { 'access_token': access_token, 'token_type': "bearer" }

@app.put('/users/me')
async def update_user(user: UserOut, token_data: TokenData = Depends(auth.get_token_data)):
  user_data = user.dict()
  user_data.pop('email')
  id = db.update_user(token_data.username, user_data)
  return { 'id': id, **user.dict() }

@app.delete('/users/{id}')
async def delete_user(id, token_data: TokenData = Depends(auth.get_token_data)):
  try:
    db.delete_user(id)
  except UserDoesNotExist as err:
    raise HTTPException(status_code=404, detail=str(err))
  except Exception as err:
    raise HTTPException(status_code=500, detail=str(err))
  else:
    response = { 'message': f"User {id} deleted" }
  return response

@app.get('/images')
async def get_image(token_data: TokenData = Depends(auth.get_token_data)):
  id = db.get_user_id_from_email(token_data.username)
  try:
    image_path = file_service.get_image(id)
  except ImageDoesNotExist as err:
    raise HTTPException(status_code=404, detail=str(err))
  except Exception as err:
    raise HTTPException(status_code=500, detail=str(err))
  else:
    return FileResponse(image_path)

@app.post('/images', status_code=201)
def save_image(file: UploadFile = File(...), token_data: TokenData = Depends(auth.get_token_data)):
  id = db.get_user_id_from_email(token_data.username)
  filename = file_service.save_image(file, image_name=id)

  return { 'filename': filename }

@app.get('/rooms')
def get_rooms():
  rooms = db.get_rooms()
  return json.loads(rooms)

@app.post('/rooms', status_code=201)
def create_room(room: Room):
  try:
    id = db.create_room(room.number, room.name)
  except RoomHasDuplicateNumberOrName as err:
    raise HTTPException(status_code=403, detail=str(err))
  except Exception as err:
    raise HTTPException(status_code=500, detail=str(err))
  else:
    response = {
      'id': id,
      **room.dict(),
    }
  return response

@app.delete('/rooms/{room_num}')
def delete_room(room_num: int):
  try:
    db.delete_room(room_num)
  except RoomDoesNotExist as err:
    raise HTTPException(status_code=404, detail=str(err))
  except Exception as err:
    raise HTTPException(status_code=500, detail=str(err))
  else:
    response = { 'message': f"Room {room_num} deleted." }
  return response

@app.get('/rooms/{room_num}/timelogs')
def get_room_timelogs(room_num: int):
  try:
    timelogs = db.get_timelogs_from_room_number(room_num)
  except RoomDoesNotExist as err:
    raise HTTPException(status_code=404, detail=str(err))
  return timelogs

@app.post('/timelog', status_code=201)
def create_timelog(timelog: Timelog):
  try:
    id = db.create_timelog(timelog.dict())
  except Exception as err:
    raise HTTPException(status_code=500, detail=str(err))
  else:
    response = {
      'id': id,
      **timelog.dict(),
    }
  return response

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000)
