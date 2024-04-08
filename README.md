## Harmony-Image

#### HarmonyImage is a fast and efficient tool for finding similar images based on structural similarity and keypoint matching in images. The application allows users to upload images or provide URLs to images, which are then compared against a database of images to find the most similar ones. To calculate similar images, the application uses asynchronous functions to download images from external sources and then process them.
![image](https://wikimedia.org/api/rest_v1/media/math/render/svg/4203f29f732e5cdc9d8a95907ef6d8e12f08ca09)
#### The SSIM formula is based on three comparative measurements between the x and Y samples, brightness, contrast and structure. Separatecomparison functions:
![image](https://wikimedia.org/api/rest_v1/media/math/render/svg/96b4f1c3840c3707a93197798dcbfbfff24fa92b)
![image](https://wikimedia.org/api/rest_v1/media/math/render/svg/fcda97086476fa420b3b06568a0d202980a600d0)
![image](https://wikimedia.org/api/rest_v1/media/math/render/svg/1aebd62ba5b7e6ae47780ccfa659333f078d6eac)
#### The excluded SSIM index ranges from -1 to +1. The value of +1 is achieved only with complete authenticity of the samples. As a rule, the metric is designed for an 8×8 pixel window.
#### To compare images, SSIM (Structural Similarity Index) is used to assess the similarity of images, as well as the ORB (Oriented FAST and Rotated BRIEF) algorithm to detect key points and their descriptors.
![image](https://i.stack.imgur.com/spSvt.png)
#### The found key points are compared with each other to determine matches. These matches allow assessing the similarity of images from a perspective other than SSIM. The final similarity score is calculated as the average between the SSIM score and the relative number of matching key points (using the ORB algorithm), providing a comprehensive approach to analyzing the similarity of images.
HarmonyImageは、画像の構造の類似性と画像間のキーポイントのマッチングに基づいて類似した画像を検索するための高速かつ効率的なツールです。

## Features
- Upload images or provide URLs to images to find similar images
- Utilizes structural similarity and keypoint matching algorithms for accurate image comparison
- Stores images in a SQLite database for quick retrieval and comparison
- Returns a list of the most similar images found in the database

## Technologies Used
- Python
- FastAPI
- SQLite
- aiohttp
- OpenCV
- NumPy
- skimage

## Installation
1. Clone the repository
2. Install the required dependencies by running `pip install -r requirements.txt`
3. Run the application by executing `uvicorn main:app --reload`

## Usage
1. Access the web interface by navigating to the root URL
2. Upload an image file or provide a URL to an image
3. Receive a list of the most similar images based on the uploaded image

## Contributing
Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
