import aiohttp
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import asyncio
from aiohttp import ClientError

UNSPLASH_ACCESS_KEY = "YOUR_UNSPLASH_ACCESS_KEY"
UNSPLASH_SEARCH_URL = "https://api.unsplash.com/search/photos"

async def download_image(session, url):
  async with session.get(url) as response:
    if response.status == 200:
      image_data = await response.read()
      image_array = np.frombuffer(image_data, np.uint8)
      image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
      return image
  raise Exception('Image download failed')

async def get_image_urls_from_unsplash(session, query):
  params = {
      "client_id": UNSPLASH_ACCESS_KEY,
      "query": query,
      "per_page": 5  # Adjust the number of images to retrieve
  }
  async with session.get(UNSPLASH_SEARCH_URL, params=params) as response:
    if response.status == 200:
      data = await response.json()
      return [result['urls']['regular'] for result in data['results']]
  return []

async def process_image(session, image_entry, target_image):
  try:
    image_urls = await get_image_urls_from_unsplash(session, image_entry["query"])
    for image_url in image_urls:
      current_image = await download_image(session, image_url)
      optimal_size = max(max(target_image.shape[:2]),
                         max(current_image.shape[:2]))
      optimal_size = min(1024, optimal_size)
      target_image_resized = cv2.resize(target_image,
                                        (optimal_size, optimal_size))
      current_image_resized = cv2.resize(current_image,
                                         (optimal_size, optimal_size))
      target_gray = cv2.cvtColor(target_image_resized, cv2.COLOR_BGR2GRAY)
      current_gray = cv2.cvtColor(current_image_resized, cv2.COLOR_BGR2GRAY)
      ssim_index = ssim(target_gray, current_gray)
      orb = cv2.ORB_create(nfeatures=500)
      target_keypoints, target_descriptors = orb.detectAndCompute(
          target_gray, None)
      current_keypoints, current_descriptors = orb.detectAndCompute(
          current_gray, None)
      if target_descriptors is None or current_descriptors is None:
        return (0, image_url)
      index_params = dict(algorithm=6,
                          table_number=6,
                          key_size=12,
                          multi_probe_level=1)
      search_params = dict(checks=50)
      flann = cv2.FlannBasedMatcher(index_params, search_params)
      matches = flann.knnMatch(target_descriptors, current_descriptors, k=2)
      good_matches = [m for m, n in matches if m.distance < 0.75 * n.distance]
      feature_score = len(good_matches) / float(len(target_keypoints))
      target_hist = cv2.calcHist([target_image_resized], [0, 1, 2], None,
                                 [32, 32, 32], [0, 256, 0, 256, 0, 256])
      current_hist = cv2.calcHist([current_image_resized], [0, 1, 2], None,
                                  [32, 32, 32], [0, 256, 0, 256, 0, 256])
      cv2.normalize(target_hist, target_hist)
      cv2.normalize(current_hist, current_hist)
      hist_score = cv2.compareHist(target_hist, current_hist,
                                   cv2.HISTCMP_CORREL)
      final_score = (feature_score + ssim_index + hist_score) / 3
      return (final_score, image_url)
  except Exception as e:
    print(f"Failed to process image due to {e}")
    return (0, "")

async def find_similar_images(file_path):
  target_image = cv2.imread(file_path)
  search_queries = ["nature", "cities", "animals", "tech", "space"]  # Example queries
  async with aiohttp.ClientSession() as session:
    tasks = [
        process_image(session, {"query": query}, target_image) for query in search_queries
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
