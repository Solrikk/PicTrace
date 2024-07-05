![Logo](https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/orb6.png)

<div align="center">
  <h3>
    <a href="https://github.com/Solrikk/PicTrace/blob/main/README.md">English</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/README_RU.md">⭐Russian⭐</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/README_GE.md">German</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/README_JP.md">Japanese</a> |
    <a href="README_KR.md">Korean</a> |
    <a href="README_CN.md">Chinese</a>
  </h3>
</div>

-----------------

# PicTrace 🔍

_**PicTrace**_ — это высокоэффективная платформа для сопоставления изображений, использующая компьютерное зрение с библиотекой _**OpenCV**_, глубокое обучение с _**TensorFlow**_ и моделью _**ResNet50**_, асинхронную обработку с _**aiohttp**_ и веб-фреймворком _**FastAPI**_ для быстрого и точного поиска изображений. PicTrace позволяет пользователям загружать изображения напрямую или предоставлять URL-адреса, быстро сканируя обширную базу данных для нахождения похожих изображений. Асинхронная обработка обеспечивает плавный и быстрый визуальный поиск, улучшая пользовательский опыт.

![PicTrace Demo](https://github.com/Solrikk/PicTrace/blob/main/assets/gif/Pictrace.gif)

## Содержание
1. [Особенности ⚡](#особенности-⚡)
2. [Начало работы с PicTrace 🚀](#начало-работы-с-pictrace-🚀)
   - [Предварительные требования](#предварительные-требования)
   - [Шаги для настройки PicTrace](#шаги-для-настройки-pictrace)
3. [Результаты: 👨‍💻](#результаты-👨‍💻)
4. [Примеры: 📋](#примеры-📋)
5. [Как SSIM работает в PicTrace](#как-ssim-работает-в-pictrace)
6. [Как ORB работает в PicTrace](#как-orb-работает-в-pictrace)
7. [Комбинирование SSIM и ORB](#комбинирование-ssim-и-orb)
8. [Окончательный выбор похожих изображений](#окончательный-выбор-похожих-изображений)

## Особенности ⚡
- **_Поддержка множества технологий_** 💼

    _**Python**_ с этими мощными библиотеками:
  - **`FastAPI:`** Идеален для создания веб-приложений и обработки HTTP-запросов, FastAPI известен своей высокой производительностью и поддержкой асинхронных операций. [Подробнее](https://fastapi.tiangolo.com/)
  - **`aiohttp:`** Идеален для обработки асинхронных HTTP-запросов, таких как загрузка изображений по URL, делая ваше приложение быстрее и эффективнее. [Подробнее](https://docs.aiohttp.org/en/stable/index.html)
  - **`OpenCV (cv2):`** Мощная библиотека компьютерного зрения, используемая для продвинутой обработки изображений, включая загрузку, изменение размера и сравнение изображений, что делает ее важным компонентом для ваших задач, связанных с изображениями. [Подробнее](https://docs.opencv.org/)
  - **`numpy:`** Универсальная библиотека для работы с многомерными массивами, часто используемая вместе с OpenCV для эффективной обработки изображений. [Подробнее](https://numpy.org/doc/)
  - **`scikit-image:`** В частности, функция `structural_similarity` (SSIM) из этой библиотеки используется для сравнения сходства изображений, повышая точность вашего приложения в сопоставлении изображений. [Подробнее](https://scikit-image.org/docs/stable/auto_examples/transform/plot_ssim.html)
  - **`hashlib:`** Используется для генерации уникальных хэшей для каждого изображения, что позволяет уникально идентифицировать и эффективно управлять каждым изображением. [Подробнее](https://docs.python.org/3/library/hashlib.html)

- **_Поддержка множества индексов_** 🗂️

  - **`Хэширование изображений:`** Генерация уникальных хэшей для изображений с целью уникальной идентификации и эффективного управления.
  - **`Извлечение признаков с ResNet50:`** Использование модели ResNet50 для извлечения надежных признаков из изображений.
  - **`Косинусное сходство:`** Измерение сходства между изображениями с использованием косинусного сходства на основе векторов признаков, извлеченных из изображений.

-----------------

## Начало работы с PicTrace 🚀
_PicTrace — это мощный инструмент для трассировки и сравнения изображений, разработанный для упрощения вашего процесса разработки. Следуйте этим шагам, чтобы настроить ваше окружение и успешно запустить приложение._

### Предварительные требования
Для работы с PicTrace убедитесь, что у вас установлены следующие компоненты:

- **Python 3.8 или выше:** PicTrace построен на Python. Вы можете загрузить последнюю версию Python с [официального сайта](https://www.python.org/downloads/).
- **pip:** Установщик пакетов для Python, который идет в комплекте с Python 3.4 и выше. Мы будем использовать pip для установки необходимых зависимостей.
- **Git:** Требуется для клонирования репозитория PicTrace. Если Git не установлен на вашем компьютере, следуйте инструкциям по установке на [официальном сайте Git](https://git-scm.com/downloads).

### Шаги для настройки PicTrace
1. **Клонируйте репозиторий**

_Сначала получите копию исходного кода PicTrace на вашем локальном компьютере. Используйте следующие команды для клонирования репозитория с GitHub:_

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

## Результаты: 👨‍💻
_Для сложных изображений с большим количеством деталей и возможным наличием шумов или искажений, даже сходство на уровне **20%** и выше может указывать на наличие значительных общих черт. В таких случаях можно ожидать низкий процент сходства из-за сложности задачи и ограничений алгоритма._
|Image 1 vs Image 2|Similar|Image|
|:-:|:-:|:-:|
|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/result_3-1.png" alt="" width="500"/>|**27,12%**|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/palegleam.jpg" alt="" width="300"/>|
|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/result_2.png" alt="" width="500"/>|**25,44%**|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/ryan-yao.jpg" alt="" width="300"/>|
|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/result_3.png" alt="" width="500"/>|**44,16%**|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/taro-ohtani.jpg" alt="" width="300"/>|

## Examples: 📋
(**_code with comments_**)

```Python 
async def find_similar_images(file_path):
    # Загрузка данных из базы данных, содержащей информацию об изображениях.
    db_data = load_db()
    # Чтение целевого изображения из указанного пути к файлу.
    target_image = cv2.imread(file_path)
    # Извлечение признаков из целевого изображения с использованием предобученной модели.
    target_features = extract_features(target_image)
    # Создание асинхронной сессии aiohttp для обработки HTTP-запросов.
    async with aiohttp.ClientSession() as session:
        # Создание асинхронных задач для функции compare_images для каждого изображения в базе данных.
        tasks = [
            compare_images(session, entry, target_features) for entry in db_data
            if "url" in entry  # Выполнение сравнения только для записей, содержащих URL изображения.
        ]
        # Ожидание выполнения всех задач и сбор результатов.
        results = await asyncio.gather(*tasks)
    # Фильтрация результатов, оставляя только те, у которых оценка сходства больше 0.
    valid_results = filter(lambda x: x[0] > 0, results)   
    # Сортировка отфильтрованных результатов по оценке сходства в порядке убывания и выбор топ-5.
    sorted_results = sorted(valid_results, key=lambda x: x[0], reverse=True)[:5]
    # Создание списка для хранения URL похожих изображений.
    similar_images = []
    for result in sorted_results:
        if result[1]:
            similar_images.append(result[1])
    # Возвращение списка URL похожих изображений.
    return similar_images
```

## _OpenCV (Open Source Computer Vision Library) 🌐:_

**OpenCV** является мощной библиотекой компьютерного зрения, которая предоставляет инструменты для обработки изображений и видео. Она широко используется в областях, связанных с машинным зрением, распознаванием изображений, видеосъемкой и многими другими. Библиотека включает широкий спектр алгоритмов для анализа изображений, таких как обнаружение объектов, распознавание лиц, трассировка движений, обработка видео и т.д.

Основные функции **OpenCV** включают:
1. **Загрузка и сохранение изображений 🖼️**: Поддерживает различные форматы изображений и позволяет легко загружать, изменять размеры и сохранять изображения, что актуально для работы с большими наборами данных.
2. **Обработка изображений ✨**: Предоставляет функции для фильтрации изображений, преобразования в оттенки серого, изменения размера, вращения и других манипуляций. Это важно для предварительной обработки изображений перед анализом.
3. **Обнаружение объектов 🔍**: Включает алгоритмы для обнаружения краев, углов и других ключевых точек, что помогает в идентификации и отслеживании определенных объектов в кадре.
4. **Распознавание объектов 👁️**: Предоставляет инструменты для распознавания лиц, жестов и других объектов на изображениях и видео, что является ключевым для многих приложений компьютерного зрения.

## Модель Нейросети (ResNet50) 🧠:
Модель **ResNet50** (Residual Network) является одной из самых популярных и мощных архитектур глубокого обучения для задач классификации изображений и извлечения признаков. Ваша модель нейросети **ResNet50** предоставляет следующие преимущества:

1. **Глубокие остаточные сети**: Использует остаточные сети для облегчения обучения глубоких нейронных сетей, что позволяет строить очень глубокие архитектуры без риска затухания градиента.
2. **Предварительно обученные веса**: Модель поставляется с предварительно обученными весами на наборе данных ImageNet, что позволяет значительно ускорить обучение и улучшить точность при классификации изображений.
3. **Извлечение признаков**: Модель может использоваться для извлечения признаков из изображений, что полезно для задач, связанных с когнитивным исследованием данных и машинным обучением.
4. **Гибкость применения**: Модель может быть использована как для классификации, так и для задачи извлечения и сравнения признаков изображений, что подходит для вашего приложения.

Вместе **OpenCV** и **ResNet50** могут использоваться для создания мощных приложений компьютерного зрения, которые могут анализировать визуальные данные и выполнять сложные задания, такие как автоматическое распознавание и классификация объектов.
 
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
