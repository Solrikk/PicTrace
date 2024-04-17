<div align="center">
  <img src="assets/searching.png" width="30%"/>
</div>

# Echo-Image ⚡️

<div align="center">
  <h3> <a href="https://github.com/Solrikk/Echo-Image/blob/main/README.md"> English | <a href="https://github.com/Solrikk/Echo-Image/blob/main/README_GE.md"> Deutsch </a> | <a href="https://github.com/Solrikk/Echo-Image/blob/main/README_JP.md"> 日本語 </a> | <a href="README_KR.md">한국어</a> | <a href="https://github.com/Solrikk/Echo-Image/blob/main/README_RU.md">Русский</a> | <a href="README_CN.md">中文</a> </h3>
</div>

 **_EchoImage:_** является передовой платформой, предназначенной для точного обнаружения схожих изображений. Используя алгоритмы структурного сходства и сопоставления ключевых точек, EchoImage обеспечивает быструю и точную методику сравнения изображений. Приложение поддерживает загрузку изображений напрямую или по URL, эффективно осуществляя поиск по обширной базе данных изображений для определения наилучших совпадений. Благодаря использованию асинхронных технологий, EchoImage обеспечивает быструю обработку, предлагая бесшовный и эффективный опыт визуального поиска.

**_You can create a database from here_** - ([details](https://github.com/Solrikk/ImageSpaceDB))

## Features
- **_Supports Multiple-Technologies_** ☄️

  - `Python` with libraries:
  - `FastAPI` for the web framework.
  - `aiohttp` for asynchronous HTTP requests.
  - `cv2` (OpenCV) for image processing.
  - `numpy` for numerical operations.
  - `skimage` for additional image processing techniques.
  - **Can also be used as a service**

- **_Supports Multiple-Indexes_** 🚀

  - `Structural Similarity Index (SSIM)` ([details](https://en.wikipedia.org/wiki/Structural_similarity_index_measure))
  - `Feature Matching with ORB (Oriented FAST and Rotated BRIEF) Descriptor` ([details](https://en.wikipedia.org/wiki/Oriented_FAST_and_rotated_BRIEF))
  - `Resizing and Grayscale Conversion` ([details](https://en.wikipedia.org/wiki/Grayscale))
  - `Hashing for Image Identification` 

- **_Portable_** 💼

  - Supports `WebAssembly`
  - Supports `Windows`, `Linux` and `OS X`
  - Supports `IOS` and `Android` (WIP)
  - Supports `no_std` (WIP, partial)

# Examples
`Python` example** [[more info](https://github.com/Solrikk/EchoImage/blob/main/main.py)]

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

SSIM сравнивает модели изменений интенсивности пикселей, которые являются важными атрибутами для человеческого зрения. Оценка SSIM варьируется от `-1 до +1`, где значение `1` указывает на идентичные изображения. Процесс можно разбить на три компонента:
1) **_Сравнение Яркости:_** Позволяет оценить общую яркость изображений. Яркость в SSIM измеряется как среднее значение всех пикселей.

```Python
target_gray = cv2.cvtColor(target_image_resized, cv2.COLOR_BGR2GRAY)
current_gray = cv2.cvtColor(current_image_resized, cv2.COLOR_BGR2GRAY)
ssim_index = ssim(target_gray, current_gray)
```

2) **_Сравнение Контрастности:_** - Сходство по контрастности измеряется через дисперсию интенсивности пикселей (отклонения от среднего значения), позволяя понять, насколько схожи узоры распределения света и тени между двумя изображениями.
3) **_Сравнение Структуры:_** Сравнивает узоры пространственного распределения пикселей, игнорируя изменения в яркости и контрастности. Это делается путем вычисления ковариации между изображениями относительно их локальных средних значений.

![image](https://wikimedia.org/api/rest_v1/media/math/render/svg/96b4f1c3840c3707a93197798dcbfbfff24fa92b)
![image](https://wikimedia.org/api/rest_v1/media/math/render/svg/fcda97086476fa420b3b06568a0d202980a600d0)
![image](https://wikimedia.org/api/rest_v1/media/math/render/svg/1aebd62ba5b7e6ae47780ccfa659333f078d6eac)

Для сравнения изображений используется Индекс Структурного Сходства (SSIM) для оценки сходства между изображениями, а также алгоритм ORB (Oriented FAST and Rotated BRIEF) для обнаружения ключевых точек и их описаний.

**_ORB (Oriented FAST and Rotated BRIEF)_** — это метод, используемый в компьютерном зрении, особенно популярный для задач, связанных с распознаванием объектов, сопоставлением изображений и отслеживанием. Этот метод сосредоточен на быстром поиске ключевых точек на изображениях и их описании таким образом, чтобы можно было эффективно их сравнить. Давайте разберем, что делает ORB, на более простых примерах:

1) **_Ориентированный FAST (Особенности из Ускоренного Теста Сегментов):_** Эта часть отвечает за обнаружение интересующих точек (или ключевых точек) на изображении. Она быстро определяет углы или края, которые выделяются на фоне окружающих их областей. Таким образом, можно идентифицировать значимые или уникальные секции изображения.

2) **_Вращенный BRIEF (Бинарные Робастные Независимые Элементарные Особенности):_** После того, как ключевые точки были найдены, необходимо создать описание каждой из них для возможности сравнения с ключевыми точками из другого изображения. BRIEF генерирует краткое бинарное описание точек, но не устойчив к вращению изображения. Здесь на сцену выходит "вращенность" - ORB добавляет возможность стабильно описывать точки даже при вращении изображений.

Объединяя эти два подхода, ORB обеспечивает быстрый и эффективный способ сопоставления изображений, несмотря на изменения в угле обзора, масштабе или освещении.

_С использованием алгоритма ORB определяются ключевые точки и дескрипторы как для текущего, так и для целевого изображений._
![image](https://i.stack.imgur.com/spSvt.png)

Найденные ключевые точки сравниваются друг с другом для определения совпадений. Эти совпадения позволяют оценить сходство изображений с точки зрения, отличной от SSIM. Итоговый балл сходства рассчитывается как среднее значение между баллом SSIM и относительным количеством совпадающих ключевых точек (с использованием алгоритма ORB), обеспечивая комплексный подход к анализу сходства изображений.

В приложении EchoImage используются как методы SSIM, так и ORB для поиска изображений, похожих на загруженное. Вот упрощенное объяснение того, как каждый метод работает в контексте вашего приложения и способствует поиску похожих изображений:

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
