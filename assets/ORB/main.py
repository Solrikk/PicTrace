from fastapi import FastAPI, UploadFile, File, HTTPException, Request
import os

os.environ["OPENCV_IO_ENABLE_GDAL"] = "1"
os.environ["OPENCV_IO_ENABLE_IMAGEIO"] = "1"
os.environ["OPENCV_IO_MAX_IMAGE_PIXELS"] = str(2**30)
import cv2
import uvicorn
import numpy as np
from fastapi.responses import StreamingResponse, HTMLResponse
import io
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")


def orb_feature_matching(img1, img2):
  orb = cv2.ORB_create()
  kp1, des1 = orb.detectAndCompute(img1, None)
  kp2, des2 = orb.detectAndCompute(img2, None)
  if des1 is None or des2 is None:
    raise HTTPException(
        status_code=400,
        detail="No features can be matched in one or both images.")
  bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
  matches = bf.match(des1, des2)
  matches = sorted(matches, key=lambda x: x.distance)
  img_matches = cv2.drawMatches(img1,
                                kp1,
                                img2,
                                kp2,
                                matches[:10],
                                None,
                                flags=2)
  return img_matches


@app.get("/", response_class=HTMLResponse)
async def read_root():
  html_content = """
    <html>
        <head>
            <title>ORB (Oriented FAST and Rotated BRIEF)</title>
        </head>
        <body>
            <h1>Upload two images to match features using ORB</h1>
            <form action="/match-features/" enctype="multipart/form-data" method="post">
                <input name="imageA" type="file">
                <input name="imageB" type="file">
                <input type="submit">
            </form>
        </body>
    </html>
    """
  return HTMLResponse(content=html_content)


@app.post("/match-features/")
async def match_features(imageA: UploadFile = File(...),
                         imageB: UploadFile = File(...)):
  contentsA = await imageA.read()
  contentsB = await imageB.read()
  nparrA = np.frombuffer(contentsA, np.uint8)
  nparrB = np.frombuffer(contentsB, np.uint8)
  img1 = cv2.imdecode(nparrA, cv2.IMREAD_GRAYSCALE)
  img2 = cv2.imdecode(nparrB, cv2.IMREAD_GRAYSCALE)
  img_matches = orb_feature_matching(img1, img2)
  _, encoded_img = cv2.imencode('.PNG', img_matches)
  return StreamingResponse(io.BytesIO(encoded_img.tobytes()),
                           media_type="image/png")


if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000)
