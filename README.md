![Logo](https://github.com/Solrikk/PicTrace/blob/main/assets/OpenCV%20-%20result/bee.jpg)

<div align="center">

[![Visitors](https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fgithub.com%2FSolrikk%2FPicTrace&label=Views&countColor=%232ccce4)](https://visitorbadge.io/status?path=https%3A%2F%2Fgithub.com%2FSolrikk%2FPicTrace)
[![GitHub stars](https://img.shields.io/github/stars/Solrikk/PicTrace?style=flat&logo=github&color=yellow)](https://github.com/Solrikk/PicTrace/stargazers)
[![Profile Views](https://komarev.com/ghpvc/?username=Solrikk&color=brightgreen&style=flat&label=Profile+Views)](https://github.com/Solrikk)
[![GitHub license](https://img.shields.io/github/license/Solrikk/PicTrace?color=blue&style=flat)](https://github.com/Solrikk/PicTrace/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/Python-3.7%2B-blue?style=flat&logo=python)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-modern-green?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)

</div>

<div align="center">
  <h3>
    <a href="https://github.com/Solrikk/PicTrace/blob/main/README.md">✦ English ✦</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/docs/readme/README_RU.md">Russian</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/docs/readme/README_GE.md">German</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/docs/readme//README_JP.md">Japanese</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/docs/readme/README_KR.md">Korean</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/docs/readme/README_CN.md">Chinese</a>
  </h3>
</div>

-----------------

# PicTrace 🔍

✨ **PicTrace** is an advanced **Python-based** web application that allows users to find **visually similar images** from a comprehensive photo archive. Leveraging the power of **deep learning** and modern **image processing techniques**, PicTrace delivers fast and accurate search functionality that is ideal for tasks such as cataloging, organizing, and analyzing large sets of visual data.

# Demos:

Curious to see how _PicTrace_ works in real-time? 

**Give it a try and see for yourself!**

https://pictrace.replit.app/

![PicTrace Demo](https://github.com/Solrikk/PicTrace/blob/main/assets/gif/Pictrace.gif)

## Getting Started with PicTrace:
| **Operating System** | **Commands for Setup and Launch** |
|----------------------|----------------------------------|
| 🐧**Linux**            | ```bash sudo git clone https://github.com/Solrikk/PicTrace.git cd PicTrace sudo pip install poetry sudo poetry install sudo poetry run python3 main.py ``` |
| 🍎**macOS**            | ```bash sudo git clone https://github.com/Solrikk/PicTrace.git cd PicTrace sudo pip install poetry sudo poetry install sudo poetry run python3 main.py ``` |
| 🪟**Windows**          | Open Command Prompt as Administrator and run: ```bash git clone https://github.com/Solrikk/PicTrace.git cd PicTrace pip install poetry poetry install poetry run python main.py ``` |

![PicTrace Demo](https://github.com/Solrikk/PicTrace/blob/main/assets/gif/shell-PicTrrace.gif)

-----------------

## Features ⚡

- **_Supports Multiple Technologies_**
    - **Tkinter**: Provides a user-friendly graphical interface for the application, allowing users to interact with PicTrace seamlessly. [Details](https://docs.python.org/3/library/tkinter.html)
    - **TensorFlow and Keras**: Utilized for loading the ResNet50 model and extracting features from images, ensuring high accuracy and efficiency in image processing. [Details](https://www.tensorflow.org/api_docs/python/tf/keras)
    - **numpy**: A versatile library for working with multi-dimensional arrays, facilitating efficient computations and data handling. [Details](https://numpy.org/doc/)
    - **Pillow (PIL)**: A library for image processing, used for loading, resizing, and saving images. [Details](https://pillow.readthedocs.io/en/stable/)
    - **pickle**: A module for serializing and deserializing Python objects, used for saving and loading precomputed image features. [Details](https://docs.python.org/3/library/pickle.html)
    - **hashlib**: Utilized for generating unique hashes for each image, ensuring every image can be uniquely identified and efficiently managed. [Details](https://docs.python.org/3/library/hashlib.html)
    - **scikit-image**: Specifically, the `structural_similarity (SSIM)` function from this library is employed to compare the similarity of images, enhancing your application's accuracy in image matching. [Details](https://scikit-image.org/docs/stable/api/skimage.metrics.html#skimage.metrics.structural_similarity)
    - **OpenCV (cv2)**: A robust computer vision library used for advanced image processing, including loading, resizing, and comparing images, making it a critical component for your image-related tasks. [Details](https://docs.opencv.org/master/)
    - **zipfile**: Handles ZIP archives containing images, simplifying image collection management. [Details](https://docs.python.org/3/library/zipfile.html)

-----------------

## Results: 
_For complex images with many details and possible presence of noise or distortions, even similarity at the level of **20%** and above can indicate the presence of significant common features. In such cases, a low percentage of similarity may be expected due to the complexity of the task and the limitations of the algorithm._
|Image 1 vs Image 2|Similar|Image|
|:-:|:-:|:-:|
|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/result_3-1.png" alt="" width="500"/>|**27,12%**|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/palegleam.jpg" alt="" width="300"/>|
|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/result_2.png" alt="" width="500"/>|**25,44%**|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/ryan-yao.jpg" alt="" width="300"/>|
|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/result_3.png" alt="" width="500"/>|**44,16%**|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/taro-ohtani.jpg" alt="" width="300"/>|

## Examples: 
(**_code with comments_**)

```Python 
# ---------------------------
# Examples: Code with Comments
# ---------------------------
def find_similar_images(uploaded_image: Image.Image):
    
    # ---------------------------
    # Extract features from the uploaded image using the pre-trained ResNet50 model.
    # ---------------------------
    uploaded_features = get_image_features(uploaded_image)
    
    # ---------------------------
    # Compare with precomputed features:
    # Iterate over each image in the archive and compute cosine similarity.
    # ---------------------------
    similarities = []
    for image_key, features in image_features.items():
        sim_val = cosine_similarity(uploaded_features, features)
        if sim_val >= SIMILARITY_THRESHOLD:
            similarities.append((image_key, sim_val))
    
    # ---------------------------
    # Sort the list of similar images by similarity score in descending order.
    # ---------------------------
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    # ---------------------------
    # Extract and save the top K similar images from the ZIP archive.
    # ---------------------------
    similar_images = []
    if similarities:
        with zipfile.ZipFile(ZIP_PATH, 'r') as archive:
            for image_key, sim_val in similarities[:TOP_K]:
                saved_image_name = extract_and_save_image(archive, image_key)
                similar_images.append((saved_image_name, sim_val))
    
    # ---------------------------
    # Return the list of similar images along with their similarity scores.
    # ---------------------------
    return similar_images

```

-----------------

## _OpenCV (Open Source Computer Vision Library):_

<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/OpenCV%20-%20result/parrot.png" width="95%" /> 

**OpenCV** is a powerful computer vision library that provides tools for image and video processing. It is widely used in fields related to machine vision, image recognition, video analysis, and more. The library includes a wide range of algorithms for image analysis, such as object detection, face recognition, motion tracking, video manipulation, and more.

Key features of **OpenCV** include:
1. **Loading and saving images 🖼️**: Supports various image formats and allows for easy loading, resizing, and saving of images, which is crucial for handling large datasets.
2. **Image processing ✨**: Provides functions for filtering images, converting them to grayscale, resizing, rotating, and other manipulations. This is important for preprocessing images before analysis.
3. **Object detection 🔍**: Includes algorithms for detecting edges, corners, and other key points, which helps in identifying and tracking specific objects in a frame.
4. **Object recognition 👁️**: Offers tools for recognizing faces, gestures, and other objects in images and videos, which is key for many computer vision applications.

## Neural Network Model (ResNet50):

![image](https://github.com/Solrikk/PicTrace/assets/70236693/d47bd022-8a05-48fc-b6c8-147ec99520ce)


The **ResNet50** (Residual Network) model is one of the most popular and powerful deep learning architectures for image classification and feature extraction tasks. Your neural network model **ResNet50** provides the following advantages:

1. **Deep residual networks**: Uses residual networks to ease the training of deep neural networks, allowing for the construction of very deep architectures without the risk of vanishing gradients.
2. **Pre-trained weights**: The model comes with pre-trained weights on the ImageNet dataset, which can significantly speed up training and improve accuracy in image classification tasks.
3. **Feature extraction**: The model can be used to extract features from images, which is useful for tasks related to cognitive data analysis and machine learning.
4. **Flexibility**: The model can be used for both classification and the task of extracting and comparing image features, which is suitable for your application.

Together, **OpenCV** and **ResNet50** can be used to create powerful computer vision applications that can analyze visual data and perform complex tasks, such as automatic object recognition and image classification.

---

The ORB method, used in computer vision, is particularly popular for tasks related to object recognition, image matching, and tracking. This method focuses on quickly finding key points on images and describing them in a way that allows for efficient comparison.

<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/ORB/images/ORB3.png" width="65%" /> 

1. **Oriented FAST (Features from Accelerated Segment Test) 🚀:** This component is responsible for detecting points of interest (or key points) on the image. It quickly identifies corners or edges that stand out in comparison to their surrounding areas. This way, significant or unique sections of the image can be identified.

2. **Rotated BRIEF (Binary Robust Independent Elementary Features) 🔄:** After key points have been found, it is necessary to create a description for each to allow comparison with key points from another image. BRIEF generates a brief binary description of the points but lacks resistance to image rotation. This is where the "rotated" part comes in - ORB adds the ability to stably describe points even when images are rotated.

Combining these two approaches, ORB provides a fast and efficient way of matching images despite changes in viewing angle, scale, or lighting.

PicTrace uses both **SSIM** and **ORB** methods to find images that are similar to an uploaded image. Here's a simplified explanation of how each method works in the context of your application and contributes to finding similar images:

## How SSIM Works in PicTrace:
1. **Resizing Images 🔧:** When comparing the uploaded image to each image in the database, both images are resized to the same dimensions (256x256 pixels). This standardizes the comparison, making it fair and more efficient.
2. **Converting to Grayscale 🌑:** Both images are converted to grayscale. This simplifies the comparison by focusing on the structure and intensity of light rather than getting distracted by color differences.
3. **Structural Similarity Comparison 🧩:** The SSIM method then compares these grayscale images to assess their structural similarity. A high score means the images are structurally similar.

## How ORB Works in PicTrace:
1. **Detecting Key Points 📍:** ORB first identifies key points in both the uploaded image and each database image. These points are easily recognizable and can be compared between images.
2. **Describing Key Points 🖊️:** For each detected key point, ORB generates a unique descriptor that summarizes the key point's characteristics. This descriptor is invariant to image rotations.
3. **Matching Key Points 🔗:** The application matches key points between the uploaded image and each database image. The process involves finding key points in the database image that have descriptors similar to those of the uploaded image.
4. **Scoring Matches 🏅:** The more key points that match between two images, the higher the similarity score based on ORB. This score reflects how many distinctive features the images share.

Together, the **SSIM** and **ORB** methods provide a robust and accurate way to find and compare images that are similar to the uploaded image.
