## HarmonyImage

#### HarmonyImage is a fast and efficient tool for finding similar images based on structural similarity and keypoint matching in images. The application allows users to upload images or provide URLs to images, which are then compared against a database of images to find the most similar ones. To calculate similar images, the application uses asynchronous functions to download images from external sources and then process them.
![image](https://wikimedia.org/api/rest_v1/media/math/render/svg/4203f29f732e5cdc9d8a95907ef6d8e12f08ca09)
##### The excluded SSIM index ranges from -1 to +1. The value of +1 is achieved only with complete authenticity of the samples. As a rule, the metric is designed for an 8×8 pixel window.
#### To compare images, SSIM (Structural Similarity Index) is used to assess the similarity of images, as well as the ORB (Oriented FAST and Rotated BRIEF) algorithm to detect key points and their descriptors.
![image](https://i.stack.imgur.com/spSvt.png)
#### HarmonyImage - быстрый и эффективный инструмент для поиска аналогичных изображений на основе структурного сходства и сопоставления ключевых точек на изображениях. Приложение позволяет пользователям загружать изображения или предоставлять URL-адреса изображений, которые затем сравниваются с базой данных изображений для поиска наиболее похожих.
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
