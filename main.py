import os
import sys
import zipfile
import pickle

from flask import Flask, request, render_template, redirect, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image, UnidentifiedImageError

# ---------------------------
# Settings and global constants
# ---------------------------
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ZIP_PATH = 'photos.zip'
MODEL_PATH = 'resnet50_local.h5'
FEATURES_PATH = 'image_features.pkl'
TOP_K = 5
SIMILARITY_THRESHOLD = 0.45  # For display purposes, consider as "60%"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'your_secret_key_here'  # Used for flash messages

# ---------------------------
# Function for correctly locating resources
# (useful when packaging with PyInstaller, among others)
# ---------------------------
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ---------------------------
# Functions for image processing and feature extraction
# ---------------------------
model = load_model(MODEL_PATH)

def preprocess_image(image: Image.Image):
    image = image.resize((224, 224))
    image_array = np.array(image)
    if image_array.shape[-1] == 4:
        image_array = image_array[..., :3]
    image_array = np.expand_dims(image_array, axis=0)
    image_array = tf.keras.applications.resnet50.preprocess_input(image_array)
    return image_array

def get_image_features(image: Image.Image):
    preprocessed_image = preprocess_image(image)
    features = model.predict(preprocessed_image)
    return features.flatten()

def cosine_similarity(features1, features2):
    num = np.dot(features1, features2)
    den = np.linalg.norm(features1) * np.linalg.norm(features2)
    return num / (den + 1e-9)

def extract_features_from_zip():
    image_features = {}
    with zipfile.ZipFile(ZIP_PATH, 'r') as archive:
        image_keys = [name for name in archive.namelist() if name.lower().endswith(('.jpg', '.jpeg', '.png'))]
        for image_key in image_keys:
            try:
                with archive.open(image_key) as image_file:
                    image = Image.open(image_file).convert('RGB')
                    features = get_image_features(image)
                    image_features[image_key] = features
            except UnidentifiedImageError:
                print(f"Cannot open image: {image_key}")
            except Exception as e:
                print(f"Error processing {image_key}: {e}")
    with open(FEATURES_PATH, 'wb') as f:
        pickle.dump(image_features, f)
    print(f"Features extracted and saved to {FEATURES_PATH}")

def load_precomputed_features():
    if not os.path.exists(FEATURES_PATH):
        extract_features_from_zip()
    with open(FEATURES_PATH, 'rb') as f:
        image_features = pickle.load(f)
    return image_features

image_features = load_precomputed_features()

def extract_and_save_image(archive, image_key):
    with archive.open(image_key) as image_file:
        image = Image.open(image_file).convert('RGB')
        safe_image_name = os.path.basename(image_key)
        image_path = os.path.join(UPLOAD_FOLDER, safe_image_name)
        image.save(image_path)
        return safe_image_name

def find_similar_images(uploaded_image: Image.Image):
    uploaded_image_features = get_image_features(uploaded_image)
    similarities = []
    for image_key, features in image_features.items():
        sim_val = cosine_similarity(uploaded_image_features, features)
        if sim_val >= SIMILARITY_THRESHOLD:
            similarities.append((image_key, sim_val))
    similarities.sort(key=lambda x: x[1], reverse=True)
    similar_images = []
    if similarities:
        with zipfile.ZipFile(ZIP_PATH, 'r') as archive:
            for image_key, sim_val in similarities[:TOP_K]:
                saved_image_name = extract_and_save_image(archive, image_key)
                similar_images.append((saved_image_name, sim_val))
    return similar_images

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'bmp', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ---------------------------
# Flask routes
# ---------------------------
@app.route('/', methods=['GET', 'POST'])
def index():
    result_text = None
    similar_images = []
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No file was uploaded.')
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            flash('No file selected.')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            try:
                uploaded_image = Image.open(file.stream).convert('RGB')
            except UnidentifiedImageError:
                flash('The uploaded file is not a valid image.')
                return redirect(request.url)
            except Exception as e:
                flash(str(e))
                return redirect(request.url)
            similar_images = find_similar_images(uploaded_image)
            if similar_images:
                result_text = "Similar images found (similarity ≥ 60%):"
            else:
                result_text = "No matching images found."
    return render_template('index.html', result_text=result_text, similar_images=similar_images)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/internet-search')
def internet_search():
    return "Internet search functionality is not implemented yet."

@app.route('/folder-search')
def folder_search():
    return "Folder search functionality is not implemented yet."

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
