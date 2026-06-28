
import os
import zipfile
import numpy as np
import tensorflow as tf
import pickle
import cv2
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
CACHE_VERSION = 2
FEATURE_MODEL_NAME = "mobilenetv2-imagenet-poolingavg-faceaware"
MODEL_INPUT_SIZE = (224, 224)
FEATURE_BATCH_SIZE = 24
FULL_IMAGE_WEIGHT = 0.55
FACE_CROP_WEIGHT = 0.45
FACE_MISMATCH_PENALTY = 0.9
FACE_AREA_WEIGHT = 0.08
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

image_features_cache = {}

app = FastAPI(title="PicTrace", description="Image similarity search application")
model = tf.keras.applications.MobileNetV2(weights='imagenet', include_top=False, pooling='avg')
face_detectors = [
    cv2.CascadeClassifier(os.path.join(cv2.data.haarcascades, cascade_name))
    for cascade_name in (
        "haarcascade_frontalface_alt2.xml",
        "haarcascade_frontalface_default.xml",
        "haarcascade_profileface.xml",
    )
]
face_detectors = [detector for detector in face_detectors if not detector.empty()]
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

def preprocess_image_batch(images):
    image_arrays = []
    for image in images:
        image = image.convert("RGB").resize(MODEL_INPUT_SIZE)
        image_arrays.append(np.asarray(image, dtype=np.float32))
    batch = np.stack(image_arrays, axis=0)
    return tf.keras.applications.mobilenet_v2.preprocess_input(batch)

def normalize_features(features):
    features = np.asarray(features, dtype=np.float32)
    if features.ndim == 1:
        features = features.reshape(1, -1)
    else:
        features = features.reshape(features.shape[0], -1)
    norms = np.linalg.norm(features, axis=1, keepdims=True)
    return features / np.maximum(norms, 1e-12)

def get_image_embeddings(images):
    if not images:
        return np.empty((0, 0), dtype=np.float32)
    features = model.predict(preprocess_image_batch(images), verbose=0)
    return normalize_features(features)

def box_iou(box_a, box_b):
    ax, ay, aw, ah = box_a
    bx, by, bw, bh = box_b
    x_left = max(ax, bx)
    y_top = max(ay, by)
    x_right = min(ax + aw, bx + bw)
    y_bottom = min(ay + ah, by + bh)
    if x_right <= x_left or y_bottom <= y_top:
        return 0.0
    intersection = (x_right - x_left) * (y_bottom - y_top)
    union = aw * ah + bw * bh - intersection
    return intersection / union if union else 0.0

def dedupe_faces(faces):
    selected = []
    for face in sorted(faces, key=lambda item: item[2] * item[3], reverse=True):
        if all(box_iou(face, existing) < 0.3 for existing in selected):
            selected.append(face)
    return selected

def detect_faces(image: Image.Image):
    if not face_detectors:
        return []
    rgb_image = np.asarray(image.convert("RGB"))
    gray_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2GRAY)
    min_side = min(gray_image.shape[:2])
    min_size = max(28, int(min_side * 0.08))
    detected_faces = []
    for detector in face_detectors:
        faces = detector.detectMultiScale(
            gray_image,
            scaleFactor=1.08,
            minNeighbors=4,
            minSize=(min_size, min_size),
        )
        detected_faces.extend(tuple(map(int, face)) for face in faces)
    return dedupe_faces(detected_faces)

def crop_largest_face(image: Image.Image, faces):
    x, y, width, height = faces[0]
    image_width, image_height = image.size
    margin = int(max(width, height) * 0.45)
    left = max(0, x - margin)
    top = max(0, y - margin)
    right = min(image_width, x + width + margin)
    bottom = min(image_height, y + height + margin)
    return image.crop((left, top, right, bottom)).convert("RGB")

def build_image_entries(image_items):
    images = [image for _, image in image_items]
    full_embeddings = get_image_embeddings(images)
    entries = {}
    face_jobs = []

    for index, (image_key, image) in enumerate(image_items):
        image = image.convert("RGB")
        faces = detect_faces(image)
        largest_face_area = 0.0
        if faces:
            x, y, width, height = faces[0]
            largest_face_area = (width * height) / max(image.width * image.height, 1)
            face_jobs.append((image_key, crop_largest_face(image, faces)))

        entries[image_key] = {
            "version": CACHE_VERSION,
            "embedding": full_embeddings[index],
            "face_count": len(faces),
            "face_area": float(largest_face_area),
            "face_embedding": None,
        }

    if face_jobs:
        face_embeddings = get_image_embeddings([image for _, image in face_jobs])
        for index, (image_key, _) in enumerate(face_jobs):
            entries[image_key]["face_embedding"] = face_embeddings[index]

    return entries

def cosine_distance(features_a, features_b):
    features_a = np.asarray(features_a, dtype=np.float32).reshape(-1)
    features_b = np.asarray(features_b, dtype=np.float32).reshape(-1)
    return float(np.clip(1.0 - np.dot(features_a, features_b), 0.0, 2.0))

def compare_images(query_entry, candidate_entry):
    full_distance = cosine_distance(query_entry["embedding"], candidate_entry["embedding"])
    query_has_face = query_entry.get("face_count", 0) > 0
    candidate_has_face = candidate_entry.get("face_count", 0) > 0

    if query_has_face and candidate_has_face and query_entry.get("face_embedding") is not None and candidate_entry.get("face_embedding") is not None:
        face_distance = cosine_distance(query_entry["face_embedding"], candidate_entry["face_embedding"])
        face_area_delta = abs(query_entry.get("face_area", 0.0) - candidate_entry.get("face_area", 0.0))
        return (
            FULL_IMAGE_WEIGHT * full_distance
            + FACE_CROP_WEIGHT * face_distance
            + min(face_area_delta, 0.75) * FACE_AREA_WEIGHT
        )

    if query_has_face and not candidate_has_face:
        return full_distance + FACE_MISMATCH_PENALTY

    return full_distance

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
                payload = pickle.load(f)
            meta = payload.get("_meta", {}) if isinstance(payload, dict) else {}
            if meta.get("version") == CACHE_VERSION and meta.get("model") == FEATURE_MODEL_NAME:
                items = payload.get("items", {})
                image_features_cache = {
                    key: entry
                    for key, entry in items.items()
                    if is_valid_cache_entry(entry)
                }
                logger.info(f"Loaded {len(image_features_cache)} cached image entries")
            else:
                logger.info("Ignoring legacy image feature cache")
                image_features_cache = {}
        except Exception as e:
            logger.error(f"Failed to load features cache: {e}")
            image_features_cache = {}
    else:
        image_features_cache = {}

def save_features_cache():
    try:
        with open(FEATURES_CACHE_PATH, 'wb') as f:
            pickle.dump(
                {
                    "_meta": {
                        "version": CACHE_VERSION,
                        "model": FEATURE_MODEL_NAME,
                    },
                    "items": image_features_cache,
                },
                f,
                protocol=pickle.HIGHEST_PROTOCOL,
            )
        logger.info("Features cache saved successfully")
    except Exception as e:
        logger.error(f"Failed to save features cache: {e}")

def is_valid_cache_entry(entry):
    if not isinstance(entry, dict) or entry.get("version") != CACHE_VERSION:
        return False
    embedding = entry.get("embedding")
    return np.asarray(embedding).reshape(-1).shape[0] == 1280

def get_cached_features(image_key):
    entry = image_features_cache.get(image_key)
    return entry if is_valid_cache_entry(entry) else None

def cache_features(image_entries):
    image_features_cache.update(image_entries)

def ensure_features_cached(images):
    uncached_images = [image_key for image_key in images if get_cached_features(image_key) is None]
    if not uncached_images:
        return 0

    processed_count = 0
    batch = []
    logger.info(f"Processing {len(uncached_images)} uncached images in batches...")

    with zipfile.ZipFile(ZIP_PATH, "r") as archive:
        for image_key in uncached_images:
            try:
                with archive.open(image_key) as image_file:
                    image = Image.open(image_file).convert("RGB")
                    image.load()
                    batch.append((image_key, image))

                if len(batch) >= FEATURE_BATCH_SIZE:
                    cache_features(build_image_entries(batch))
                    processed_count += len(batch)
                    logger.info(f"Processed {processed_count}/{len(uncached_images)} images...")
                    batch = []
            except UnidentifiedImageError:
                logger.warning(f"Cannot identify image file: {image_key}")
            except Exception as e:
                logger.error(f"Error preprocessing image {image_key}: {e}")

        if batch:
            cache_features(build_image_entries(batch))
            processed_count += len(batch)

    save_features_cache()
    return processed_count

def preprocess_all_images():
    images = get_images_from_zip()
    if not images:
        logger.warning("No images found in ZIP archive")
        return
    processed_count = ensure_features_cached(images)
    logger.info(f"Preprocessing complete. Processed {processed_count} new images.")

def extract_and_save_image(archive, image_key):
    with archive.open(image_key) as image_file:
        image = Image.open(image_file)
        safe_image_name = os.path.basename(image_key)
        image_path = os.path.join(UPLOAD_FOLDER, safe_image_name)
        if os.path.splitext(safe_image_name)[1].lower() in (".jpg", ".jpeg") and image.mode != "RGB":
            image = image.convert("RGB")
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
    images = get_images_from_zip()
    total_images = len(images)
    cached_images = sum(1 for image_key in images if get_cached_features(image_key) is not None)
    return {
        "total_images": total_images,
        "cached_images": cached_images,
        "cache_percentage": round((cached_images / total_images * 100) if total_images > 0 else 0, 2)
    }

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request, "upload_form.html")

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
        
        uploaded_filename = f"uploaded_{os.path.basename(file.filename or 'image.jpg')}"
        uploaded_path = os.path.join(UPLOAD_FOLDER, uploaded_filename)
        uploaded_image.save(uploaded_path)
        
        query_entry = build_image_entries([("__query__", uploaded_image)])["__query__"]
    except Exception as e:
        logger.error(f"Failed to process uploaded image: {e}")
        return {"error": f"Failed to process uploaded image: {str(e)}"}
    
    images = get_images_from_zip()
    if not images:
        return {"error": "No images found in ZIP archive"}
    
    newly_cached = ensure_features_cached(images)
    similarities = []
    query_has_face = query_entry.get("face_count", 0) > 0

    for image_key in images:
        cached_features = get_cached_features(image_key)
        if cached_features is not None:
            try:
                similarity = compare_images(query_entry, cached_features)
                face_rank = 0 if not query_has_face or cached_features.get("face_count", 0) > 0 else 1
                similarities.append((image_key, similarity, face_rank))
            except Exception as e:
                logger.error(f"Error comparing cached image {image_key}: {e}")

    similarities.sort(key=lambda item: (item[2], item[1]))
    similar_images = []
    with zipfile.ZipFile(ZIP_PATH, "r") as archive:
        for image_key, similarity_score, _ in similarities[:5]:
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
        "total_processed": len(images),
        "newly_cached": newly_cached,
        "query_faces": query_entry.get("face_count", 0)
    }

load_features_cache()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
