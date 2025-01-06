![Logo](https://github.com/Solrikk/PicTrace/blob/main/assets/OpenCV%20-%20result/bee.jpg)

<div align="center">
  <h3>
    <a href="https://github.com/Solrikk/PicTrace/blob/main/README.md">⭐English ⭐</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/docs/readme/README_RU.md">Russian</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/docs/readme/README_GE.md">German</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/docs/readme//README_JP.md">Japanese</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/docs/readme/README_KR.md">Korean</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/docs/readme/README_CN.md">Chinese</a>
  </h3>
</div>

-----------------

# PicTrace 🔍

**PicTrace** is an advanced **Python-based** application equipped with a **graphical user interface (GUI)** and a **web version built on FastAPI** that enables users to identify **visually similar images** from a comprehensive **photo archive**. By harnessing the capabilities of **deep learning** and **sophisticated image processing methodologies**, **PicTrace** delivers **rapid and precise search functionalities**, making it perfect for tasks such as **cataloging**, **organizing**, and **analyzing large sets of visual data**.

## Getting Started with PicTrace:
| **Operating System** | **Commands for Setup and Launch** |
|----------------------|----------------------------------|
| 🐧**Linux**            | ```bash sudo git clone https://github.com/Solrikk/PicTrace.git cd PicTrace sudo pip install poetry sudo poetry install sudo poetry run python3 main.py ``` |
| 🍎**macOS**            | ```bash sudo git clone https://github.com/Solrikk/PicTrace.git cd PicTrace sudo pip install poetry sudo poetry install sudo poetry run python3 main.py ``` |
| 🪟**Windows**          | Open Command Prompt as Administrator and run: ```bash git clone https://github.com/Solrikk/PicTrace.git cd PicTrace pip install poetry poetry install poetry run python main.py ``` |

![PicTrace Demo](https://github.com/Solrikk/PicTrace/blob/main/assets/gif/shell-PicTrrace.gif)

-----------------

## Features: ⚡
- **_Supports Multiple Technologies_** 

    _**Python**_ with these powerful libraries:
  - **`Tkinter:`** Provides a user-friendly graphical interface for the application, allowing users to interact with PicTrace seamlessly. [Details](https://docs.python.org/3/library/tkinter.html)
  - **`aiohttp:`** Perfect for handling asynchronous HTTP requests, such as downloading images by URL, making your app faster and more efficient. [Details](https://docs.aiohttp.org/en/stable/index.html)
  - **`OpenCV (cv2):`** A robust computer vision library used for advanced image processing, including loading, resizing, and comparing images, making it a critical component for your image-related tasks. [Details](https://docs.opencv.org/)
  - **`numpy:`** A versatile library for working with multi-dimensional arrays, often used alongside OpenCV for efficient image processing. [More Info](https://numpy.org/doc/)
  - **`scikit-image:`** Particularly, the `structural_similarity` (SSIM) function from this library is employed to compare the similarity of images, enhancing your application's accuracy in image matching. [Details](https://scikit-image.org/docs/stable/auto_examples/transform/plot_ssim.html)
  - **`hashlib:`** Utilized for generating unique hashes for each image, ensuring every image can be uniquely identified and efficiently managed. [More Info](https://docs.python.org/3/library/hashlib.html)

- **_Supports Multiple Indexes_** 🗂

  - **`Image Hashing:`** Generating unique hashes for images to ensure unique identification and efficient management.
  - **`Feature Extraction with ResNet50:`** Utilizes the ResNet50 model for extracting robust feature representations from images.
  - **`Cosine Similarity:`** Measuring similarity between images using cosine similarity on feature vectors extracted from the images.

-----------------

# Demos:

Curious to see how _PicTrace_ works in real-time? 

**Give it a try and see for yourself!**

![PicTrace Demo](https://github.com/Solrikk/PicTrace/blob/main/assets/gif/Pictrace.gif)

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
