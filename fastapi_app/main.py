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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
ZIP_PATH = os.path.join(BASE_DIR, "photos.zip")
MODEL_PATH = os.path.join(BASE_DIR, "resnet50_local.h5")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = FastAPI()
model = load_model(MODEL_PATH)
templates = Jinja2Templates(directory=TEMPLATES_DIR)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/uploads", StaticFiles(directory=UPLOAD_FOLDER), name="uploads")

def preprocess_image(image: Image.Image):
    image = image.resize((224, 224))
    image_array = np.array(image)
    if image_array.shape[-1] == 4:
        image_array = image_array[..., :3]
    image_array = np.expand_dims(image_array, axis=0)
    image_array = tf.keras.applications.resnet50.preprocess_input(image_array)
    return image_array

def get_image_features(image: Image.Image):
    return model.predict(preprocess_image(image))

def compare_images(image1_features, image2_features):
    return np.linalg.norm(image1_features - image2_features)

def get_images_from_zip():
    with zipfile.ZipFile(ZIP_PATH, "r") as archive:
        return [name for name in archive.namelist() if name.lower().endswith((".jpg", ".jpeg", ".png"))]

def extract_and_save_image(archive, image_key):
    with archive.open(image_key) as image_file:
        image = Image.open(image_file)
        safe_image_name = os.path.basename(image_key)
        image_path = os.path.join(UPLOAD_FOLDER, safe_image_name)
        image.save(image_path)
        return safe_image_name

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("upload_form.html", {"request": request})

@app.post("/find_similar/")
async def find_similar_images(file: UploadFile = File(...)):
    uploaded_image = Image.open(BytesIO(await file.read()))
    uploaded_image_features = get_image_features(uploaded_image)
    images = get_images_from_zip()
    similarities = []
    with zipfile.ZipFile(ZIP_PATH, "r") as archive:
        for image_key in images:
            try:
                with archive.open(image_key) as image_file:
                    image = Image.open(image_file).convert("RGB")
                    similarity = compare_images(uploaded_image_features, get_image_features(image))
                    similarities.append((image_key, similarity))
            except UnidentifiedImageError:
                print(f"Cannot identify image file: {image_key}")
            except Exception as e:
                print(f"Error processing image {image_key}: {e}")
    similarities.sort(key=lambda x: x[1])
    similar_images = []
    with zipfile.ZipFile(ZIP_PATH, "r") as archive:
        for image_key, _ in similarities[:5]:
            similar_images.append(extract_and_save_image(archive, image_key))
    return {"filename": file.filename, "similar_images": similar_images}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
