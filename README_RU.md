<div align="center">
  <img src="assets/logo.svg" width="15%"/>
</div>

# Harmony-Image ⚡️

<div align="center">
  <h3>  English | <a href="README_FR.md"> Français </a> | <a href="README_JP.md"> 日本語 </a> | <a href="README_KR.md">한국어</a> | <a href="https://github.com/Solrikk/Harmony-Image/blob/main/README_RU.md">Русский</a> | <a href="README_CN.md">中文</a> </h3>
</div>

 **_Harmony-Image:_** Улучшите свой визуальный поиск. В основе Harmony-Image лежит усовершенствованная платформа, предназначенная для точного поиска похожих изображений. Используя возможности алгоритмов структурного сходства и сопоставления ключевых точек, этот инструмент предлагает быстрый и точный подход к сравнению изображений.

Независимо от того, загружаете ли вы изображения напрямую или используете URL-адреса, Harmony-Image эффективно просматривает обширную базу данных изображений, чтобы найти наиболее подходящие. Умелое использование асинхронной технологии обеспечивает быструю обработку, превращая ваш поиск в плавный и плодотворный процесс.

## Особенности
- **Поддерживает несколько технологий** ☄️

  - `Python` with libraries:
  - `FastAPI` for the web framework.
  - `aiohttp` for asynchronous HTTP requests.
  - `cv2` (OpenCV) for image processing.
  - `numpy` for numerical operations.
  - `skimage` for additional image processing techniques.
  - **Can also be used as a service**

- **Поддерживает несколько индексов** 🚀

  - `Structural Similarity Index (SSIM)` ([details](https://en.wikipedia.org/wiki/Structural_similarity_index_measure))
  - `Feature Matching with ORB (Oriented FAST and Rotated BRIEF) Descriptor` ([details](https://en.wikipedia.org/wiki/Oriented_FAST_and_rotated_BRIEF))
  - `Resizing and Grayscale Conversion` ([details](https://en.wikipedia.org/wiki/Grayscale))
  - `Hashing for Image Identification` 

#

![image](https://wikimedia.org/api/rest_v1/media/math/render/svg/4203f29f732e5cdc9d8a95907ef6d8e12f08ca09)

SSIM сравнивает закономерности изменения интенсивности пикселей, которые являются важными параметрами для человеческого зрения. Оценка SSIM варьируется от -1 до +1, где значение 1 указывает на идентичность изображений. Процесс можно разделить на три компонента:
1) **Сравнение яркости:** Это позволяет оценить общую яркость изображений. Яркость в SSIM измеряется как среднее значение всех значений в пикселях.
2) **Сравнение контрастности:** Сходство в контрастности измеряется с помощью дисперсии интенсивности пикселей (отклонения от среднего значения), позволяющей понять, насколько схожи схемы распределения света и тени между двумя изображениями.
3) **Структурное сравнение:** Сравнивает модели пространственного распределения пикселей, игнорируя различия в яркости и контрастности. Это делается путем вычисления ковариации между изображениями относительно их локальных средних значений.

![image](https://wikimedia.org/api/rest_v1/media/math/render/svg/96b4f1c3840c3707a93197798dcbfbfff24fa92b)
![image](https://wikimedia.org/api/rest_v1/media/math/render/svg/fcda97086476fa420b3b06568a0d202980a600d0)
![image](https://wikimedia.org/api/rest_v1/media/math/render/svg/1aebd62ba5b7e6ae47780ccfa659333f078d6eac)

Для сравнения изображений используется SSIM (индекс структурного сходства) для оценки сходства изображений, а также алгоритм ORB (Oriented FAST and Rotated BRIEF) для определения ключевых точек и их дескрипторов.

ORB (Oriented FAST and Rotated BRIEF) - это метод, используемый в компьютерном зрении, особенно популярный для задач, связанных с распознаванием объектов, сопоставлением изображений и отслеживанием. Он предназначен для быстрого поиска ключевых точек на изображениях и их описания таким образом, чтобы обеспечить эффективное сравнение. Давайте разберем то, что делает ORB, на более простые термины:

_ Используя алгоритм ORB, ключевые точки и дескрипторы определяются как для текущего, так и для целевого изображений._
![image](https://i.stack.imgur.com/spSvt.png)
Найденные ключевые точки сравниваются друг с другом для определения совпадений. Эти совпадения позволяют оценить сходство изображений с точки зрения, отличной от SSIM. Итоговая оценка сходства рассчитывается как среднее значение между оценкой SSIM и относительным количеством совпадающих ключевых точек (с использованием алгоритма ORB), что обеспечивает комплексный подход к анализу сходства изображений.

In your FastAPI application, both the SSIM and ORB methods are utilized to find images that are similar to an uploaded image. Here's a simplified explanation of how each method works in the context of your application and contributes to finding similar images:

## How SSIM Works in Harmony-Image:
1) **_Resizing Images:_** When comparing the uploaded image to each image in the database, both images are resized to the same dimensions (256x256 pixels). This standardizes the comparison, making it fair and more efficient since we're working with images of the same size.

2) **_Converting to Grayscale:_** Both images are converted to grayscale. This simplifies the comparison by focusing on the structure and intensity of light rather than being distracted by color differences.

3) **_Structural Similarity Comparison:_** The SSIM method then compares these grayscale images to assess their structural similarity. This involves analyzing how similar the patterns of light and shadow are between the two images, giving a score that reflects their similarity. A high score means the images are structurally similar.

## How ORB Works in Harmony-Image:
1) **_Detecting Key Points:_** ORB first identifies key points in both the uploaded image and each database image. These key points are distinctive spots that can be easily recognized and compared between images, such as corners and interesting textures.

2) **_Describing Key Points:_** For each key point detected, ORB generates a unique descriptor that summarizes the key point's characteristics. This descriptor is made rotation-invariant, meaning it describes the key point in a way that's consistent even if the image is rotated.

3) **_Matching Key Points:_** The application then matches key points between the uploaded image and each database image using these descriptors. The matching process involves finding key points in the database image that have descriptors similar to those in the uploaded image.

4) **_Scoring Matches:_** The more key points that match between two images, the higher the score of similarity based on ORB. This score reflects how many distinctive features are shared between the images.

## Combining SSIM and ORB:
 After calculating similarity scores using both SSIM and ORB for each image comparison, Harmony-Image averages these scores to get a final measure of similarity.
Images from the database are then ranked based on their final similarity scores, and the top 5 most similar images are selected.

 Final Selection of Similar Images:
The application filters out duplicate URLs to ensure a diverse set of similar images.
 It returns URLs of the top similar images, which can then be presented to the user.
 In essence, your application uses a combination of structural analysis (SSIM) and feature matching (ORB) to find and rank images in your database that are most similar to an image uploaded by the user. This dual approach leverages the strengths of both methods, ensuring a robust and nuanced comparison that goes beyond simple pixel-by-pixel analysis.
