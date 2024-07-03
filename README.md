![Logo](https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/orb6.png)

<div align="center">
  <h3>
    <a href="https://github.com/Solrikk/PicTrace/blob/main/README.md">⭐ English ⭐</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/README_RU.md">🇷🇺 Russian</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/README_GE.md">🇩🇪 German</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/README_JP.md">🇯🇵 Japanese</a> |
    <a href="README_KR.md">🇰🇷 Korean</a> |
    <a href="README_CN.md">🇨🇳 Chinese</a>
  </h3>
</div>

-----------------

# PicTrace 🔍

_**PicTrace**_ is a highly efficient image matching platform that leverages computer vision using _**OpenCV**_, deep learning with _**TensorFlow**_ and the _**ResNet50 model**_, asynchronous processing with _**aiohttp**_, and the _**FastAPI**_ web framework for rapid and accurate image search. PicTrace allows users to upload images directly or provide URLs, quickly scanning a vast database to find similar images. Asynchronous processing ensures smooth and fast visual search, enhancing the user experience.

![PicTrace Demo](https://github.com/Solrikk/PicTrace/blob/main/assets/gif/Pictrace.gif)

## Features ⚡
- **_Supports Multiple Technologies_** 💼

    _**Python**_ with these powerful libraries:
  - **`FastAPI:`** Ideal for web application creation and handling HTTP requests, FastAPI is known for its high performance and support for asynchronous operations. [Details](https://fastapi.tiangolo.com/)
  - **`aiohttp:`** Perfect for handling asynchronous HTTP requests, such as downloading images by URL, making your app faster and more efficient. [Details](https://docs.aiohttp.org/en/stable/index.html)
  - **`OpenCV (cv2):`** A robust computer vision library used for advanced image processing, including loading, resizing, and comparing images, making it a critical component for your image-related tasks. [Details](https://docs.opencv.org/)
  - **`numpy:`** A versatile library for working with multi-dimensional arrays, often used alongside OpenCV for efficient image processing. [More Info](https://numpy.org/doc/)
  - **`scikit-image:`** Particularly, the `structural_similarity` (SSIM) function from this library is employed to compare the similarity of images, enhancing your application's accuracy in image matching. [Details](https://scikit-image.org/docs/stable/auto_examples/transform/plot_ssim.html)
  - **`hashlib:`** Utilized for generating unique hashes for each image, ensuring every image can be uniquely identified and efficiently managed. [More Info](https://docs.python.org/3/library/hashlib.html)

- **_Supports Multiple Indexes_** 🗂️

  - **`Image Hashing:`** Generating unique hashes for images to ensure unique identification and efficient management.
  - **`Feature Extraction with ResNet50:`** Utilizes the ResNet50 model for extracting robust feature representations from images.
  - **`Cosine Similarity:`** Measuring similarity between images using cosine similarity on feature vectors extracted from the images.

-----------------

## 🚀 Getting Started with PicTrace
_PicTrace is a powerful image tracing and comparison tool designed to streamline your development process. Follow these steps to set up your environment and launch the application successfully._

### Prerequisites
To work with PicTrace, ensure you have the following components installed:

- **Python 3.8 or higher:** PicTrace is built with Python. You can download the latest version of Python from [the official website](https://www.python.org/downloads/).
- **pip:** The package installer for Python, which comes pre-installed with Python 3.4 and higher. We'll use pip to install the necessary dependencies.
- **Git:** Required to clone the PicTrace repository. If Git is not already installed on your system, follow the installation instructions on [Git's official site](https://git-scm.com/downloads).

### Steps to Set Up PicTrace

1. **Clone the repository**

_First, get a copy of the PicTrace source code on your local machine. Use the following commands to clone the repository from GitHub:_

```git clone https://github.com/solrikk/PicTrace.git```

2. **_Set up a virtual environment:_** ✔️

_A virtual environment is crucial for isolating the project dependencies from your global Python setup, preventing version conflicts among different projects. To create and activate a virtual environment, execute the following commands:._

To create and activate a virtual environment, follow these commands:

```shell
python -m venv venv
# Windows
venv\Scripts\activate
# Linux и MacOS
source venv/bin/activate
```

3. **_Install dependencies:_** ✔️
 - _This command reads the `requirements.txt` file and installs all listed packages, ensuring that PicTrace has all the necessary components to run smoothly._
```shell
pip install -r requirements.txt
```
### _Launching the application:_
1. **_Start the server:_**
```shell
python app.py
```
`After starting the server, the application will be available at http://localhost:5000 .`

-----------------

## Results: 👨‍💻
_For complex images with many details and possible presence of noise or distortions, even similarity at the level of **20%** and above can indicate the presence of significant common features. In such cases, a low percentage of similarity may be expected due to the complexity of the task and the limitations of the algorithm._
|Image 1 vs Image 2|Similar|Image|
|:-:|:-:|:-:|
|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/result_3-1.png" alt="" width="500"/>|**27,12%**|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/palegleam.jpg" alt="" width="300"/>|
|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/result_2.png" alt="" width="500"/>|**25,44%**|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/ryan-yao.jpg" alt="" width="300"/>|
|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/result_3.png" alt="" width="500"/>|**44,16%**|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/taro-ohtani.jpg" alt="" width="300"/>|

## Examples: 📋
(**_code with comments_**)

```Python 
async def find_similar_images(file_path):
    # Load the data from the database, which contains information about images.
    db_data = load_db()
    # Read the target image from the given file path.
    target_image = cv2.imread(file_path)
    # Extract features from the target image using a pre-trained model.
    target_features = extract_features(target_image)
    # Create an aiohttp asynchronous session for handling HTTP requests.
    async with aiohttp.ClientSession() as session:
        # Create asynchronous tasks for the compare_images function for each image in the database.
        tasks = [
            compare_images(session, entry, target_features) for entry in db_data
            if "url" in entry  # Only perform comparisons for entries that contain an image URL.
        ]
        # Wait for all tasks to complete and gather the results.
        results = await asyncio.gather(*tasks)
    # Filter the results, keeping only those with a similarity score greater than 0.
    valid_results = filter(lambda x: x[0] > 0, results)   
    # Sort the filtered results by similarity score in descending order and take the top 5.
    sorted_results = sorted(valid_results, key=lambda x: x[0], reverse=True)[:5]
    # Create a list to store the URLs of the similar images.
    similar_images = []
    for result in sorted_results:
        if result[1]:
            similar_images.append(result[1])
    # Return the list of URLs of the similar images.
    return similar_images
```

-----------------

![image](https://wikimedia.org/api/rest_v1/media/math/render/svg/4203f29f732e5cdc9d8a95907ef6d8e12f08ca09)

SSIM compares patterns of pixel intensity changes which are important attributes for human vision. The SSIM score ranges from `-1 to +1`, where a `value of 1` indicates identical images. The process can be broken down into three components:

<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/ssim/ssim2.png" width="95%" /> 

1) **_Luminance Comparison_** allows for the assessment of the overall luminance of the images. Luminance in SSIM is measured as the average of all pixel values.
```Python
target_gray = cv2.cvtColor(target_image_resized, cv2.COLOR_BGR2GRAY)
current_gray = cv2.cvtColor(current_image_resized, cv2.COLOR_BGR2GRAY)
ssim_index = ssim(target_gray, current_gray)
```
2) **_Contrast Comparison_** is measured through the variance of pixel intensities (variations from the average value), understanding how similar the patterns of light and shadow distribution are between two images.
```Python
cv2.normalize(target_hist, target_hist)
cv2.normalize(current_hist, current_hist)
hist_score = cv2.compareHist(target_hist, current_hist, cv2.HISTCMP_CORREL)
```
3) **_Structure Comparison_** compares patterns of spatial pixel distribution, ignoring variations in luminance and contrast. It is done by calculating the covariance between the images relative to their local average values.
```Python
ssim_index = ssim(target_gray, current_gray)
```
![image](https://wikimedia.org/api/rest_v1/media/math/render/svg/96b4f1c3840c3707a93197798dcbfbfff24fa92b)
![image](https://wikimedia.org/api/rest_v1/media/math/render/svg/fcda97086476fa420b3b06568a0d202980a600d0)
![image](https://wikimedia.org/api/rest_v1/media/math/render/svg/1aebd62ba5b7e6ae47780ccfa659333f078d6eac)

To compare images, the Structural Similarity Index **(SSIM)** is used to assess the similarity between images, as well as the **ORB (Oriented FAST and Rotated BRIEF)** algorithm for detecting key points and their descriptions.

## _ORB (Oriented FAST and Rotated BRIEF):_ 
ORB method used in computer vision, particularly popular for tasks related to object recognition, image matching, and tracking. This method is focused on quickly finding key points on images and describing them in a way that allows for efficient comparison. Let's break down what ORB does with simpler examples:

<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/ORB/images/ORB3.png" width="95%" /> 

1) **Oriented FAST (Features from Accelerated Segment Test):** This part is responsible for detecting points of interest (or key points) on the image. It quickly identifies corners or edges that stand out in comparison to their surrounding areas. This way, significant or unique sections of the image can be identified.

2) **Rotated BRIEF (Binary Robust Independent Elementary Features):** After key points have been found, it's necessary to create a description of each to allow comparison with key points from another image. BRIEF generates a brief binary description of the points but lacks resistance to image rotation. This is where the "rotated" part comes in - ORB adds the ability to stably describe points even when images are rotated.

By combining these two approaches, ORB provides a fast and efficient way of matching images despite changes in viewing angle, scale, or lighting.

_Using the ORB algorithm, key points and descriptors are determined for both the current and target images._

The found key points are compared with each other to determine matches. These matches allow assessing the similarity of images from a perspective other than SSIM. The final similarity score is calculated as the average between the SSIM score and the relative number of matching key points (using the ORB algorithm), providing a comprehensive approach to analyzing the similarity of images.

PicTrace application, both the SSIM and ORB methods are utilized to find images that are similar to an uploaded image. Here's a simplified explanation of how each method works in the context of your application and contributes to finding similar images:

## How SSIM Works in PicTrace:
1) **_Resizing Images:_** When comparing the uploaded image to each image in the database, both images are resized to the same dimensions `(256x256 pixels)`. This standardizes the comparison, making it fair and more efficient since we're working with images of the same size.

2) **_Converting to Grayscale:_** Both images are converted to grayscale. This simplifies the comparison by focusing on the structure and intensity of light rather than being distracted by color differences.

3) **_Structural Similarity Comparison:_** The SSIM method then compares these grayscale images to assess their structural similarity. This involves analyzing how similar the patterns of light and shadow are between the two images, giving a score that reflects their similarity. A high score means the images are structurally similar.

## How ORB Works in PicTrace:
1) **_Detecting Key Points:_** ORB first identifies key points in both the uploaded image and each database image. These key points are distinctive spots that can be easily recognized and compared between images, such as corners and interesting textures.

2) **_Describing Key Points:_** For each key point detected, ORB generates a unique descriptor that summarizes the key point's characteristics. This descriptor is made rotation-invariant, meaning it describes the key point in a way that's consistent even if the image is rotated.

3) **_Matching Key Points:_** The application then matches key points between the uploaded image and each database image using these descriptors. The matching process involves finding key points in the database image that have descriptors similar to those in the uploaded image.

4) **_Scoring Matches:_** The more key points that match between two images, the higher the score of similarity based on ORB. This score reflects how many distinctive features are shared between the images.

## Combining SSIM and ORB:
After calculating similarity scores using both SSIM and ORB for each image comparison, Harmony-Image averages these scores to get a final measure of similarity.
Images from the database are then ranked based on their final similarity scores, and the top 5 most similar images are selected.

## Final Selection of Similar Images:
The application filters out duplicate URLs to ensure a diverse set of similar images.
 It returns URLs of the top similar images, which can then be presented to the user.
 In essence, your application uses a combination of structural analysis (SSIM) and feature matching (ORB) to find and rank images in your database that are most similar to an image uploaded by the user. This dual approach leverages the strengths of both methods, ensuring a robust and nuanced comparison that goes beyond simple pixel-by-pixel analysis.
