import json
from datetime import timedelta

import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

import services.auth_service as auth
from services.db_service import DBService
from models import UserOut, UserIn, Token, TokenData
from exceptions import EmailIsAlreadyTaken, UserDoesNotExist

ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

db = DBService()
db.initialize_db()

@app.get('/')
async def root():
  return {'message': "hello world!"}

@app.get('/users')
async def get_users(token_data: TokenData = Depends(auth.get_token_data)):
  users = db.get_users()
  return json.loads(users)

@app.post('/users/register', response_model=UserOut)
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
      'id': str(id),
      **new_user.dict(),
    }
  return response

@app.post('/users/login', response_model=Token)
async def login(credentials: OAuth2PasswordRequestForm = Depends()):
  user = auth.authenticate_user(db.get_user_from_email, credentials.username, credentials.password)
  if not user:
    raise HTTPException(status_code=400, detail="Incorrect email or password")

  access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = auth.create_access_token(
    data = { 'sub': user.email },
    expires_delta = access_token_expires
  )

  return { 'access_token': access_token, 'token_type': "bearer" }

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

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000)
