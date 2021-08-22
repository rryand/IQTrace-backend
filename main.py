import json

import uvicorn
from fastapi import FastAPI

from models import User as PyUser
from services.db_service import DBService
from exceptions import EmailIsAlreadyTaken

app = FastAPI()

db = DBService()
db.initialize_db()

@app.get('/')
async def root():
  return {'message': "hello world!"}

@app.get('/users')
async def get_users():
  users = db.get_users()
  return json.loads(users)

@app.post('/users')
async def create_user(user: PyUser):
  try:
    id = db.create_user(user.dict())
  except EmailIsAlreadyTaken as err:
    response = { 'message': str(err) }
  else:
    response = {
      'id': str(id),
      **user.dict(),
    }
  return response

@app.delete('/users')
async def delete_user():
  db.delete_user()
  return { 'message': "User deleted" }

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000)
