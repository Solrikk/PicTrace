from fastapi import FastAPI, UploadFile, File, HTTPException
import os
import cv2
import numpy as np
import io
from fastapi.responses import StreamingResponse, HTMLResponse
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

    img_matches = cv2.drawMatches(
        img1,
        kp1,
        img2,
        kp2,
        matches[:30],
        None,
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS |
              cv2.DrawMatchesFlags_DRAW_RICH_KEYPOINTS)

    for i, match in enumerate(matches[:30]):
        color = tuple(np.random.randint(0, 255, 3).tolist())
        img1_idx = match.queryIdx
        img2_idx = match.trainIdx
        (x1, y1) = kp1[img1_idx].pt
        (x2, y2) = kp2[img2_idx].pt

        cv2.circle(img_matches, (int(x1), int(y1)), 4, color, 2)
        cv2.circle(img_matches, (int(x2) + img1.shape[1], int(y2)), 4, color, 2)
        cv2.line(img_matches, (int(x1), int(y1)),
                 (int(x2) + img1.shape[1], int(y2)), color, 2)

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
                <input name="imageA" type="file" accept="image/*" required>
                <input name="imageB" type="file" accept="image/*" required>
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
    img1 = cv2.imdecode(nparrA, cv2.IMREAD_COLOR)
    img2 = cv2.imdecode(nparrB, cv2.IMREAD_COLOR)
    img_matches = orb_feature_matching(img1, img2)
    _, encoded_img = cv2.imencode('.PNG', img_matches)
    return StreamingResponse(io.BytesIO(encoded_img.tobytes()),
                             media_type="image/png")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)