![Logo](https://github.com/Solrikk/PicTrace/blob/main/assets/OpenCV%20-%20result/bee.jpg)

<div align="center">
  <h3>
    <a href="https://github.com/Solrikk/PicTrace/blob/main/README.md">⭐ English ⭐</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/README_RU.md">Russian</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/README_GE.md">German</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/README_JP.md">Japanese</a> |
    <a href="README_KR.md">Korean</a> |
    <a href="README_CN.md">Chinese</a>
  </h3>
</div>

-----------------

# PicTrace 🔍

_**PicTrace**_는 _**OpenCV**_를 사용한 컴퓨터 비전, _**TensorFlow**_ 및 _**ResNet50 모델**_을 사용한 딥러닝, _**aiohttp**_를 사용한 비동기 처리, 빠르고 정확한 이미지 검색을 위한 _**FastAPI**_ 웹 프레임워크를 활용한 고성능 이미지 매칭 플랫폼입니다. PicTrace는 사용자가 이미지를 직접 업로드하거나 URL을 제공할 수 있게 하며, 방대한 데이터베이스를 신속하게 스캔하여 유사한 이미지를 찾습니다. 비동기 처리는 매끄럽고 빠른 비주얼 검색을 보장하여 사용자 경험을 향상시킵니다.

# 온라인 데모:

_PicTrace_가 실시간으로 어떻게 작동하는지 궁금하신가요? 

온라인 데모를 확인하고 이미지 매칭 플랫폼의 기능을 직접 체험해 보세요.

[온라인 데모](https://PicTrace.replit.app) - **직접 시도해 보세요!**

![PicTrace Demo](https://github.com/Solrikk/PicTrace/blob/main/assets/gif/Pictrace.gif)

## 목차:
1. [기능 ⚡](#features-⚡)
2. [PicTrace 시작하기 🚀](#getting-started-with-pictrace-🚀)
   - [필수 조건](#prerequisites)
   - [PicTrace 설정 단계](#steps-to-set-up-pictrace)
   - [애플리케이션 실행](#launching-the-application)
3. [결과: 👨‍💻](#results-👨‍💻)
4. [예제: 📋](#examples-📋)
   - [주석이 포함된 코드](#code-with-comments)
5. [PicTrace에서 SSIM이 작동하는 방법](#how-ssim-works-in-pictrace)
6. [PicTrace에서 ORB가 작동하는 방법](#how-orb-works-in-pictrace)
7. [SSIM 및 ORB 결합](#combining-ssim-and-orb)
8. [OpenCV (오픈 소스 컴퓨터 비전 라이브러리) 🌐](#opencv-open-source-computer-vision-library-🌐)
9. [신경망 모델 (ResNet50) 🧠](#neural-network-model-resnet50-🧠)
10. [유사한 이미지의 최종 선택](#final-selection-of-similar-images)

## 기능: ⚡
- **_여러 기술 지원_** 💼

    _**Python**_과 함께 사용하는 강력한 라이브러리:
  - **`FastAPI:`** 웹 애플리케이션 생성과 HTTP 요청 처리를 위한 이상적인 선택. FastAPI는 고성능과 비동기 작업 지원으로 유명합니다. [자세히 보기](https://fastapi.tiangolo.com/)
  - **`aiohttp:`** URL을 통해 이미지를 다운로드하는 등 비동기 HTTP 요청 처리를 완벽하게 지원하여 애플리케이션을 더 빠르고 효율적으로 만듭니다. [자세히 보기](https://docs.aiohttp.org/en/stable/index.html)
  - **`OpenCV (cv2):`** 고급 이미지 처리를 위한 강력한 컴퓨터 비전 라이브러리로, 이미지 로드, 리사이징 및 비교 등을 포함한 이미지 관련 작업에 중요한 구성 요소입니다. [자세히 보기](https://docs.opencv.org/)
  - **`numpy:`** 다차원 배열 작업을 위한 다재다능한 라이브러리로, OpenCV와 함께 사용하여 효율적인 이미지 처리를 수행합니다. [자세히 보기](https://numpy.org/doc/)
  - **`scikit-image:`** 특히, 이 라이브러리의 `structural_similarity` (SSIM) 함수는 이미지 유사성을 비교하는 데 사용되어 애플리케이션의 정확성을 향상시킵니다. [자세히 보기](https://scikit-image.org/docs/stable/auto_examples/transform/plot_ssim.html)
  - **`hashlib:`** 각 이미지에 고유한 해시를 생성하여 모든 이미지를 고유하게 식별하고 효율적으로 관리할 수 있습니다. [자세히 보기](https://docs.python.org/3/library/hashlib.html)

- **_다중 인덱스 지원_** 🗂️

  - **`이미지 해싱:`** 이미지를 고유하게 식별하고 효율적으로 관리하기 위해 고유한 해시를 생성합니다.
  - **`ResNet50을 사용한 특징 추출:`** ResNet50 모델을 사용하여 이미지에서 강력한 특징 표현을 추출합니다.
  - **`코사인 유사도:`** 이미지에서 추출한 특징 벡터를 기반으로 코사인 유사도를 사용하여 이미지 간 유사성을 측정합니다.

-----------------

## PicTrace 시작하기: 🚀
_PicTrace는 개발 프로세스를 간소화하도록 설계된 강력한 이미지 추적 및 비교 도구입니다. 다음 단계를 수행하여 환경을 설정하고 애플리케이션을 성공적으로 실행하십시오._

### 필수 조건
PicTrace를 사용하려면 다음 구성 요소가 설치되어 있는지 확인하세요:

- **Python 3.8 이상:** PicTrace는 Python으로 구축되었습니다. [공식 웹사이트](https://www.python.org/downloads/)에서 최신 버전의 Python을 다운로드할 수 있습니다.
- **pip:** Python 패키지 설치 관리자이며, Python 3.4 이상에 기본 설치되어 있습니다. 필요한 종속성을 설치하는 데 pip를 사용합니다.
- **Git:** PicTrace 저장소를 복제하는 데 필요합니다. 시스템에 Git이 설치되어 있지 않다면 [Git의 공식 사이트](https://git-scm.com/downloads)에서 설치 지침을 따르십시오.

### PicTrace 설정 단계:
1. **저장소 복제**

_먼저, 로컬 머신에 PicTrace 소스 코드를 복사합니다. GitHub에서 저장소를 복제하려면 다음 명령을 사용하십시오:_

```git clone https://github.com/solrikk/PicTrace.git```

2. **_가상 환경 설정:_** ✔️

_가상 환경은 프로젝트 종속성을 글로벌 Python 설정에서 분리하여, 다양한 프로젝트 간 버전 충돌을 방지하는 데 중요합니다. 가상 환경을 만들고 활성화하려면 다음 명령을 실행하십시오:_

가상 환경을 만들고 활성화하려면 다음 명령을 따르십시오:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux 및 MacOS
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

## 결과: 👨‍💻
_상세한 정보와 노이즈 또는 왜곡이 있을 가능성이 있는 복잡한 이미지에 대해서도, 유사도가 **20%** 이상이라면 중요한 공통 요소가 있음을 나타낼 수 있습니다. 이러한 경우, 작업의 복잡성과 알고리즘의 한계로 인해 낮은 유사도 비율이 예상될 수 있습니다._
|이미지 1 vs 이미지 2|유사도|이미지|
|:-:|:-:|:-:|
|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/result_3-1.png" alt="" width="500"/>|**27.12%**|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/palegleam.jpg" alt="" width="300"/>|
|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/result_2.png" alt="" width="500"/>|**25.44%**|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/ryan-yao.jpg" alt="" width="300"/>|
|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/result_3.png" alt="" width="500"/>|**44.16%**|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/taro-ohtani.jpg" alt="" width="300"/>|

## 예제: 📋
(**_주석이 포함된 코드_**)

```Python 
async def find_similar_images(file_path):
    # 이미지에 대한 정보를 포함하는 데이터베이스에서 데이터를 로드합니다.
    db_data = load_db()
    # 지정된 파일 경로에서 대상 이미지를 읽어들입니다.
    target_image = cv2.imread(file_path)
    # 미리 학습된 모델을 사용하여 대상 이미지에서 특징을 추출합니다.
    target_features = extract_features(target_image)
    # HTTP 요청 처리를 위한 aiohttp 비동기 세션을 만듭니다.
    async with aiohttp.ClientSession() as session:
        # 데이터베이스의 각 이미지에 대해 compare_images 함수에 대한 비동기 작업을 만듭니다.
        tasks = [
            compare_images(session, entry, target_features) for entry in db_data
            if "url" in entry  # 이미지 URL을 포함하는 항목에만 비교를 수행합니다.
        ]
        # 모든 작업이 완료되기를 기다리고 결과를 모읍니다.
        results = await asyncio.gather(*tasks)
    # 유사도 점수가 0보다 큰 결과만 유지하여 필터링합니다.
    valid_results = filter(lambda x: x[0] > 0, results)   
    # 유효한 결과를 유사도 점수 순으로 내림차순 정렬하고 상위 5개를 선택합니다.
    sorted_results = sorted(valid_results, key=lambda x: x[0], reverse=True)[:5]
    # 유사한 이미지의 URL을 저장할 리스트를 만듭니다.
    similar_images = []
    for result in sorted_results:
        if result[1]:
            similar_images.append(result[1])
    # 유사한 이미지의 URL 리스트를 반환합니다.
    return similar_images
```

-----------------

## _OpenCV (오픈 소스 컴퓨터 비전 라이브러리) 🌐:_

<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/OpenCV%20-%20result/parrot.png" width="95%" /> 

**OpenCV**는 이미지 및 비디오 처리를 위한 강력한 컴퓨터 비전 라이브러리입니다. 기계 비전, 이미지 인식, 비디오 분석 등과 관련된 분야에서 널리 사용됩니다. 라이브러리는 이미지 분석을 위한 다양한 알고리즘을 포함하고 있으며, 예를 들어 객체 검출, 얼굴 인식, 모션 추적, 비디오 조작 등이 있습니다.

**OpenCV**의 주요 기능은 다음과 같습니다:
1. **이미지 로드 및 저장 🖼️**: 다양한 이미지 형식을 지원하며, 이미지 로드, 크기 조정, 저장을 쉽게 할 수 있어 대용량 데이터셋을 처리하는 데 중요합니다.
2. **이미지 처리 ✨**: 이미지 필터링, 그레이스케일 변환, 크기 조정, 회전 및 기타 조작을 위한 함수를 제공합니다. 이는 분석 전에 이미지를 전처리하는 데 중요합니다.
3. **객체 검출 🔍**: 테두리, 모서리 및 기타 주요 포인트를 검출하는 알고리즘을 포함하여 특정 객체를 식별하고 추적하는 데 도움을 줍니다.
4. **객체 인식 👁️**: 얼굴, 제스처 및 기타 객체를 이미지 및 비디오에서 인식하는 도구를 제공하며, 이는 많은 컴퓨터 비전 응용 프로그램에 중요합니다.

## 신경망 모델 (ResNet50) 🧠:

![image](https://github.com/Solrikk/PicTrace/assets/70236693/d47bd022-8a05-48fc-b6c8-147ec99520ce)

**ResNet50** (Residual Network) 모델은 이미지 분류 및 특징 추출 작업을 위한 가장 인기 있고 강력한 딥러닝 아키텍처 중 하나입니다. ResNet50 모델은 다음과 같은 장점을 제공합니다:

1. **딥 레지듀얼 네트워크 🏗️**: 레지듀얼 네트워크를 사용하여 딥 뉴럴 네트워크의 트레이닝을 용이하게 하여 매우 깊은 아키텍처를 구축할 수 있게 합니다.
2. **사전 학습된 가중치 🎓**: 모델은 ImageNet 데이터셋에서 사전 학습된 가중치를 제공하여 트레이닝 속도를 대폭 향상시키고 이미지 분류 작업의 정확성을 높입니다.
3. **특징 추출 🔑**: 모델을 사용하여 이미지에서 특징을 추출할 수 있으며, 이는 인지 데이터 분석 및 머신러닝과 관련된 작업에 유용합니다.
4. **유연성 🚀**: 모델은 분류 작업과 이미지 특징의 추출 및 비교 작업 모두에 사용할 수 있으며, 이는 애플리케이션에 적합합니다.

**OpenCV**와 **ResNet50**을 함께 사용하면 시각 데이터를 분석하고 자동 객체 인식 및 이미지 분류와 같은 복잡한 작업을 수행할 수 있는 강력한 컴퓨터 비전 응용 프로그램을 만들 수 있습니다.

---

컴퓨터 비전에서 사용되는 ORB(Oriented FAST and Rotated BRIEF) 방법은 객체 인식, 이미지 매칭 및 추적과 관련된 작업에 특히 인기가 있습니다. 이 방법은 이미지에서 키포인트를 빠르게 찾고 이러한 키포인트를 효율적으로 비교할 수 있도록 설명하는 데 중점을 둡니다.

<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/ORB/images/ORB3.png" width="65%" /> 

1. **Oriented FAST (가속 분할 테스트에서의 특징) 🚀:** 이 구성 요소는 이미지에서 관심 포인트(또는 키포인트)를 감지하는 역할을 합니다. 주변 영역과 비교하여 두드러진 코너나 에지를 빠르게 식별합니다. 이 방식으로 이미지의 의미가 있거나 고유한 섹션을 식별할 수 있습니다.
2. **Rotated BRIEF (바이너리 강건 독립 기본 특징) 🔄:** 키포인트가 발견된 후, 다른 이미지의 키포인트와 비교할 수 있도록 각 키포인트에 대한 설명을 생성해야 합니다. BRIEF는 키포인트의 간단한 이진 설명을 생성하지만, 이미지 회전에 대한 내성이 없습니다. 이는 "회전" 부분이 필요한 이유입니다 - ORB는 이미지가 회전해도 안정적으로 포인트를 설명할 수 있도록 추가 기능을 제공합니다.

이 두 가지 접근 방식을 결합하여 ORB는 시야각, 스케일 또는 조명의 변화에도 불구하고 이미지를 빠르고 효율적으로 일치시키는 방법을 제공합니다.

PicTrace는 업로드된 이미지와 유사한 이미지를 찾기 위해 **SSIM**과 **ORB** 방법을 모두 사용합니다. 여기에서는 각 방법이 애플리케이션의 맥락에서 어떻게 작동하며 유사한 이미지를 찾는 데 어떻게 기여하는지에 대해 간단히 설명합니다:

## PicTrace에서 SSIM이 작동하는 방법:
1. **이미지 크기 조정 🔧:** 업로드된 이미지와 데이터베이스의 각 이미지를 비교할 때, 두 이미지 모두 동일한 크기(256x256 픽셀)로 조정됩니다. 이는 비교를 표준화하여 더 공정하고 효율적으로 만듭니다.
2. **그레이스케일로 변환 🌑:** 두 이미지는 그레이스케일로 변환됩니다. 이는 색상 차이에 방해받지 않고 구조와 빛의 강도에 중점을 두어 비교를 단순화합니다.
3. **구조적 유사성 비교 🧩:** SSIM 방법은 이러한 그레이스케일 이미지를 비교하여 구조적 유사성을 평가합니다. 높은 점수는 이미지가 구조적으로 유사함을 의미합니다.

## PicTrace에서 ORB가 작동하는 방법:
1. **키포인트 감지 📍:** ORB는 먼저 업로드된 이미지와 각 데이터베이스 이미지에서 키포인트를 식별합니다. 이러한 포인트는 쉽게 인식 가능하며 이미지 간 비교가 가능합니다.
2. **키포인트 설명 🖊️:** 검출된 각 키포인트에 대해 ORB는 해당 키포인트의 특성을 요약하는 고유한 설명자를 생성합니다. 이 설명자는 이미지 회전에 불변입니다.
3. **키포인트 매칭 🔗:** 애플리케이션은 업로드된 이미지와 각 데이터베이스 이미지 간의 키포인트를 매칭합니다. 이 과정에는 업로드된 이미지의 설명자와 유사한 설명자를 가진 데이터베이스 이미지의 키포인트를 찾는 작업이 포함됩니다.
4. **매칭 점수 평가 🏅:** 두 이미지 간의 매칭 키포인트가 많을수록 ORB 기반 유사도 점수가 높아집니다. 이 점수는 이미지가 공유하는 독특한 특징의 수를 반영합니다.

**SSIM** 과 **ORB** 방법을 결합하여 업로드된 이미지와 유사한 이미지를 찾고 비교하는 강력하고 정확한 방법을 제공합니다.
