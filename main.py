from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import HTMLResponse, FileResponse
import aiohttp
import hashlib
import os
from typing import List
from skimage.metrics import structural_similarity as ssim
import cv2
import numpy as np
import json
import asyncio

app = FastAPI()


def load_db():
  try:
    with open("images.json", "r") as file:
      return json.load(file)
  except FileNotFoundError:
    return []


def save_db(data):
  with open("images.json", "w") as file:
    json.dump(data, file, indent=4)


def init_db():
  db_data = load_db()
  if not isinstance(db_data, list):
    db_data = []
    save_db(db_data)


def get_image_hash(image):
  hash = hashlib.sha256(image).hexdigest()
  return hash


def add_image_to_db(file_path, image_hash):
  db_data = load_db()
  if isinstance(db_data, list):
    db_data.append({"file_path": file_path, "hash": image_hash})
    save_db(db_data)


async def download_image(url: str) -> np.ndarray:
  async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
      if response.status == 200:
        image_data = await response.read()
        image_array = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        return image
  raise Exception('Image download failed')


async def process_image(image_entry: dict, target_image: np.ndarray) -> tuple:
  try:
    current_image = await download_image(image_entry["url"])
    target_image_resized = cv2.resize(target_image, (256, 256))
    current_image_resized = cv2.resize(current_image, (256, 256))
    target_gray = cv2.cvtColor(target_image_resized, cv2.COLOR_BGR2GRAY)
    current_gray = cv2.cvtColor(current_image_resized, cv2.COLOR_BGR2GRAY)
    ssim_index = ssim(target_gray, current_gray)
    orb = cv2.ORB_create()
    target_keypoints, target_descriptors = orb.detectAndCompute(
        target_gray, None)
    current_keypoints, current_descriptors = orb.detectAndCompute(
        current_gray, None)
    if target_descriptors is None or current_descriptors is None:
      return (0, image_entry["url"])
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(target_descriptors, current_descriptors)
    matches = sorted(matches, key=lambda x: x.distance)
    orb_score = len(matches) / float(len(target_keypoints))
    final_score = (orb_score + ssim_index) / 2
    return (final_score, image_entry["url"])
  except Exception as e:
    print(f"Failed to process image {image_entry['url']} due to {e}")
    return (0, image_entry["url"])


async def find_similar_images(file_path: str) -> List[str]:
  db_data = load_db()
  target_image = cv2.imread(file_path)
  tasks = [
      process_image(entry, target_image) for entry in db_data if "url" in entry
  ]
  results = await asyncio.gather(*tasks)
  valid_results = filter(lambda x: x[0] > 0, results)
  sorted_results = sorted(valid_results, key=lambda x: x[0], reverse=True)[:5]
  seen_urls = set()
  top_similar_images = []
  for result in sorted_results:
    if result[1] not in seen_urls:
      top_similar_images.append(result[1])
      seen_urls.add(result[1])
  return top_similar_images


@app.get("/", response_class=HTMLResponse)
async def upload_form():
  with open("upload_form.html", "r") as file:
    form_content = file.read()
  return HTMLResponse(content=form_content, status_code=200)


@app.post("/upload/")
async def create_upload_file(file: UploadFile = File(...)):
  contents = await file.read()
  image_hash = get_image_hash(contents)
  file_path = f'uploads/{file.filename}'
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
        image_hash = get_image_hash(contents)
        file_path = f'uploads/{hashlib.sha256(contents).hexdigest()}.jpg'
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
