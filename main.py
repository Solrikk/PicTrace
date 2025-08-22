
import os
import zipfile
import numpy as np
import tensorflow as tf
import pickle
from tensorflow.keras.models import load_model
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from io import BytesIO
from PIL import Image, UnidentifiedImageError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
ZIP_PATH = os.path.join(BASE_DIR, "photos.zip")
FEATURES_CACHE_PATH = os.path.join(BASE_DIR, "image_features_cache.pkl")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

image_features_cache = {}

app = FastAPI(title="PicTrace", description="Image similarity search application")
model = tf.keras.applications.MobileNetV2(weights='imagenet', include_top=False, pooling='avg')
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@app.get("/gallery")
async def get_gallery():
    images = get_images_from_zip()
    with zipfile.ZipFile(ZIP_PATH, "r") as archive:
        saved_images = []
        for image_key in images[:20]:
            try:
                saved_name = extract_and_save_image(archive, image_key)
                saved_images.append(saved_name)
            except Exception as e:
                print(f"Error processing image {image_key}: {e}")
    return {"photos": saved_images}

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/uploads", StaticFiles(directory=UPLOAD_FOLDER), name="uploads")

def preprocess_image(image: Image.Image):
    image = image.convert("RGB")
    image = image.resize((224, 224))
    image_array = np.array(image)
    image_array = np.expand_dims(image_array, axis=0)
    image_array = tf.keras.applications.mobilenet_v2.preprocess_input(image_array)
    return image_array

def get_image_features(image: Image.Image):
    return model.predict(preprocess_image(image))

def compare_images(image1_features, image2_features):
    return np.linalg.norm(image1_features - image2_features)

def get_images_from_zip():
    if not os.path.exists(ZIP_PATH):
        print(f"Warning: ZIP file {ZIP_PATH} not found")
        return []
    try:
        with zipfile.ZipFile(ZIP_PATH, "r") as archive:
            return [name for name in archive.namelist() if name.lower().endswith((".jpg", ".jpeg", ".png"))]
    except zipfile.BadZipFile:
        print(f"Error: {ZIP_PATH} is not a valid ZIP file")
        return []

def load_features_cache():
    global image_features_cache
    if os.path.exists(FEATURES_CACHE_PATH):
        try:
            with open(FEATURES_CACHE_PATH, 'rb') as f:
                image_features_cache = pickle.load(f)
            logger.info(f"Loaded {len(image_features_cache)} cached features")
        except Exception as e:
            logger.error(f"Failed to load features cache: {e}")
            image_features_cache = {}
    else:
        image_features_cache = {}

def save_features_cache():
    try:
        with open(FEATURES_CACHE_PATH, 'wb') as f:
            pickle.dump(image_features_cache, f)
        logger.info("Features cache saved successfully")
    except Exception as e:
        logger.error(f"Failed to save features cache: {e}")

def get_cached_features(image_key):
    return image_features_cache.get(image_key)

def cache_features(image_key, features):
    image_features_cache[image_key] = features

def preprocess_all_images():
    images = get_images_from_zip()
    if not images:
        logger.warning("No images found in ZIP archive")
        return
    
    processed_count = 0
    with zipfile.ZipFile(ZIP_PATH, "r") as archive:
        for image_key in images:
            if get_cached_features(image_key) is not None:
                continue
                
            try:
                with archive.open(image_key) as image_file:
                    image = Image.open(image_file).convert("RGB")
                    image_features = get_image_features(image)
                    cache_features(image_key, image_features)
                    processed_count += 1
                    
                    if processed_count % 10 == 0:
                        logger.info(f"Processed {processed_count} images...")
                        
            except Exception as e:
                logger.error(f"Error preprocessing image {image_key}: {e}")
    
    save_features_cache()
    logger.info(f"Preprocessing complete. Processed {processed_count} new images.")

def extract_and_save_image(archive, image_key):
    with archive.open(image_key) as image_file:
        image = Image.open(image_file)
        safe_image_name = os.path.basename(image_key)
        image_path = os.path.join(UPLOAD_FOLDER, safe_image_name)
        image.save(image_path)
        return safe_image_name

@app.get("/get_all_photos")
async def get_all_photos():
    images = get_images_from_zip()
    with zipfile.ZipFile(ZIP_PATH, "r") as archive:
        saved_images = []
        for image_key in images:
            try:
                saved_name = extract_and_save_image(archive, image_key)
                saved_images.append(saved_name)
            except Exception as e:
                print(f"Error processing image {image_key}: {e}")
    return {"photos": saved_images}

@app.post("/preprocess_images")
async def preprocess_images_endpoint():
    try:
        preprocess_all_images()
        return {
            "status": "success", 
            "message": "All images processed and cached",
            "cached_count": len(image_features_cache)
        }
    except Exception as e:
        logger.error(f"Error during preprocessing: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/cache_stats")
async def get_cache_stats():
    total_images = len(get_images_from_zip())
    cached_images = len(image_features_cache)
    return {
        "total_images": total_images,
        "cached_images": cached_images,
        "cache_percentage": round((cached_images / total_images * 100) if total_images > 0 else 0, 2)
    }

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("upload_form.html", {"request": request})

def validate_upload_file(file: UploadFile) -> bool:
    if file.size and file.size > 10 * 1024 * 1024:
        return False
    
    allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/webp"]
    if file.content_type not in allowed_types:
        return False
    
    return True

@app.post("/find_similar/")
async def find_similar_images(file: UploadFile = File(...)):
    if not validate_upload_file(file):
        return {"error": "Invalid file. Please upload a JPEG, PNG, or WebP image under 10MB."}
    
    try:
        file_content = await file.read()
        uploaded_image = Image.open(BytesIO(file_content)).convert("RGB")
        
        uploaded_filename = f"uploaded_{file.filename}"
        uploaded_path = os.path.join(UPLOAD_FOLDER, uploaded_filename)
        uploaded_image.save(uploaded_path)
        
        uploaded_image_features = get_image_features(uploaded_image)
    except Exception as e:
        logger.error(f"Failed to process uploaded image: {e}")
        return {"error": f"Failed to process uploaded image: {str(e)}"}
    
    images = get_images_from_zip()
    if not images:
        return {"error": "No images found in ZIP archive"}
    
    similarities = []
    
    cached_similarities = []
    uncached_images = []
    
    for image_key in images:
        cached_features = get_cached_features(image_key)
        if cached_features is not None:
            try:
                similarity = compare_images(uploaded_image_features, cached_features)
                cached_similarities.append((image_key, similarity))
            except Exception as e:
                logger.error(f"Error comparing cached image {image_key}: {e}")
        else:
            uncached_images.append(image_key)
    
    if uncached_images:
        logger.info(f"Processing {len(uncached_images)} uncached images...")
        with zipfile.ZipFile(ZIP_PATH, "r") as archive:
            for image_key in uncached_images:
                try:
                    with archive.open(image_key) as image_file:
                        image = Image.open(image_file).convert("RGB")
                        image_features = get_image_features(image)
                        cache_features(image_key, image_features)
                        
                        similarity = compare_images(uploaded_image_features, image_features)
                        similarities.append((image_key, similarity))
                except UnidentifiedImageError:
                    logger.warning(f"Cannot identify image file: {image_key}")
                except Exception as e:
                    logger.error(f"Error processing image {image_key}: {e}")
    
    similarities.extend(cached_similarities)
    
    save_features_cache()
    
    similarities.sort(key=lambda x: x[1])
    similar_images = []
    with zipfile.ZipFile(ZIP_PATH, "r") as archive:
        for image_key, similarity_score in similarities[:5]:
            try:
                saved_name = extract_and_save_image(archive, image_key)
                similar_images.append({
                    "filename": saved_name,
                    "similarity_score": float(similarity_score)
                })
            except Exception as e:
                logger.error(f"Error extracting image {image_key}: {e}")
    
    return {
        "filename": uploaded_filename, 
        "similar_images": similar_images,
        "total_processed": len(images)
    }

load_features_cache()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
