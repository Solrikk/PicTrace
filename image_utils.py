import aiohttp
import cv2
import numpy as np
from database import add_image_to_db, load_db
from skimage.metrics import structural_similarity as ssim
import asyncio


async def download_image(session: aiohttp.ClientSession,
                         url: str) -> np.ndarray:
  async with session.get(url) as response:
    if response.status == 200:
      image_data = await response.read()
      image_array = np.frombuffer(image_data, np.uint8)
      image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
      return image
  raise Exception('Image download failed')


async def process_image(session: aiohttp.ClientSession, image_entry: dict,
                        target_image: np.ndarray) -> tuple:
  try:
    current_image = await download_image(session, image_entry["url"])
    optimal_size = max(min(target_image.shape[:2]),
                       min(current_image.shape[:2]))
    optimal_size = min(512, optimal_size)  
    target_image_resized = cv2.resize(target_image,
                                      (optimal_size, optimal_size))
    current_image_resized = cv2.resize(current_image,
                                       (optimal_size, optimal_size))
    # Convert to grayscale for SSIM and ORB computations
    target_gray = cv2.cvtColor(target_image_resized, cv2.COLOR_BGR2GRAY)
    current_gray = cv2.cvtColor(current_image_resized, cv2.COLOR_BGR2GRAY)
    # Computing similarity using SSIM
    ssim_index = ssim(target_gray, current_gray)
    # Using ORB for feature-based comparison
    orb = cv2.ORB_create(nfeatures=500)
    target_keypoints, target_descriptors = orb.detectAndCompute(
        target_gray, None)
    current_keypoints, current_descriptors = orb.detectAndCompute(
        current_gray, None)

    if target_descriptors is None or current_descriptors is None:
      return (0, image_entry["url"])

    # Using FLANN for better matching
    index_params = dict(algorithm=6,
                        table_number=6,
                        key_size=12,
                        multi_probe_level=1)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(target_descriptors, current_descriptors, k=2)

    # Ratio test as per Lowe's paper
    good_matches = []
    for m, n in matches:
      if m.distance < 0.75 * n.distance:
        good_matches.append(m)
    feature_score = len(good_matches) / float(len(target_keypoints))

    # Histogram comparison for color similarity
    target_hist = cv2.calcHist([target_image_resized], [0, 1, 2], None,
                               [8, 8, 8], [0, 256, 0, 256, 0, 256])
    current_hist = cv2.calcHist([current_image_resized], [0, 1, 2], None,
                                [8, 8, 8], [0, 256, 0, 256, 0, 256])
    cv2.normalize(target_hist, target_hist)
    cv2.normalize(current_hist, current_hist)
    hist_score = cv2.compareHist(target_hist, current_hist, cv2.HISTCMP_CORREL)

    final_score = (feature_score + ssim_index + hist_score) / 3

    return (final_score, image_entry["url"])
  except Exception as e:
    print(f"Failed to process image {image_entry['url']} due to {e}")
    return (0, image_entry["url"])


async def find_similar_images(file_path: str) -> list:
  db_data = load_db()
  target_image = cv2.imread(file_path)
  async with aiohttp.ClientSession() as session:
    tasks = [
        process_image(session, entry, target_image) for entry in db_data
        if "url" in entry
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
