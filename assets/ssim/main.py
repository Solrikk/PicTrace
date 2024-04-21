from fastapi import FastAPI, HTTPException, UploadFile, File, Response
from fastapi.responses import HTMLResponse
from skimage.metrics import structural_similarity as compare_ssim
import matplotlib.pyplot as plt
import cv2
import numpy as np
from io import BytesIO
from PIL import Image

app = FastAPI()

def read_imagefile(file) -> Image.Image:
    image = Image.open(BytesIO(file))
    return image

def convert_to_gray(image):
    image = np.array(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray

def resize_image(image, size=(256, 256)):
    return cv2.resize(image, size, interpolation=cv2.INTER_AREA)

def load_image(image_file):
    image = read_imagefile(image_file)
    if image is None:
        raise IOError("Error loading image. Please check the file and try again.")
    gray = convert_to_gray(image)
    resized_gray = resize_image(gray)
    return resized_gray

@app.post("/uploadfiles/")
async def create_upload_files(imageA: UploadFile = File(...), imageB: UploadFile = File(...)):
    try:
        contentsA = await imageA.read()
        contentsB = await imageB.read()
        imageA = load_image(contentsA)
        imageB = load_image(contentsB)

        ssim, diff = compare_ssim(imageA, imageB, full=True)
        diff = (diff * 255).astype("uint8")

        fig, axs = plt.subplots(1, 3, figsize=(10, 3))

        axs[0].imshow(imageA, cmap='gray')
        axs[0].set_title('Image A')
        axs[0].axis('off')

        axs[1].imshow(imageB, cmap='gray')
        axs[1].set_title('Image B')
        axs[1].axis('off')

        axs[2].imshow(diff, cmap='gray')
        axs[2].set_title('Difference')
        axs[2].axis('off')

        plt.tight_layout()
        img_buf = BytesIO()
        plt.savefig(img_buf, format='png')
        img_buf.seek(0)
        plt.close(fig)

        img_buf.seek(0)
        return Response(content=img_buf.read(), media_type="image/png")

    except IOError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def main():
    content = """
<body>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="imageA" type="file">
<input name="imageB" type="file">
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)