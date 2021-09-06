import os
import shutil

from fastapi import UploadFile

from exceptions import ImageDoesNotExist

IMAGE_FOLDER = "images/"

def get_image(id: str) -> str:
  image_folder_path = os.path.join(os.getcwd(), IMAGE_FOLDER)
  files = os.listdir(image_folder_path)

  for file in files:
    if id in file:
      image_file_path = os.path.join(image_folder_path, file)
      return image_file_path

  raise ImageDoesNotExist(f"Image does not exist for user.")

def save_image(image: UploadFile, image_name: str) -> str:
  file_extension = "." + image.filename.split(".")[-1]
  full_image_name = image_name + file_extension

  image_path = os.path.join(os.getcwd(), IMAGE_FOLDER + full_image_name)
  with open(image_path, "wb+") as file_object:
    shutil.copyfileobj(image.file, file_object)

  return full_image_name
