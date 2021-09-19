import numpy

import face_recognition as fr

from exceptions import HasMoreThanOneFace

def load_image(image_path: str):
  return fr.load_image_file(image_path)

def generate_face_encoding(image) -> list:
  encodings = fr.face_encodings(image)
  
  if len(encodings) > 1:
    raise HasMoreThanOneFace(
      f"{image} has been detected to have more than one face.")
  
  return encodings[0].tolist()

def compare_faces(known_encoding: list, unknown_encoding: list) -> bool:
  is_similar = fr.compare_faces(
    [numpy.array(known_encoding)],
    numpy.array(unknown_encoding)
  )[0]

  if is_similar:
    return True
  else:
    return False
