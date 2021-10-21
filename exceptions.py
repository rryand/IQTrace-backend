class EmailIsAlreadyTaken(Exception):
  pass

class RoomHasDuplicateNumberOrName(Exception):
  pass

class UserDoesNotExist(Exception):
  pass

class RoomDoesNotExist(Exception):
  pass

class HasMoreThanOneFace(Exception):
  pass

class CannotReadFace(Exception):
  pass

class FileTypeNotAllowed(Exception):
  pass

class VerificationItemDoesNotExist(Exception):
  pass
