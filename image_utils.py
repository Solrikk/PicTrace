import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
import cv2
import numpy as np
import asyncio
from concurrent.futures import ThreadPoolExecutor
from classification_utils import (is_architecture_image, is_aviation_image,
                                  is_background_image, is_animal_image,
                                  is_people_image, extract_features_batch)
from sklearn.metrics.pairwise import cosine_similarity

S3_BUCKET_NAME = 'YOUR_S3_BUCKET_NAME'
S3_REGION = 'YOUR_S3_REGION'
S3_ACCESS_KEY = 'YOUR_S3_ACCESS_KEY'
S3_SECRET_ACCESS_KEY = 'YOUR_S3_SECRET_ACCESS_KEY'
S3_ENDPOINT_URL = 'YOUR_S3_ENDPOINT_URL'

s3_client = boto3.client(
    's3',
    endpoint_url=S3_ENDPOINT_URL,
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_ACCESS_KEY,
    config=Config(region_name=S3_REGION, signature_version='s3v4'),
)


async def list_s3_images(folder=''):
  try:
    images = []
    continuation_token = None
    while True:
      if continuation_token:
        response = s3_client.list_objects_v2(
            Bucket=S3_BUCKET_NAME,
            ContinuationToken=continuation_token,
            Prefix=folder)
      else:
        response = s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME,
                                             Prefix=folder)
      images.extend([
          item['Key'] for item in response.get('Contents', [])
          if item['Key'].lower().endswith(('.jpg', '.jpeg', '.png'))
      ])
      if response.get('IsTruncated'):
        continuation_token = response.get('NextContinuationToken')
      else:
        break
    return images
  except ClientError as e:
    print(f"Failed to list images in S3 bucket: {e}")
    raise Exception('Listing images in S3 failed') from e


def download_image_from_s3(file_name):
  try:
    response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=file_name)
    image_data = response['Body'].read()
    image_array = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image
  except ClientError as e:
    print(f"Failed to download image {file_name} from S3: {e}")
    return None


async def compare_images(file_name, target_features, loop):
  try:
    current_image = download_image_from_s3(file_name)
    if current_image is None:
      return (0, "")
    with ThreadPoolExecutor() as pool:
      current_features = await loop.run_in_executor(
          pool, lambda: extract_features_batch([current_image]))
    if current_features.size == 0:
      return (0, "")
    similarity = cosine_similarity(current_features, target_features)
    if similarity[0][0] > 0.5:
      return (similarity[0][0], file_name)
  except Exception as e:
    print(f"Failed to compare image {file_name} due to {e}")
  return (0, "")


async def find_similar_images(file_path):
  loop = asyncio.get_event_loop()
  is_architecture = await is_architecture_image(file_path)
  is_aviation = await is_aviation_image(file_path)
  is_background = await is_background_image(file_path)
  is_animal = await is_animal_image(file_path)
  is_people = await is_people_image(file_path)

  if is_architecture:
    folder = "Architecture/"
  elif is_aviation:
    folder = "Aviation/"
  elif is_background:
    folder = "Backgrounds/"
  elif is_animal:
    folder = "Animals/"
  elif is_people:
    folder = "People/"
  else:
    folder = ''

  target_image = cv2.imread(file_path)
  if target_image is None:
    raise ValueError(
        f"Failed to read target image from file path: {file_path}")
  target_features = extract_features_batch([target_image])

  file_names = await list_s3_images(folder=folder)
  tasks = [
      compare_images(file_name, target_features, loop)
      for file_name in file_names
  ]
  results = await asyncio.gather(*tasks)

  valid_results = filter(lambda x: x[0] > 0, results)
  sorted_results = sorted(valid_results, key=lambda x: x[0], reverse=True)[:3]

  similar_images = [
      f"{S3_ENDPOINT_URL}/{S3_BUCKET_NAME}/{result[1]}"
      for result in sorted_results if result[1]
  ]

  return similar_images
