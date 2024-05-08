![Logo](https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/orb6.png) 

<div align="center"> <h3> <a href="https://github.com/Solrikk/PicTrace/blob/main/README.md">⭐English⭐</a> | <a href="https://github.com/Solrikk/PicTrace/blob/main/README_RU.md">Russian</a> | <a href="https://github.com/Solrikk/PicTrace/blob/main/README_GE.md">German</a> | <a href="https://github.com/Solrikk/PicTrace/blob/main/README_JP.md">Japanese</a> | <a href="README_KR.md">Korean</a> | <a href="README_CN.md">Chinese</a> </h3> </div>

-----------------

# PicTrace

 🔎 _**PicTrace**_ is an efficient image matching platform leveraging `structural similarity` and `keypoint algorithms` for fast, accurate image searches. It allows direct uploads or URL submissions, quickly scanning a large database to find `similar images`. With `asynchronous processing`, PicTrace delivers a smooth and quick `visual search` experience.

## Features ⚙️
- **_Supports Multiple-Technologies_** ☄️

    _**Python**_  with libraries:
  - `FastAPI` - Used for web application creation and handling HTTP requests, supports asynchronous operations. ([details](https://fastapi.tiangolo.com/))
  - `aiohttp` - Utilized for asynchronous HTTP requests, such as downloading images by URL. ([details](https://docs.aiohttp.org/en/stable/index.html))
  - `OpenCV (cv2)`: - A `computer vision` library used for image processing, including loading, resizing, and comparing images. ([details](https://gamedevacademy.org/cv2-python-tutorial-complete-guide/#:~:text=%E2%80%98cv2%E2%80%99%20is%20OpenCV%E2%80%99s%20python%20library,perceive%20visuals%20like%20a%20human))
  - `numpy` - A library for working with multi-dimensional arrays, used alongside OpenCV for image processing.
  - `skimage` - Specifically, the `structural_similarity` function is used to compare the similarity of images.
  - `hashlib` - Used to generate image hashes, allowing each image to be uniquely identified.

- **_Supports Multiple-Indexes_** 🚀

  - `Structural Similarity Index (SSIM)` ([details](https://en.wikipedia.org/wiki/Structural_similarity_index_measure))
  - `Feature Matching with ORB (Oriented FAST and Rotated BRIEF) Descriptor` ([details](https://en.wikipedia.org/wiki/Oriented_FAST_and_rotated_BRIEF))
  - `Resizing and Grayscale Conversion` ([details](https://en.wikipedia.org/wiki/Grayscale))
  - `Hashing for Image Identification`
    
-----------------

## ⚠️ Getting Started with PicTrace: ⚠️
_PicTrace is a powerful image tracing and comparison tool designed to streamline your development process. Follow these steps to set up your environment and launch the application successfully._

### _To work with PicTrace, make sure that you have the following components installed:_
- **Python 3.8 or higher:** PicTrace is built with Python, and running it requires you to have Python 3.8 or a newer version installed on your system. You can download the latest version of Python from [the official website](https://www.python.org/downloads/).
- **pip:** pip is the package installer for Python. It comes pre-installed with Python 3.4 and higher. We'll use pip to install the dependencies needed for PicTrace.
- **Git:** You'll need Git to clone the PicTrace repository. If you don't have Git installed, follow the instructions on [Git's official site](https://git-scm.com/downloads) to set it up on your system.
1. **_Clone the repository:_** ✔️

_First, you need to get a copy of the PicTrace source code on your local machine. Use the following command to clone the repository from `GitHub`:_

```shell
git clone https://github.com/yourusername/PicTrace.git
cd PicTrace
```
2. **_Set up a virtual environment:_** ✔️

_A virtual environment is crucial for isolating the project dependencies from your global Python setup. This prevents version conflicts among different projects._

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

## Results:
_For complex images with many details and possible presence of noise or distortions, even similarity at the level of **20%** and above can indicate the presence of significant common features. In such cases, a low percentage of similarity may be expected due to the complexity of the task and the limitations of the algorithm._
|Image 1 vs Image 2|Similar|Image|
|:-:|:-:|:-:|
|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/result_3-1.png" alt="" width="500"/>|**27,12%**|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/palegleam.jpg" alt="" width="300"/>|
|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/result_2.png" alt="" width="500"/>|**25,44%**|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/ryan-yao.jpg" alt="" width="300"/>|
|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/result_3.png" alt="" width="500"/>|**44,16%**|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/taro-ohtani.jpg" alt="" width="300"/>|
|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/ORB/images/Orb5.png" alt="" width="500"/>|___|__|
|<img src="" alt="" width="400"/>|___|__|
|<img src="" alt="" width="400"/>|___|__|
|<img src="" alt="" width="400"/>|___|__|

## Examples: 📋
(**_code with comments_**)

```Python 
# Define an asynchronous function to process and compare an image against a target image.
async def process_image(session, image_entry, target_image):
  try:
    # Obtain a list of image URLs from a webpage.
    image_urls = await get_image_urls_from_page(session, image_entry["url"])
    for image_url in image_urls:
      # Download current image from the URL.
      current_image = await download_image(session, image_url)
      # Determine the optimal size for comparison, not exceeding 1024 pixels.
      optimal_size = max(max(target_image.shape[:2]),
                         max(current_image.shape[:2]))
      optimal_size = min(1024, optimal_size)
      # Resize both target and current images to the optimal size for comparison.
      target_image_resized = cv2.resize(target_image,
                                        (optimal_size, optimal_size))
      current_image_resized = cv2.resize(current_image,
                                         (optimal_size, optimal_size))
      # Convert images to grayscale for the comparison process.
      target_gray = cv2.cvtColor(target_image_resized, cv2.COLOR_BGR2GRAY)
      current_gray = cv2.cvtColor(current_image_resized, cv2.COLOR_BGR2GRAY)
      # Calculate the Structural Similarity Index (SSIM) between the two images.
      ssim_index = ssim(target_gray, current_gray)
      # Initialize ORB detector for feature extraction.
      orb = cv2.ORB_create(nfeatures=500)
      # Detect keypoints and compute descriptors for both images.
      target_keypoints, target_descriptors = orb.detectAndCompute(
          target_gray, None)
      current_keypoints, current_descriptors = orb.detectAndCompute(
          current_gray, None)
      # Return early if no descriptors are found in either image.
      if target_descriptors is None or current_descriptors is None:
        return (0, image_entry["url"])
      # Setup parameters for FLANN based matcher, used for finding good matches.
      index_params = dict(algorithm=6,
                          table_number=6,
                          key_size=12,
                          multi_probe_level=1)
      search_params = dict(checks=50)
      flann = cv2.FlannBasedMatcher(index_params, search_params)
      # Match descriptors between the two images and filter good matches.
      matches = flann.knnMatch(target_descriptors, current_descriptors, k=2)
      good_matches = [m for m, n in matches if m.distance < 0.75 * n.distance]
      # Calculate the feature score based on good matches.
      feature_score = len(good_matches) / float(len(target_keypoints))
      # Compute histograms for both images in RGB channels.
      target_hist = cv2.calcHist([target_image_resized], [0, 1, 2], None,
                                 [32, 32, 32], [0, 256, 0, 256, 0, 256])
      current_hist = cv2.calcHist([current_image_resized], [0, 1, 2], None,
                                  [32, 32, 32], [0, 256, 0, 256, 0, 256])
      # Normalize histograms.
      cv2.normalize(target_hist, target_hist)
      cv2.normalize(current_hist, current_hist)
      # Compare histograms using correlation method.
      hist_score = cv2.compareHist(target_hist, current_hist,
                                   cv2.HISTCMP_CORREL)
      # Calculate the final score by averaging SSIM, feature, and histogram scores.
      final_score = (feature_score + ssim_index + hist_score) / 3
      return (final_score, image_entry["url"])
  except Exception as e:
    # Handle any errors during the process and return a zero score.
    print(f"Failed to process image {image_entry['url']} due to {e}")
    return (0, image_entry["url"])
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
