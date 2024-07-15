import aiohttp
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing import image
import boto3
from botocore.client import Config
from concurrent.futures import ThreadPoolExecutor
import asyncio
from sklearn.metrics.pairwise import cosine_similarity

S3_BUCKET_NAME = '68597a50-pictrace'
S3_REGION = 'ru-1'
S3_ACCESS_KEY = '2YLZ7SZSE6AJQE58PK85'
S3_SECRET_ACCESS_KEY = 'TXuayVE5LyKqrVRuL2wrZQb8dVDOaxar0f7jb48P'
S3_ENDPOINT_URL = 'https://s3.timeweb.cloud'

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
        response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=file_name)
        image_data = response['Body'].read()
        image_array = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Failed to decode image")
        return img
    except Exception as e:
        print(f"Failed to download image {file_name} from S3 due to {e}")
        return None

def extract_features_batch(img_list):
    img_array = np.array([cv2.resize(img, (224, 224)) for img in img_list if img is not None])
    if len(img_array) == 0:
        return np.array([])
    img_array = preprocess_input(img_array)
    features = model.predict(img_array, batch_size=32)
    return features

async def compare_images(file_name, target_features, loop):
    try:
        current_image = await download_image_from_s3(file_name)
        if current_image is None:
            return (0, "")
        current_features = await loop.run_in_executor(None, lambda: extract_features_batch([current_image]))
        if current_features.size == 0:
            return (0, "")
        similarity = cosine_similarity(current_features, target_features)
        if similarity[0][0] > 0.5:
            return (similarity[0][0], file_name)
    except Exception as e:
        print(f"Failed to compare image {file_name} due to {e}")
    return (0, "")

async def list_s3_images():
    try:
        images = []
        continuation_token = None
        while True:
            if continuation_token:
                response = s3_client.list_objects_v2(
                    Bucket=S3_BUCKET_NAME,
                    ContinuationToken=continuation_token
                )
            else:
                response = s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME)
            images.extend([
                item['Key'] for item in response.get('Contents', [])
                if item['Key'].lower().endswith(('.jpg', '.jpeg', '.png'))
            ])
            if response.get('IsTruncated'):
                continuation_token = response.get('NextContinuationToken')
            else:
                break
        return images
    except Exception as e:
        print(f"Failed to list images in S3 bucket: {e}")
        raise Exception('Listing images in S3 failed')

async def find_similar_images(file_path):
    loop = asyncio.get_event_loop()
    target_image = cv2.imread(file_path)
    if target_image is None:
        raise ValueError(f"Failed to read target image from file path: {file_path}")
    target_features = extract_features_batch([target_image])

    file_names = await list_s3_images()

    tasks = [compare_images(file_name, target_features, loop) for file_name in file_names]
    results = await asyncio.gather(*tasks)

    valid_results = filter(lambda x: x[0] > 0, results)
    sorted_results = sorted(valid_results, key=lambda x: x[0], reverse=True)[:3]

    similar_images = [
        f"{S3_ENDPOINT_URL}/{S3_BUCKET_NAME}/{result[1]}"
        for result in sorted_results
        if result[1]
    ]

    return similar_images
