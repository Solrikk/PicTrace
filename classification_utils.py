import cv2
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.models import Model
import tensorflow as tf

physical_devices = tf.config.list_physical_devices('GPU')
if physical_devices:
  try:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
    print(f'{len(physical_devices)} GPUs are available')
  except:
    print("Error setting up GPU memory growth")

base_model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
model = Model(inputs=base_model.input, outputs=base_model.output)


def extract_features_batch(img_list, batch_size=32):
  img_array = np.array(
      [cv2.resize(img, (224, 224)) for img in img_list if img is not None])
  if len(img_array) == 0:
    return np.array([])
  img_array = preprocess_input(img_array)
  with tf.device('/GPU:0'):
    features = model.predict(img_array, batch_size=batch_size)
  return features


def extract_dummy_features(color_value):
  dummy_image = np.ones((224, 224, 3)) * color_value
  dummy_image = preprocess_input(dummy_image)
  return model.predict(np.array([dummy_image]))


async def is_category_image(image_path, category_features):
  img = cv2.imread(image_path)
  if img is None:
    raise ValueError(f"Failed to read image from file path: {image_path}")
  features = extract_features_batch([img])
  similarity = cosine_similarity(features, category_features)
  return similarity[0][0] > 0.5


async def is_architecture_image(image_path):
  architecture_features = extract_dummy_features(255)
  return await is_category_image(image_path, architecture_features)


async def is_aviation_image(image_path):
  aviation_features = extract_dummy_features(128)
  return await is_category_image(image_path, aviation_features)


async def is_background_image(image_path):
  background_features = extract_dummy_features(50)
  return await is_category_image(image_path, background_features)


async def is_animal_image(image_path):
  animal_features = extract_dummy_features(75)
  return await is_category_image(image_path, animal_features)


async def is_people_image(image_path):
  people_features = extract_dummy_features(200)
  return await is_category_image(image_path, people_features)
