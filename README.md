![Logo](https://github.com/Solrikk/PicTrace/blob/main/assets/OpenCV%20-%20result/bee.jpg)

<div align="center">
  <h3>
    <a href="https://github.com/Solrikk/PicTrace/blob/main/README.md">⭐English ⭐</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/README_RU.md">Russian</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/README_GE.md">German</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/README_JP.md">Japanese</a> |
    <a href="README_KR.md">Korean</a> |
    <a href="README_CN.md">Chinese</a>
  </h3>
</div>

-----------------

# PicTrace 🔍

_**PicTrace**_ is a highly efficient image matching platform that leverages computer vision using _**OpenCV**_, deep learning with _**TensorFlow**_ and the _**ResNet50 model**_, asynchronous processing with _**aiohttp**_, and the _**FastAPI**_ web framework for rapid and accurate image search. PicTrace allows users to upload images directly or provide URLs, quickly scanning a vast database to find similar images. Asynchronous processing ensures smooth and fast visual search, enhancing the user experience.

# Online Demos:

Curious to see how _PicTrace_ works in real-time? 

Explore my online demo and witness the capabilities of my image matching platform.

[Online Demo](https://PicTrace.replit.app) - **Give it a try and see for yourself!**

![PicTrace Demo](https://github.com/Solrikk/PicTrace/blob/main/assets/gif/Pictrace.gif)

## Table of Contents:
1. [Features ⚡](#features-⚡)
2. [Getting Started with PicTrace 🚀](#getting-started-with-pictrace-🚀)
   - [Prerequisites](#prerequisites)
   - [Steps to Set Up PicTrace](#steps-to-set-up-pictrace)
   - [Launching the application](#launching-the-application)
3. [Results: 👨‍💻](#results-👨‍💻)
4. [Examples: 📋](#examples-📋)
   - [Code with Comments](#code-with-comments)
5. [How SSIM Works in PicTrace](#how-ssim-works-in-pictrace)
6. [How ORB Works in PicTrace](#how-orb-works-in-pictrace)
7. [Combining SSIM and ORB](#combining-ssim-and-orb)
8. [OpenCV (Open Source Computer Vision Library) 🌐](#opencv-open-source-computer-vision-library-🌐)
9. [Neural Network Model (ResNet50) 🧠](#neural-network-model-resnet50-🧠)
10. [Final Selection of Similar Images](#final-selection-of-similar-images)

## Features: ⚡
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

## Getting Started with PicTrace: 🚀
_PicTrace is a powerful image tracing and comparison tool designed to streamline your development process. Follow these steps to set up your environment and launch the application successfully._

### Prerequisites
To work with PicTrace, ensure you have the following components installed:

- **Python 3.8 or higher:** PicTrace is built with Python. You can download the latest version of Python from [the official website](https://www.python.org/downloads/).
- **pip:** The package installer for Python, which comes pre-installed with Python 3.4 and higher. We'll use pip to install the necessary dependencies.
- **Git:** Required to clone the PicTrace repository. If Git is not already installed on your system, follow the installation instructions on [Git's official site](https://git-scm.com/downloads).

### Steps to Set Up PicTrace:
1. **Clone the repository**

_First, get a copy of the PicTrace source code on your local machine. Use the following commands to clone the repository from GitHub:_

```git clone https://github.com/solrikk/PicTrace.git```

2. **_Set up a virtual environment:_** ✔️

_A virtual environment is crucial for isolating the project dependencies from your global Python setup, preventing version conflicts among different projects. To create and activate a virtual environment, execute the following commands:._

To create and activate a virtual environment, follow these commands:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux и MacOS
source venv/bin/activate
```

3. **_Install dependencies:_** ✔️
 - _This command reads the `requirements.txt` file and installs all listed packages, ensuring that PicTrace has all the necessary components to run smoothly._
```bash
pip install -r requirements.txt
```
### _Launching the application:_
1. **_Start the server:_**
```bash
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

## _OpenCV (Open Source Computer Vision Library) 🌐:_

<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/OpenCV%20-%20result/parrot.png" width="95%" /> 

**OpenCV** is a powerful computer vision library that provides tools for image and video processing. It is widely used in fields related to machine vision, image recognition, video analysis, and more. The library includes a wide range of algorithms for image analysis, such as object detection, face recognition, motion tracking, video manipulation, and more.

Key features of **OpenCV** include:
1. **Loading and saving images 🖼️**: Supports various image formats and allows for easy loading, resizing, and saving of images, which is crucial for handling large datasets.
2. **Image processing ✨**: Provides functions for filtering images, converting them to grayscale, resizing, rotating, and other manipulations. This is important for preprocessing images before analysis.
3. **Object detection 🔍**: Includes algorithms for detecting edges, corners, and other key points, which helps in identifying and tracking specific objects in a frame.
4. **Object recognition 👁️**: Offers tools for recognizing faces, gestures, and other objects in images and videos, which is key for many computer vision applications.

## Neural Network Model (ResNet50) 🧠:

![image](https://github.com/Solrikk/PicTrace/assets/70236693/d47bd022-8a05-48fc-b6c8-147ec99520ce)


The **ResNet50** (Residual Network) model is one of the most popular and powerful deep learning architectures for image classification and feature extraction tasks. Your neural network model **ResNet50** provides the following advantages:

1. **Deep residual networks 🏗️**: Uses residual networks to ease the training of deep neural networks, allowing for the construction of very deep architectures without the risk of vanishing gradients.
2. **Pre-trained weights 🎓**: The model comes with pre-trained weights on the ImageNet dataset, which can significantly speed up training and improve accuracy in image classification tasks.
3. **Feature extraction 🔑**: The model can be used to extract features from images, which is useful for tasks related to cognitive data analysis and machine learning.
4. **Flexibility 🚀**: The model can be used for both classification and the task of extracting and comparing image features, which is suitable for your application.

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
