from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import hashlib
import os
from image_utils import find_similar_images
from database import init_db, add_image_to_db

app = FastAPI()

init_db()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def upload_form():
  with open('templates/upload_form.html', 'r') as file:
    html_content = file.read()
  return HTMLResponse(content=html_content)


@app.post("/upload/", response_class=JSONResponse)
async def create_upload_file(file: UploadFile = File(...)):
  contents = await file.read()
  image_hash = hashlib.sha256(contents).hexdigest()
  file_path = f'uploads/{image_hash}.jpg'
  os.makedirs(os.path.dirname(file_path), exist_ok=True)
  with open(file_path, 'wb') as f:
    f.write(contents)
  add_image_to_db(file_path, image_hash)
  similar_images = await find_similar_images(file_path)

  response_data = {
      "message": "File uploaded successfully",
      "filename": image_hash,
      "similar_images": similar_images
  }

  return JSONResponse(content=response_data)


@app.get("/uploads/{image_hash}.jpg", response_class=FileResponse)
async def serve_uploaded_image(image_hash: str):
  file_path = f'uploads/{image_hash}.jpg'
  return FileResponse(file_path)
