from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import HTMLResponse, FileResponse
import aiohttp
import hashlib
import os
from typing import List
from skimage.metrics import structural_similarity as ssim
import cv2
import numpy as np
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
import sqlite3

app = FastAPI()

DB_FILE = 'images.db'

def init_db():
  conn = sqlite3.connect(DB_FILE)
  cursor = conn.cursor()
  cursor.execute('''CREATE TABLE IF NOT EXISTS images 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT, file_path TEXT, hash TEXT)''')
  conn.commit()
  conn.close()

def load_db():
  conn = sqlite3.connect('images.db')
  cursor = conn.cursor()
  cursor.execute("SELECT id, url FROM images")
  db_data = cursor.fetchall()
  conn.close()
  return [{"id": row[0], "url": row[1]} for row in db_data]


def add_image_to_db(file_path, image_hash):
  conn = sqlite3.connect(DB_FILE)
  cursor = conn.cursor()
  cursor.execute("INSERT INTO images (url, hash) VALUES (?, ?)", (file_path, image_hash))
  conn.commit()
  conn.close()


def get_image_hash(image):
  hash = hashlib.sha256(image).hexdigest()
  return hash


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
  tasks = []

  for entry in db_data:
    if "url" in entry:
      task = asyncio.create_task(process_image(entry, target_image))
      tasks.append(task)

  results = []

  for completed_task in asyncio.as_completed(tasks):
    result = await completed_task
    results.append(result)

  valid_results = [result for result in results if result[0] > 0]
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
  return FileResponse('templates/upload_form.html')


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


init_db()
