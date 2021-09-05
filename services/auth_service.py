import bcrypt

class AuthService:
  def generate_hashed_password(self, password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
  
  def verify_password(self, password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))