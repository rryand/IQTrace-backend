import bcrypt

class AuthService:
  def generate_hashed_password(self, password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())