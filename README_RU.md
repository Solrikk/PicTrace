<div align="center">
  <img src="assets/searching.png" width="30%"/>
</div>

<div align="center">
  <h3> <a href="https://github.com/Solrikk/Echo-Image/blob/main/README.md"> English | <a href="https://github.com/Solrikk/Echo-Image/blob/main/README_RU.md">Русский</a> | <a href="https://github.com/Solrikk/Echo-Image/blob/main/README_GE.md"> Deutsch </a> | <a href="https://github.com/Solrikk/Echo-Image/blob/main/README_JP.md"> 日本語 </a> | <a href="README_KR.md">한국어</a> | <a href="README_CN.md">中文</a> </h3>
</div>

-----------------

# Echo-Image ⚡️

 **_EchoImage:_** это передовая платформа, предназначенная для точного поиска похожих изображений. Используя алгоритмы сравнения структурного сходства и сопоставления ключевых точек, EchoImage обеспечивает быстрый и точный метод сравнения изображений. Приложение поддерживает загрузку изображений напрямую или через URL, эффективно просматривая огромную базу данных изображений для определения наилучших совпадений. Благодаря использованию асинхронных технологий, EchoImage обеспечивает быструю обработку, предлагая бесшовный и эффективный опыт визуального поиска.

**_Вы можете создать базу данных здесь_** - ([подробности](https://github.com/Solrikk/ImageSpaceDB))

## Возможности
- **_Поддерживает множество технологий_** ☄️

    _**Python**_ с библиотеками::
  - `FastAPI` для веб-фреймворка.
  - `aiohttp` для асинхронных HTTP-запросов.
  - `cv2` (OpenCV) для обработки изображений.
  - `numpy` для выполнения числовых операций.
  - `skimage` для дополнительных методов обработки изображений.

- **_Поддерживает множество индексов_** 🚀

  - `Индекс структурного сходства (SSIM)` ([подробности](https://en.wikipedia.org/wiki/Structural_similarity_index_measure))
  - `Сопоставление признаков с использованием дескриптора ORB (Oriented FAST and Rotated BRIEF)` ([подробности](https://en.wikipedia.org/wiki/Oriented_FAST_and_rotated_BRIEF))
  - `Изменение размера и преобразование в оттенки серого` ([подробности](https://en.wikipedia.org/wiki/Grayscale))
  - `Хеширование для идентификации изображений`
    
# Примеры
`Пример на Python` [[больше информации](https://github.com/Solrikk/EchoImage/blob/main/main.py)]

```Python
async def process_image(session, image_entry, target_image):
  try:
    current_image = await download_image(session, image_entry["url"])
    optimal_size = max(max(target_image.shape[:2]),
                       max(current_image.shape[:2]))
    optimal_size = min(1024, optimal_size)
    target_image_resized = cv2.resize(target_image,
                                      (optimal_size, optimal_size))
    current_image_resized = cv2.resize(current_image,
                                       (optimal_size, optimal_size))
    target_gray = cv2.cvtColor(target_image_resized, cv2.COLOR_BGR2GRAY)
    current_gray = cv2.cvtColor(current_image_resized, cv2.COLOR_BGR2GRAY)
    ssim_index = ssim(target_gray, current_gray)
    orb = cv2.ORB_create(nfeatures=500)
    target_keypoints, target_descriptors = orb.detectAndCompute(
        target_gray, None)
    current_keypoints, current_descriptors = orb.detectAndCompute(
        current_gray, None)
    if target_descriptors is None or current_descriptors is None:
      return (0, image_entry["url"])
    index_params = dict(algorithm=6,
                        table_number=6,
                        key_size=12,
                        multi_probe_level=1)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
```

#

![image](https://wikimedia.org/api/rest_v1/media/math/render/svg/4203f29f732e5cdc9d8a95907ef6d8e12f08ca09)

SSIM сравнивает паттерны изменений интенсивности пикселей, которые являются важными атрибутами для человеческого зрения. Оценка SSIM находится в диапазоне от `-1 до +1`, где `значение 1` указывает на идентичные изображения. Процесс можно разбить на три компонента:

<img src="https://github.com/Solrikk/EchoImage/blob/main/assets/ssim/ssim2.png" width="95%" /> 

1) **_Сравнение яркости_** позволяет оценить общую яркость изображений. Яркость в SSIM измеряется как среднее всех значений пикселей.

```Python
target_gray = cv2.cvtColor(target_image_resized, cv2.COLOR_BGR2GRAY)
current_gray = cv2.cvtColor(current_image_resized, cv2.COLOR_BGR2GRAY)
ssim_index = ssim(target_gray, current_gray)
```

2) **_Сравнение контраста_** измеряется через дисперсию интенсивности пикселей (отклонения от среднего значения), понимая, насколько похожи паттерны распределения света и тени между двумя изображениями.
3) **_Сравнение структуры_** cравнивает паттерны пространственного распределения пикселей, игнорируя изменения в яркости и контрасте. Это делается путем расчета ковариации между изображениями относительно их локальных средних значений.

![image](https://wikimedia.org/api/rest_v1/media/math/render/svg/96b4f1c3840c3707a93197798dcbfbfff24fa92b)
![image](https://wikimedia.org/api/rest_v1/media/math/render/svg/fcda97086476fa420b3b06568a0d202980a600d0)
![image](https://wikimedia.org/api/rest_v1/media/math/render/svg/1aebd62ba5b7e6ae47780ccfa659333f078d6eac)

Для сравнения изображений используется Индекс структурного сходства **(SSIM)** для оценки сходства между изображениями, а также алгоритм **ORB (Oriented FAST and Rotated BRIEF)** для обнаружения ключевых точек и их описаний.

## _ORB (Oriented FAST and Rotated BRIEF)_ 
ORB метод, используемый в компьютерном зрении, особенно популярный для задач, связанных с распознаванием объектов, сопоставлением изображений и отслеживанием. Этот метод сосредоточен на быстром поиске ключевых точек на изображениях и описании их таким образом, чтобы можно было эффективно сравнивать их. ORB обеспечивает быстрый и эффективный способ сопоставления изображений, несмотря на изменения в угле обзора, масштабе или освещении.

<img src="https://github.com/Solrikk/EchoImage/blob/main/assets/ORB/ORB3.png" width="95%" /> 

1) **Oriented FAST (Features from Accelerated Segment Test):** This part is responsible for detecting points of interest (or key points) on the image. It quickly identifies corners or edges that stand out in comparison to their surrounding areas. This way, significant or unique sections of the image can be identified.

2) **Rotated BRIEF (Binary Robust Independent Elementary Features):** After key points have been found, it's necessary to create a description of each to allow comparison with key points from another image. BRIEF generates a brief binary description of the points but lacks resistance to image rotation. This is where the "rotated" part comes in - ORB adds the ability to stably describe points even when images are rotated.

By combining these two approaches, ORB provides a fast and efficient way of matching images despite changes in viewing angle, scale, or lighting.

_Using the ORB algorithm, key points and descriptors are determined for both the current and target images._

The found key points are compared with each other to determine matches. These matches allow assessing the similarity of images from a perspective other than SSIM. The final similarity score is calculated as the average between the SSIM score and the relative number of matching key points (using the ORB algorithm), providing a comprehensive approach to analyzing the similarity of images.

EchoImage application, both the SSIM and ORB methods are utilized to find images that are similar to an uploaded image. Here's a simplified explanation of how each method works in the context of your application and contributes to finding similar images:

## How SSIM Works in EchoImage:
1) **_Resizing Images:_** When comparing the uploaded image to each image in the database, both images are resized to the same dimensions `(256x256 pixels)`. This standardizes the comparison, making it fair and more efficient since we're working with images of the same size.

2) **_Converting to Grayscale:_** Both images are converted to grayscale. This simplifies the comparison by focusing on the structure and intensity of light rather than being distracted by color differences.

3) **_Structural Similarity Comparison:_** The SSIM method then compares these grayscale images to assess their structural similarity. This involves analyzing how similar the patterns of light and shadow are between the two images, giving a score that reflects their similarity. A high score means the images are structurally similar.

## How ORB Works in EchoImage:
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
