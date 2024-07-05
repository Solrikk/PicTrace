import aiohttp
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing import image
import boto3
from botocore.client import Config
import asyncio
from sklearn.metrics.pairwise import cosine_similarity

S3_BUCKET_NAME = 'your-new-bucket-name'
S3_REGION = 'your-new-region'
S3_ACCESS_KEY = 'your-new-access-key'
S3_SECRET_ACCESS_KEY = 'your-new-secret-access-key'
S3_ENDPOINT_URL = 'https://your-new-endpoint'

s3_client = boto3.client(
    's3',
    endpoint_url=S3_ENDPOINT_URL,
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_ACCESS_KEY,
    config=Config(region_name=S3_REGION, signature_version='s3v4'),
)

base_model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
model = Model(inputs=base_model.input, outputs=base_model.output)


async def download_image_from_s3(file_name):
  try:
    print(f"Downloading image from S3: {file_name}")
    response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=file_name)
    image_data = response['Body'].read()
    image_array = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    print("Image downloaded from S3")
    return img
  except Exception as e:
    print(f"Failed to download image {file_name} from S3 due to {e}")
    raise Exception('Image download from S3 failed')


def extract_features(img):
  print("Extracting features from the image")
  img = cv2.resize(img, (224, 224))
  img_array = image.img_to_array(img)
  img_array = np.expand_dims(img_array, axis=0)
  img_array = preprocess_input(img_array)
  features = model.predict(img_array)
  print("Features extracted")
  return features


async def compare_images(session, file_name, target_features):
  try:
    current_image = await download_image_from_s3(file_name)
    current_features = extract_features(current_image)
    similarity = cosine_similarity(current_features, target_features)
    print(f"Image similarity for {file_name}: {similarity[0][0]}")
    if similarity[0][0] > 0.5:
      return (similarity[0][0], file_name)
  except Exception as e:
    print(f"Failed to compare image {file_name} due to {e}")
  return (0, "")


async def list_s3_images():
  try:
    response = s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME)
    images = [
        item['Key'] for item in response.get('Contents', [])
        if item['Key'].endswith(('.jpg', '.jpeg', '.png'))
    ]
    print(f"Found {len(images)} images in S3 bucket")
    return images
  except Exception as e:
    print(f"Failed to list images in S3 bucket: {e}")
    raise Exception('Listing images in S3 failed')


async def find_similar_images(file_path):
  target_image = cv2.imread(file_path)
  target_features = extract_features(target_image)

  file_names = await list_s3_images()

  async with aiohttp.ClientSession() as session:
    tasks = [
        compare_images(session, file_name, target_features)
        for file_name in file_names
    ]
    results = await asyncio.gather(*tasks)

  valid_results = filter(lambda x: x[0] > 0, results)
  sorted_results = sorted(valid_results, key=lambda x: x[0], reverse=True)[:5]

  similar_images = []
  for result in sorted_results:
    if result[1]:
      similar_images.append(f"{S3_ENDPOINT_URL}/{S3_BUCKET_NAME}/{result[1]}")

  print(f"Found {len(similar_images)} similar images")
  return similar_images
