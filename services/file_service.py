import os
import shutil

from fastapi import UploadFile

def save_image(image: UploadFile, image_name: str):
  file_extension = "." + image.filename.split(".")[-1]
  full_image_name = image_name + file_extension
  
  current_path = os.getcwd()
  image_path = os.path.join(current_path, f"images/{full_image_name}")
  with open(image_path, "wb+") as file_object:
    shutil.copyfileobj(image.file, file_object)

  return full_image_name
