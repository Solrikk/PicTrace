![Логотип](https://github.com/Solrikk/PicTrace/blob/main/assets/OpenCV%20-%20result/bee.jpg)

<div align="center">
  <h3>
    <a href="https://github.com/Solrikk/PicTrace/blob/main/README.md">Английский</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/docs/readme/README_RU.md">✦ Русский ✦</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/docs/readme/README_GE.md">Немецкий</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/docs/readme//README_JP.md">Японский</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/docs/readme/README_KR.md">Корейский</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/docs/readme/README_CN.md">Китайский</a>
  </h3>
</div>

-----------------

# PicTrace 🔍

✨ **PicTrace** - это продвинутое приложение на **Python**, оснащенное **графическим пользовательским интерфейсом (GUI)** и **веб-версией на FastAPI**, которое позволяет пользователям идентифицировать **визуально похожие изображения** из обширного **фотоархива**. Используя возможности **глубокого обучения** и **сложные методы обработки изображений**, **PicTrace** предоставляет **быстрые и точные функции поиска**, что делает его идеальным для задач, таких как **каталогизация**, **организация** и **анализ больших наборов визуальных данных**.

# Демонстрации:

Хотите увидеть, как _PicTrace_ работает в реальном времени? 

**Попробуйте и убедитесь сами!**

https://pictrace.replit.app/

![Демо PicTrace](https://github.com/Solrikk/PicTrace/blob/main/assets/gif/Pictrace.gif)

## Начало работы с PicTrace:
| **Операционная система** | **Команды для установки и запуска** |
|--------------------------|-----------------------------------|
| 🐧**Linux**              | ```bash sudo git clone https://github.com/Solrikk/PicTrace.git cd PicTrace sudo pip install poetry sudo poetry install sudo poetry run python3 main.py ``` |
| 🍎**macOS**              | ```bash sudo git clone https://github.com/Solrikk/PicTrace.git cd PicTrace sudo pip install poetry sudo poetry install sudo poetry run python3 main.py ``` |
| 🪟**Windows**            | Откройте командную строку от имени администратора и выполните: ```bash git clone https://github.com/Solrikk/PicTrace.git cd PicTrace pip install poetry poetry install poetry run python main.py ``` |

![Демо PicTrace](https://github.com/Solrikk/PicTrace/blob/main/assets/gif/shell-PicTrrace.gif)

-----------------

## Функции ⚡

- **_Поддержка нескольких технологий_**
    - **Tkinter**: Обеспечивает удобный графический интерфейс для приложения, позволяя пользователям комфортно взаимодействовать с PicTrace. [Подробности](https://docs.python.org/3/library/tkinter.html)
    - **TensorFlow и Keras**: Используются для загрузки модели ResNet50 и извлечения признаков из изображений, обеспечивая высокую точность и эффективность в обработке изображений. [Подробности](https://www.tensorflow.org/api_docs/python/tf/keras)
    - **numpy**: Многофункциональная библиотека для работы с многомерными массивами, облегчающая эффективное вычисление и обработку данных. [Подробности](https://numpy.org/doc/)
    - **Pillow (PIL)**: Библиотека для обработки изображений, используемая для загрузки, изменения размера и сохранения изображений. [Подробности](https://pillow.readthedocs.io/en/stable/)
    - **pickle**: Модуль для сериализации и десериализации объектов Python, используемый для сохранения и загрузки заранее рассчитанных признаков изображений. [Подробности](https://docs.python.org/3/library/pickle.html)
    - **hashlib**: Используется для генерации уникальных хешей для каждого изображения, что позволяет эффективно управлять каждым изображением. [Подробности](https://docs.python.org/3/library/hashlib.html)
    - **scikit-image**: Конкретно функция `structural_similarity (SSIM)` из этой библиотеки используется для сравнения схожести изображений, повышая точность вашего приложения при сопоставлении изображений. [Подробности](https://scikit-image.org/docs/stable/api/skimage.metrics.html#skimage.metrics.structural_similarity)
    - **OpenCV (cv2)**: Надежная библиотека компьютерного зрения, используемая для сложной обработки изображений, включая загрузку, изменение размера и сравнение изображений. [Подробности](https://docs.opencv.org/master/)
    - **zipfile**: Обрабатывает ZIP-архивы содержащие изображения, облегчая управление коллекциями изображений. [Подробности](https://docs.python.org/3/library/zipfile.html)

-----------------

## Результаты: 
_Для сложных изображений с множеством деталей и возможным наличием шумов или искажений даже схожесть на уровне **20%** и выше может указывать на наличие значительных общих признаков. В таких случаях низкий процент схожести может быть ожидаем из-за сложности задачи и ограничений алгоритма._
|Изображение 1 vs Изображение 2|Схожесть|Изображение|
|:-:|:-:|:-:|
|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/result_3-1.png" alt="" width="500"/>|**27,12%**|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/palegleam.jpg" alt="" width="300"/>|
|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/result_2.png" alt="" width="500"/>|**25,44%**|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/ryan-yao.jpg" alt="" width="300"/>|
|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/result_3.png" alt="" width="500"/>|**44,16%**|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/taro-ohtani.jpg" alt="" width="300"/>|

## Примеры: 
(**_код с комментариями_**)

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
