import cv2
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.models import Model

base_model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
model = Model(inputs=base_model.input, outputs=base_model.output)


def extract_features_batch(img_list):
  img_array = np.array(
      [cv2.resize(img, (224, 224)) for img in img_list if img is not None])
  if len(img_array) == 0:
    return np.array([])
  img_array = preprocess_input(img_array)
  features = model.predict(img_array, batch_size=32)
  return features


def extract_architecture_features():
  dummy_image = np.ones((224, 224, 3)) * 255
  dummy_image = preprocess_input(dummy_image)
  return model.predict(np.array([dummy_image]))


def extract_aviation_features():
  dummy_image = np.ones((224, 224, 3)) * 128
  dummy_image = preprocess_input(dummy_image)
  return model.predict(np.array([dummy_image]))


def extract_background_features():
  dummy_image = np.ones((224, 224, 3)) * 50
  dummy_image = preprocess_input(dummy_image)
  return model.predict(np.array([dummy_image]))


async def is_architecture_image(image_path):
  img = cv2.imread(image_path)
  if img is None:
    raise ValueError(f"Failed to read image from file path: {image_path}")

  features = extract_features_batch([img])
  architecture_features = extract_architecture_features()
  similarity = cosine_similarity(features, architecture_features)
  return similarity[0][0] > 0.5


async def is_aviation_image(image_path):
  img = cv2.imread(image_path)
  if img is None:
    raise ValueError(f"Failed to read image from file path: {image_path}")

  features = extract_features_batch([img])
  aviation_features = extract_aviation_features()
  similarity = cosine_similarity(features, aviation_features)
  return similarity[0][0] > 0.5


async def is_background_image(image_path):
  img = cv2.imread(image_path)
  if img is None:
    raise ValueError(f"Failed to read image from file path: {image_path}")

  features = extract_features_batch([img])
  background_features = extract_background_features()
  similarity = cosine_similarity(features, background_features)
  return similarity[0][0] > 0.5
