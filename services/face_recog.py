import numpy

import face_recognition as fr
from PIL import Image

from exceptions import CannotReadFace, HasMoreThanOneFace

def load_image(image_path: str):
  return fr.load_image_file(image_path)

def generate_face_encoding(image) -> numpy.ndarray:
  encodings = fr.face_encodings(image)
  
  if len(encodings) > 1:
    raise HasMoreThanOneFace(
      f"{image} has been detected to have more than one face.")
  elif len(encodings) == 0:
    raise CannotReadFace(f"Can't read face in image.")
  
  return encodings[0]

def compare_faces(known_encoding: list, unknown_encoding: list, tolerance: float = 0.6) -> bool:
  distance = fr.face_distance([numpy.array(known_encoding)], unknown_encoding)[0]
  print(f"Face distance: {distance} | Tolerance: {tolerance}")

  is_similar = True if distance <= tolerance else False

  if is_similar:
    return True
  else:
    return False

def resize_image(image_name: str, max_size: tuple = (500, 500)) -> str:
  image = Image.open(image_name)
  image.thumbnail(max_size)
  width, height = image.size

  if height < width:
    image = image.rotate(90, expand=True)

  image.save("resized.jpg")
  return "resized.jpg"

