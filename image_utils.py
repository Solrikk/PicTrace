import aiohttp
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing import image
from database import load_db
import asyncio
from sklearn.metrics.pairwise import cosine_similarity

base_model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
model = Model(inputs=base_model.input, outputs=base_model.output)


async def download_image(session, url):
  async with session.get(url) as response:
    if response.status == 200:
      image_data = await response.read()
      image_array = np.frombuffer(image_data, np.uint8)
      img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
      return img
  raise Exception('Image download failed')


def extract_features(img):
  img = cv2.resize(img, (224, 224))
  img_array = image.img_to_array(img)
  img_array = np.expand_dims(img_array, axis=0)
  img_array = preprocess_input(img_array)
  features = model.predict(img_array)
  return features


async def compare_images(session, image_url, target_features):
  try:
    current_image = await download_image(session, image_url)
    current_features = extract_features(current_image)
    similarity = cosine_similarity(current_features, target_features)
    return (similarity[0][0], image_url)
  except Exception as e:
    print(f"Failed to compare image {image_url} due to {e}")
    return (0, image_url)


async def find_similar_images(file_path):
  db_data = load_db()
  target_image = cv2.imread(file_path)
  target_features = extract_features(target_image)
  async with aiohttp.ClientSession() as session:
    tasks = [
        compare_images(session, entry["url"], target_features)
        for entry in db_data if "url" in entry
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
