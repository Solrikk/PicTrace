import os
import zipfile
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from io import BytesIO
from PIL import Image, UnidentifiedImageError

app = FastAPI()

model = load_model('resnet50_local.h5')
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

ZIP_PATH = 'photos.zip'
UPLOAD_FOLDER = 'uploads'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
    return features

def compare_images(image1_features, image2_features):
    return np.linalg.norm(image1_features - image2_features)

def get_images_from_zip():
    with zipfile.ZipFile(ZIP_PATH, 'r') as archive:
        image_keys = [name for name in archive.namelist() if name.lower().endswith(('.jpg', '.jpeg', '.png'))]
    return image_keys

def extract_and_save_image(archive, image_key):
    with archive.open(image_key) as image_file:
        image = Image.open(image_file)
        safe_image_name = os.path.basename(image_key)
        image_path = os.path.join(UPLOAD_FOLDER, safe_image_name)
        image.save(image_path)
        return safe_image_name

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/find_similar/")
async def find_similar_images(file: UploadFile = File(...)):
    uploaded_image = Image.open(BytesIO(await file.read()))
    uploaded_image_features = get_image_features(uploaded_image)
    images = get_images_from_zip()
    similarities = []

    with zipfile.ZipFile(ZIP_PATH, 'r') as archive:
        for image_key in images:
            try:
                with archive.open(image_key) as image_file:
                    image = Image.open(image_file)
                    image = image.convert('RGB')
                    image_features = get_image_features(image)
                    similarity = compare_images(uploaded_image_features, image_features)
                    similarities.append((image_key, similarity))
            except UnidentifiedImageError:
                print(f"Cannot identify image file: {image_key}")
            except Exception as e:
                print(f"Error processing image {image_key}: {e}")

    similarities.sort(key=lambda x: x[1])
    similar_images = []

    with zipfile.ZipFile(ZIP_PATH, 'r') as archive:
        for image_key, _ in similarities[:5]:
            saved_image_name = extract_and_save_image(archive, image_key)
            similar_images.append(saved_image_name)

    return {
        'filename': file.filename,
        'similar_images': similar_images
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
