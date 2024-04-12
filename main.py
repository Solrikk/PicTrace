from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
import aiohttp
import hashlib
import os
from image_utils import find_similar_images, download_image
from database import init_db, add_image_to_db

app = FastAPI()

init_db()


@app.get("/", response_class=HTMLResponse)
async def upload_form():
  with open('templates/upload_form.html', 'r') as file:
    html_content = file.read()
  return HTMLResponse(content=html_content)


@app.post("/upload/")
async def create_upload_file(file: UploadFile = File(...)):
  contents = await file.read()
  image_hash = hashlib.sha256(contents).hexdigest()
  file_path = f'uploads/{image_hash}.jpg'
  os.makedirs(os.path.dirname(file_path), exist_ok=True)
  with open(file_path, 'wb') as f:
    f.write(contents)
  add_image_to_db(file_path, image_hash)
  similar_images = await find_similar_images(file_path)
  return {
      "message": "File uploaded successfully",
      "filename": file.filename,
      "hash": image_hash,
      "similar_images": similar_images
  }


@app.post("/upload_from_url/")
async def upload_from_url(image_url: str = Form(...)):
  async with aiohttp.ClientSession() as session:
    async with session.get(image_url) as response:
      if response.status == 200:
        contents = await response.read()
        image_hash = hashlib.sha256(contents).hexdigest()
        file_path = f'uploads/{image_hash}.jpg'
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as f:
          f.write(contents)
        add_image_to_db(file_path, image_hash)
        similar_images = await find_similar_images(file_path)
        return {
            "message": "File uploaded successfully from URL",
            "filename": os.path.basename(file_path),
            "hash": image_hash,
            "similar_images": similar_images
        }
      else:
        return {"message": "Failed to download image from URL"}
