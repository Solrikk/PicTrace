![로고](https://github.com/Solrikk/PicTrace/blob/main/assets/ORB/images/Orb5.png)

<div align="center">
  <h3> <a href="https://github.com/Solrikk/PicTrace/blob/main/README.md"> 영어 | <a href="https://github.com/Solrikk/PicTrace/blob/main/README_RU.md">러시아어</a> | <a href="https://github.com/Solrikk/PicTrace/blob/main/README_GE.md"> 독일어 </a> | <a href="https://github.com/Solrikk/PicTrace/blob/main/README_JP.md"> 일본어 </a> | <a href="README_KR.md">⭐한국어⭐</a> | <a href="README_CN.md">중국어</a> </h3>
</div>

-----------------

# PicTrace

🔎 **_PicTrace:_** 는 유사한 이미지를 정확하게 발견하기 위해 설계된 고급 플랫폼입니다. 구조적 유사성 및 키포인트 매칭 알고리즘을 활용하여, PicTrace는 이미지 비교를 위한 신속하고 정확한 방법을 제공합니다. 애플리케이션은 이미지를 직접 업로드하거나 URL을 통해 업로드할 수 있으며, 방대한 이미지 데이터베이스를 효율적으로 탐색하여 최적의 매치를 식별합니다. 비동기 기술을 사용한 덕분에 PicTrace는 빠른 처리를 보장하며, 원활하고 효과적인 시각적 검색 경험을 제공합니다.

## 특징 ⚙️
- **_다중 기술 지원_** ☄️

  _**파이썬**_ 과 라이브러리들:
  - `FastAPI` - 웹 애플리케이션 생성 및 HTTP 요청 처리에 사용됩니다. 비동기 연산을 지원합니다.
  - `aiohttp` - 비동기 HTTP 요청, 예를 들어 URL로 이미지를 다운로드 하는 등의 작업에 사용됩니다.
  - `OpenCV (cv2)`: - 이미지 로딩, 크기 조정, 비교 등 이미지 처리에 사용되는 `컴퓨터 비전` 라이브러리입니다.
  - `numpy` - 다차원 배열을 다루는 라이브러리로, OpenCV와 함께 이미지 처리 작업에 사용됩니다.
  - `skimage` - 특히, 이미지의 유사성을 비교하는데 사용되는 `structural_similarity` 함수가 있습니다.
  - `hashlib` - 각 이미지를 고유하게 식별할 수 있게 하는 이미지 해시를 생성하는 데 사용됩니다.

- **_다양한 인덱스 지원_** 🚀

- `구조적 유사성 지수 (SSIM)` ([상세 정보](https://en.wikipedia.org/wiki/Structural_similarity_index_measure))
- `ORB (Oriented FAST and Rotated BRIEF) 기술자를 사용한 특징 매칭` ([상세 정보](https://en.wikipedia.org/wiki/Oriented_FAST_and_rotated_BRIEF))
- `크기 조정 및 그레이스케일 변환` ([상세 정보](https://en.wikipedia.org/wiki/Grayscale))
- `이미지 식별을 위한 해싱`
    
## ⚠️ PicTrace 시작하기: ⚠️
_PicTrace는 개발 프로세스를 간소화하기 위해 설계된 강력한 이미지 추적 및 비교 도구입니다. 환경을 설정하고 애플리케이션을 성공적으로 실행하기 위해 다음 단계를 따르십시오._

### _PicTrace를 사용하기 위해 다음 구성 요소가 설치되어 있는지 확인하십시오:_
- `Python 3.8 이상`: PicTrace 개발에 사용되는 핵심 프로그래밍 언어입니다.
- `pip`: Python용 패키지 설치 프로그램으로, 소프트웨어 패키지를 관리하는 데 사용됩니다.
1. **_Clone the repository:_** ✔️

_First, you need to get a copy of the PicTrace source code on your local machine. Use the following command to clone the repository from `GitHub`:_

- `git clone https://github.com/<Solrikk>/PicTrace.git`
- `cd PicTrace`
2. **_Set up a virtual environment:_** ✔️

_A virtual environment is crucial for isolating the project dependencies from your global Python setup. This prevents version conflicts among different projects._

To create and activate a virtual environment, follow these commands:

```ShellScript
python -m venv venv
# Windows
venv\Scripts\activate
# Linux и MacOS
source venv/bin/activate
```
3. **_Install dependencies:_** ✔️
 - _This command reads the `requirements.txt` file and installs all listed packages, ensuring that PicTrace has all the necessary components to run smoothly._
```ShellScript
pip install -r requirements.txt
```
### _Launching the application:_
1. **_Start the server:_**
```ShellScript
python app.py
```
`After starting the server, the application will be available at http://localhost:5000 .`

## Results:
|Image 1 vs Image 2|Similar|Image|
|:-:|:-:|:-:|
|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/result_1.jpg" alt="" width="400"/>|YES|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/melbourne.jpg" alt="" width="200"/>|
|<img src="" alt="" width="400"/>|___|__|
|<img src="" alt="" width="400"/>|___|__|
|<img src="" alt="" width="400"/>|___|__|
|<img src="" alt="" width="400"/>|___|__|
|<img src="" alt="" width="400"/>|___|__|
|<img src="" alt="" width="400"/>|___|__|

## Examples: 📋
(**_code with comments_**)

```Python 
# 대상 이미지와 비교하여 이미지를 처리하는 비동기 함수를 정의합니다.
async def process_image(session, image_entry, target_image):
  try:
    # 웹페이지에서 이미지 URL 목록을 얻습니다.
    image_urls = await get_image_urls_from_page(session, image_entry["url"])
    for image_url in image_urls:
      # URL에서 현재 이미지를 다운로드합니다.
      current_image = await download_image(session, image_url)
      # 비교를 위한 최적의 크기를 결정합니다. 1024 픽셀을 초과하지 않습니다.
      optimal_size = max(max(target_image.shape[:2]),
                         max(current_image.shape[:2]))
      optimal_size = min(1024, optimal_size)
      # 비교를 위해 대상 및 현재 이미지를 최적 크기로 조정합니다.
      target_image_resized = cv2.resize(target_image,
                                        (optimal_size, optimal_size))
      current_image_resized = cv2.resize(current_image,
                                         (optimal_size, optimal_size))
      # 비교 과정을 위해 이미지를 그레이스케일로 변환합니다.
      target_gray = cv2.cvtColor(target_image_resized, cv2.COLOR_BGR2GRAY)
      current_gray = cv2.cvtColor(current_image_resized, cv2.COLOR_BGR2GRAY)
      # 두 이미지 간의 구조적 유사성 지수(SSIM)를 계산합니다.
      ssim_index = ssim(target_gray, current_gray)
      # 특징 추출을 위한 ORB 검출기를 초기화합니다.
      orb = cv2.ORB_create(nfeatures=500)
      # 두 이미지에 대해 키 포인트를 감지하고 설명자를 계산합니다.
      target_keypoints, target_descriptors = orb.detectAndCompute(
          target_gray, None)
      current_keypoints, current_descriptors = orb.detectAndCompute(
          current_gray, None)
      # 이미지 중 하나에서도 설명자를 찾지 못하는 경우 조기에 반환합니다.
      if target_descriptors is None or current_descriptors is None:
        return (0, image_entry["url"])
      # 좋은 매치를 찾기 위해 FLANN 기반 매쳐를 위한 설정 매개변수입니다.
      index_params = dict(algorithm=6,
                          table_number=6,
                          key_size=12,
                          multi_probe_level=1)
      search_params = dict(checks=50)
      flann = cv2.FlannBasedMatcher(index_params, search_params)
      # 두 이미지 간의 설명자를 매치하고 좋은 매치를 필터링합니다.
      matches = flann.knnMatch(target_descriptors, current_descriptors, k=2)
      good_matches = [m for m, n in matches if m.distance < 0.75 * n.distance]
      # 좋은 매치를 기반으로 특징 점수를 계산합니다.
      feature_score = len(good_matches) / float(len(target_keypoints))
      # RGB 채널에서 두 이미지에 대한 히스토그램을 계산합니다.
      target_hist = cv2.calcHist([target_image_resized], [0, 1, 2], None,
                                 [32, 32, 32], [0, 256, 0, 256, 0, 256])
      current_hist = cv2.calcHist([current_image_resized], [0, 1, 2], None,
                                  [32, 32, 32], [0, 256, 0, 256, 0, 256])
      # 히스토그램을 정규화합니다.
      cv2.normalize(target_hist, target_hist)
      cv2.normalize(current_hist, current_hist)
      # 상관 관계 방법을 사용하여 히스토그램을 비교합니다.
      hist_score = cv2.compareHist(target_hist, current_hist,
                                   cv2.HISTCMP_CORREL)
      # SSIM, 특징, 히스토그램 점수의 평균을 계산하여 최종 점수를 계산합니다.
      final_score = (feature_score + ssim_index + hist_score) / 3
      return (final_score, image_entry["url"])
  except Exception as e:
    # 처리 중에 발생한 모든 오류를 처리하고 제로 점수를 반환합니다.
    print(f"Failed to process image {image_entry['url']} due to {e}")
    return (0, image_entry["url"])
```

-----------------

![image](https://wikimedia.org/api/rest_v1/media/math/render/svg/4203f29f732e5cdc9d8a95907ef6d8e12f08ca09)

SSIM은 인간의 시각에 중요한 속성인 픽셀 강도 변화 패턴을 비교합니다. SSIM 점수는 `-1에서 +1`까지이며, `1의 값`은 이미지가 동일함을 나타냅니다. 이 과정은 세 가지 구성 요소로 나눌 수 있습니다:

<img src="https://github.com/Solrikk/EchoImage/blob/main/assets/ssim/ssim2.png" width="95%" /> 

1) 1) **_Luminance Comparison_** 은 이미지의 전체 밝기를 평가할 수 있게 합니다. SSIM에서의 밝기는 모든 픽셀 값의 평균으로 측정됩니다.
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

## _ORB (Oriented FAST and Rotated BRIEF)_ 
ORB method used in computer vision, particularly popular for tasks related to object recognition, image matching, and tracking. This method is focused on quickly finding key points on images and describing them in a way that allows for efficient comparison. Let's break down what ORB does with simpler examples:

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
