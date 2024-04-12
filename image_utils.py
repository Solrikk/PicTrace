import aiohttp
import cv2
import numpy as np
from database import add_image_to_db, load_db
from skimage.metrics import structural_similarity as ssim
import asyncio


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


async def find_similar_images(file_path: str) -> list:
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
