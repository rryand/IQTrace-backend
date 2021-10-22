import json
from datetime import timedelta
import shutil

import uvicorn
from fastapi import FastAPI, HTTPException, Depends, File, UploadFile
from fastapi.security import OAuth2PasswordRequestForm

import settings
import services.face_recog as face_recog
import services.auth_service as auth
import services.db_service as db
import services.mail_service as mail
from models import UserOut, UserIn, Token, TokenData, Room, Timelog
from exceptions import (CannotReadFace, EmailIsAlreadyTaken, HasMoreThanOneFace, RoomHasDuplicateNumberOrName,
  UserDoesNotExist, RoomDoesNotExist, FileTypeNotAllowed, VerificationAlreadyExists, VerificationItemDoesNotExist)

app = FastAPI()

db.initialize_db()

TEMP_FILE = "destination.jpg"

async def verify_image_file_type(file: UploadFile = File(...)):
  if file.content_type not in settings.ALLOWED_MIME_TYPES:
    raise FileTypeNotAllowed(f"File type {file.content_type} is not allowed.")
  else:
    return file

@app.get('/')
async def root():
  return {'message': "hello world!"}

@app.get('/users', response_model=UserOut)
async def get_users(email: str):
  user = db.get_user_from_email(email)
  return user.to_mongo().to_dict()

@app.put('/users')
async def update_user(email: str, user: UserOut):
  user_data = user.dict()
  user_data.pop('email')
  user_data.pop('is_admin')

  # TODO: add temp check and temp alert

  id = db.update_user(email, user_data)
  return { 'id': id, **user.dict() }

@app.patch('/user-temp')
async def update_user_temp(email: str, temp: float):
  # TODO: add temp check and temp alert

  id = db.update_user(email, {'temp': temp})
  return {'temp': temp}

@app.get('/users/all')
async def get_users(token_data: TokenData = Depends(auth.get_token_data)):
  users = db.get_users()
  return json.loads(users)

@app.post('/users/register', response_model=UserOut, status_code=201)
async def register_user(user: UserIn):
  try:
    user.is_admin = False
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

@app.get('/users/me', response_model=UserOut)
async def get_current_user(token_data: TokenData = Depends(auth.get_token_data)):
  user = db.get_user_from_email(token_data.username)
  if not user:
    raise HTTPException(status_code=404, detail="User not found.")
  
  return user.to_mongo().to_dict()

@app.put('/users/me')
async def update_current_user(user: UserOut, token_data: TokenData = Depends(auth.get_token_data)):
  user_data = user.dict()
  user_data.pop('email')
  user_data.pop('is_admin')
  id = db.update_user(token_data.username, user_data)
  return { 'id': id, **user.dict() }

@app.patch('/users/image-encoding')
def update_user_encoding(email: str, file: UploadFile = File(...)):
  try:
    with open(TEMP_FILE, "wb") as buffer:
      shutil.copyfileobj(file.file, buffer)

    resized_image = face_recog.resize_image(TEMP_FILE)
    image = face_recog.load_image(resized_image)
    face_encoding = face_recog.generate_face_encoding(image)
    
    encoding_data = { 'face_encoding': face_encoding.tolist() }
    db.update_user(email, encoding_data)
  except (HasMoreThanOneFace, CannotReadFace) as err:
    raise HTTPException(status_code=400, detail=str(err))
  except Exception as err:
    raise HTTPException(status_code=500, detail=str(err))

  return encoding_data

@app.post('/users/me/image-encoding/compare')
async def verify_image(email: str, image: UploadFile = Depends(verify_image_file_type)):
  user = db.get_user_from_email(email)

  uploaded_image = face_recog.load_image(image.file)
  uploaded_face_encoding = face_recog.generate_face_encoding(uploaded_image)

  is_similar = face_recog.compare_faces(user.face_encoding, uploaded_face_encoding)
  return { 'is_similar': is_similar }

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

@app.get('/rooms')
def get_rooms():
  rooms = db.get_rooms()
  return json.loads(rooms)

@app.post('/rooms', status_code=201)
def create_room(room: Room):
  try:
    id = db.create_room({'number': room.number, 'name': room.name})
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

@app.post('/verification')
def send_verification_email(email: str):
  email = email.replace(' ', '+').strip()
  try:
    pk = db.create_verification(email)
    mail.send_verification_email(email, pk)
  except VerificationAlreadyExists as err:
    raise HTTPException(status_code=403, detail=str(err))

  return {
    'email': email,
    'message': "Email verification sent.",
  }

# NOTE: Should return HTML page and 
#       POST verification from there
@app.get('/verification/{verification_id}')
def verify_email(verification_id: str):
  try:
    email = db.delete_verification(verification_id)
    db.update_user(email, {'is_verified': True})
    response = {
      'email': email,
      'is_verified': True,
      'message': "Email verified."
    }
  except VerificationItemDoesNotExist as err:
    response = {'message': str(err)}

  return response
  

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000)
