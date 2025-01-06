![Logo](https://github.com/Solrikk/PicTrace/blob/main/assets/OpenCV%20-%20result/bee.jpg)

<div align="center">
  <h3>
    <a href="https://github.com/Solrikk/PicTrace/blob/main/README.md">English</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/README_RU.md">Russian</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/README_GE.md">German</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/README_JP.md">Japanese</a> |
    <a href="README_KR.md">Korean</a> |
    <a href="README_CN.md">⭐Chinese⭐</a>
  </h3>
</div>

-----------------

# PicTrace 🔍

_**PicTrace**_ 是一个高效的图像匹配平台，利用 _**OpenCV**_ 进行计算机视觉，利用 _**TensorFlow**_ 和 _**ResNet50模型**_ 进行深度学习，利用 _**aiohttp**_ 进行异步处理，并利用 _**FastAPI**_ Web框架进行快速准确的图像搜索。PicTrace允许用户直接上传图像或提供URL，快速扫描庞大的数据库以查找相似的图像。异步处理确保了平滑和快速的视觉搜索，增强了用户体验。

# 在线演示：

想实时了解 _PicTrace_ 如何工作吗？ 

探索我的在线演示，见证我的图像匹配平台的功能。

[在线演示](https://PicTrace.replit.app) - **试试看，自己体验一下吧!**

![PicTrace Demo](https://github.com/Solrikk/PicTrace/blob/main/assets/gif/Pictrace.gif)

## 目录:
1. [功能 ⚡](#features-⚡)
2. [PicTrace快速入门 🚀](#getting-started-with-pictrace-🚀)
   - [先决条件](#prerequisites)
   - [设置PicTrace的步骤](#steps-to-set-up-pictrace)
   - [启动应用程序](#launching-the-application)
3. [结果: 👨‍💻](#results-👨‍💻)
4. [示例: 📋](#examples-📋)
   - [带注释的代码](#code-with-comments)
5. [PicTrace中SSIM的工作原理](#how-ssim-works-in-pictrace)
6. [PicTrace中ORB的工作原理](#how-orb-works-in-pictrace)
7. [结合SSIM和ORB](#combining-ssim-and-orb)
8. [OpenCV (开源计算机视觉库) 🌐](#opencv-open-source-computer-vision-library-🌐)
9. [神经网络模型 (ResNet50) 🧠](#neural-network-model-resnet50-🧠)
10. [相似图像的最终选择](#final-selection-of-similar-images)

## 功能: ⚡
- **_支持多种技术_** 💼

    _**Python**_ 与这些强大的库配合使用:
  - **`FastAPI:`** 适用于创建Web应用程序和处理HTTP请求，FastAPI以其高性能和对异步操作的支持而著称。 [详情](https://fastapi.tiangolo.com/)
  - **`aiohttp:`** 适合处理异步HTTP请求，如通过URL下载图像，使您的应用程序更快更高效。 [详情](https://docs.aiohttp.org/en/stable/index.html)
  - **`OpenCV (cv2):`** 用于高级图像处理的强大计算机视觉库，包括加载、调整大小和比较图像，使其成为与图像相关任务的关键组件。 [详情](https://docs.opencv.org/)
  - **`numpy:`** 用于处理多维数组的多功能库，通常与OpenCV一起使用以实现高效的图像处理。 [详情](https://numpy.org/doc/)
  - **`scikit-image:`** 特别是，该库的`structural_similarity` (SSIM)函数用于比较图像的相似性，提升您的应用程序在图像匹配中的准确性。 [详情](https://scikit-image.org/docs/stable/auto_examples/transform/plot_ssim.html)
  - **`hashlib:`** 用于为每个图像生成唯一哈希，确保每个图像都可以唯一标识并高效管理。 [详情](https://docs.python.org/3/library/hashlib.html)

- **_支持多种索引_** 🗂️

  - **`图像哈希:`** 生成图像的唯一哈希，以确保唯一标识和高效管理。
  - **`用ResNet50进行特征提取:`** 利用ResNet50模型从图像中提取强大的特征表示。
  - **`余弦相似度:`** 使用余弦相似度来测量从图像中提取的特征向量之间的相似性。

-----------------

## PicTrace快速入门: 🚀
_PicTrace是一个功能强大的图像跟踪和比较工具，旨在简化您的开发过程。按照以下步骤设置您的环境并成功启动应用程序。_

### 先决条件
要使用PicTrace，请确保安装了以下组件：

- **Python 3.8或更高版本:** PicTrace是用Python构建的。您可以从 [官方网站](https://www.python.org/downloads/) 下载Python的最新版本。
- **pip:** Python的包管理器，Python 3.4及更高版本中已预装。我们将使用pip安装必要的依赖项。
- **Git:** 需要克隆PicTrace存储库。如果您的系统上尚未安装Git，请按照 [Git官方网站](https://git-scm.com/downloads) 上的安装说明进行安装。

### 设置PicTrace的步骤:
1. **克隆存储库**

_首先，在本地机器上获取PicTrace源代码的副本。使用以下命令从GitHub克隆存储库:_

```git clone https://github.com/solrikk/PicTrace.git```

2. **_设置虚拟环境:_** ✔️

_虚拟环境对于将项目依赖项与全局Python设置隔离开来至关重要，防止不同项目之间的版本冲突。要创建和激活虚拟环境，请执行以下命令:_

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux和MacOS
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

## 结果: 👨‍💻
_对于细节很多且可能有噪声或失真的复杂图像来说，即使相似度在 **20%** 及以上，也能表明存在显著的共同特征。在这种情况下，由于任务的复杂性和算法的局限性，可能会预期低百分比的相似度。_
|图片 1 vs 图片 2|相似度|图片|
|:-:|:-:|:-:|
|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/result_3-1.png" alt="" width="500"/>|**27.12%**|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/palegleam.jpg" alt="" width="300"/>|
|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/result_2.png" alt="" width="500"/>|**25.44%**|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/ryan-yao.jpg" alt="" width="300"/>|
|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/result_3.png" alt="" width="500"/>|**44.16%**|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/taro-ohtani.jpg" alt="" width="300"/>|

## 示例: 📋
(**_带注释的代码_**)

```Python 
async def find_similar_images(file_path):
    # 从数据库加载数据，其中包含有关图像的信息。
    db_data = load_db()
    # 从指定的文件路径读取目标图像。
    target_image = cv2.imread(file_path)
    # 使用预训练模型从目标图像中提取特征。
    target_features = extract_features(target_image)
    # 创建一个aiohttp异步会话来处理HTTP请求。
    async with aiohttp.ClientSession() as session:
        # 为数据库中的每个图像创建compare_images函数的异步任务。
        tasks = [
            compare_images(session, entry, target_features) for entry in db_data
            if "url" in entry  # 仅对包含图像URL的条目执行比较。
        ]
        # 等待所有任务完成并收集结果。
        results = await asyncio.gather(*tasks)
    # 过滤结果，仅保留相似度得分大于0的结果。
    valid_results = filter(lambda x: x[0] > 0, results)   
    # 按相似度得分降序排序过滤后的结果，并取前5名。
    sorted_results = sorted(valid_results, key=lambda x: x[0], reverse=True)[:5]
    # 创建一个列表来存储相似图像的URL。
    similar_images = []
    for result in sorted_results:
        if result[1]:
            similar_images.append(result[1])
    # 返回相似图像的URL列表。
    return similar_images
```

-----------------

## _OpenCV (开源计算机视觉库) 🌐:_

<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/OpenCV%20-%20result/parrot.png" width="95%" /> 

**OpenCV** 是一个功能强大的计算机视觉库，提供了图像和视频处理工具。它广泛用于与机器视觉、图像识别、视频分析等相关的领域。该库包含了广泛的图像分析算法，例如对象检测、面部识别、运动跟踪、视频操作等等。

**OpenCV** 的主要功能包括：
1. **加载和保存图像 🖼️**: 支持各种图像格式，便于图像的加载、调整大小和保存，这对处理大型数据集至关重要。
2. **图像处理 ✨**: 提供了过滤图像、将图像转换为灰度、调整图像大小、旋转图像等功能。这些在分析前对图像进行预处理时尤为重要。
3. **对象检测 🔍**: 包含用于检测边缘、角点和其他关键点的算法，有助于在帧中识别和跟踪特定对象。
4. **对象识别 👁️**: 提供了面部识别、手势和图像与视频中其他对象识别的工具，这对许多计算机视觉应用至关重要。

## 神经网络模型 (ResNet50) 🧠:

![image](https://github.com/Solrikk/PicTrace/assets/70236693/d47bd022-8a05-48fc-b6c8-147ec99520ce)

**ResNet50** (残差网络) 模型是图像分类和特征提取任务中最受欢迎和最强大的深度学习架构之一。您的神经网络模型 **ResNet50** 具有以下优势：

1. **深度残差网络 🏗️**: 利用残差网络，简化深度神经网络的训练，允许构建非常深的架构而不会出现梯度消失的风险。
2. **预训练权重 🎓**: 该模型附带在 ImageNet 数据集上预训练的权重，这可以显著加快训练速度并提高图像分类任务的准确性。
3. **特征提取 🔑**: 该模型可用于从图像中提取特征，这对认知数据分析和机器学习相关的任务非常有用。
4. **灵活性 🚀**: 该模型既可用于分类，也可用于提取和比较图像特征的任务，适合您的应用。

结合 **OpenCV** 和 **ResNet50**，可以创建强大的计算机视觉应用程序，能够分析视觉数据并执行复杂任务，例如自动对象识别和图像分类。

---

ORB方法在计算机视觉中尤为流行，适用于对象识别、图像匹配和跟踪相关的任务。这种方法着重于快速找到图像上的关键点，并以便于高效比较的方式对这些关键点进行描述。

<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/ORB/images/ORB3.png" width="65%" /> 

1. **定向FAST (加速分段测试的特征) 🚀:** 该组件负责检测图像上的兴趣点（或关键点）。它会快速识别与周围区域相比显著的角点或边缘。通过这种方式，可以识别图像的显著或独特部分。
2. **旋转BRIEF (二进制鲁棒独立基本特征) 🔄:** 在找到关键点后，需要为每个关键点创建描述，以便与另一图像的关键点进行比较。BRIEF生成关键点的简要二进制描述，但不具备图像旋转的抗性。这里的"旋转"部分增加了ORB的功能，使其即使在图像旋转时也能稳定描述关键点。

将这两种方法结合起来，ORB提供了一种快速且有效的方式，即使在视角、比例或光照变化的情况下，仍能匹配图像。

PicTrace使用 **SSIM** 和 **ORB** 方法来查找与上传图像相似的图像。以下是每种方法在您的应用中如何工作并有助于找到相似图像的简化解释：

## PicTrace中SSIM的工作原理:
1. **调整图像大小 🔧:** 在比较上传的图像和数据库中的每个图像时，两者的尺寸都会调整为相同（256x256像素）。这样标准化了比较，使其更公平且更高效。
2. **转换为灰度 🌑:** 两者图像都转换为灰度。这简化了比较，通过聚焦于结构和光的强度，而不是被颜色差异分散注意力。
3. **结构相似性比较 🧩:** SSIM方法然后比较这些灰度图像，以评估其结构相似性。高得分意味着图像在结构上是相似的。

## PicTrace中ORB的工作原理:
1. **检测关键点 📍:** ORB首先在上传的图像和每个数据库图像中识别关键点。这些点易于识别，并可在图像之间进行比较。
2. **描述关键点 🖊️:** 对于每个检测到的关键点，ORB生成一个唯一的描述符，概括关键点的特征。该描述符对于图像旋转是不变的。
3. **匹配关键点 🔗:** 应用程序将上传的图像与每个数据库图像之间的关键点进行匹配。这个过程涉及找到数据库图像中具有与上传图像相似描述符的关键点。
4. **评分匹配 🏅:** 两个图像之间匹配的关键点越多，根据ORB计算的相似度分数越高。这个分数反映了图像共享的独特特征的数量。

通过结合 **SSIM** 和 **ORB** 方法，提供了一种强大且准确的方式来查找和比较与上传图像相似的图片。
