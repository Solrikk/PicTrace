![Logo](https://github.com/Solrikk/PicTrace/blob/main/assets/OpenCV%20-%20result/bee.jpg)

<div align="center">
  <h3>
    <a href="https://github.com/Solrikk/PicTrace/blob/main/README.md">English</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/README_RU.md">Russian</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/README_GE.md">German</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/README_JP.md">⭐Japanese⭐</a> |
    <a href="README_KR.md">Korean</a> |
    <a href="README_CN.md">Chinese</a>
  </h3>
</div>

-----------------

# PicTrace 🔍

_**PicTrace**_ は、高速かつ正確な画像検索のために、_**OpenCV**_ を使用したコンピュータビジョン、_**TensorFlow**_ と _**ResNet50モデル**_ を用いた深層学習、_**aiohttp**_ を使った非同期処理、および _**FastAPI**_ ウェブフレームワークを活用した非常に効率的な画像マッチングプラットフォームです。PicTraceは、ユーザーが画像を直接アップロードしたり、URLを提供することで、膨大なデータベースを迅速にスキャンして類似画像を見つけることを可能にします。非同期処理によりスムーズで迅速なビジュアル検索が実現し、ユーザーエクスペリエンスが向上します。

# オンラインデモ:

_**PicTrace**_ がリアルタイムでどのように動作するか気になりますか？ 

オンラインデモを試して、画像マッチングプラットフォームの機能を確認してください。

[オンラインデモ](https://PicTrace.replit.app) - **ぜひ試してみてください！**

![PicTrace Demo](https://github.com/Solrikk/PicTrace/blob/main/assets/gif/Pictrace.gif)

## 目次:
1. [機能 ⚡](#機能-⚡)
2. [PicTraceの始め方 🚀](#pictraceの始め方-🚀)
   - [前提条件](#前提条件)
   - [PicTraceのセットアップ手順](#pictraceのセットアップ手順)
   - [アプリケーションの起動方法](#アプリケーションの起動方法)
3. [結果: 👨‍💻](#結果-👨‍💻)
4. [例: 📋](#例-📋)
   - [コメント付きのコード](#コメント付きのコード)
5. [PicTraceでのSSIMの動作](#pictraceでのssimの動作)
6. [PicTraceでのORBの動作](#pictraceでのorbの動作)
7. [SSIMとORBの組み合わせ](#ssimとorbの組み合わせ)
8. [OpenCV（オープンソースコンピュータビジョンライブラリ）🌐](#opencvオープンソースコンピュータビジョンライブラリ-🌐)
9. [ニューラルネットワークモデル（ResNet50）🧠](#ニューラルネットワークモデル-ResNet50-🧠)
10. [類似画像の最終選択](#類似画像の最終選択)

## 機能: ⚡
- **_複数の技術をサポート_** 💼

    これらの強力なライブラリを備えた _**Python**_:
  - **`FastAPI:`** ウェブアプリケーションの作成とHTTPリクエストの処理に最適で、高性能と非同期操作のサポートで知られています。 [詳細](https://fastapi.tiangolo.com/)
  - **`aiohttp:`** URLを介して画像をダウンロードするなどの非同期HTTPリクエストの処理に最適で、アプリの速度と効率を向上させます。 [詳細](https://docs.aiohttp.org/en/stable/index.html)
  - **`OpenCV (cv2):`** 画像の読み込み、サイズ変更、比較などの高度な画像処理に使用される堅牢なコンピュータビジョンライブラリで、画像関連のタスクに欠かせません。 [詳細](https://docs.opencv.org/)
  - **`numpy:`** 多次元配列の操作のための多用途なライブラリで、効率的な画像処理のためにOpenCVと一緒に使用されることが多いです。 [詳細](https://numpy.org/doc/)
  - **`scikit-image:`** 特にこのライブラリの `structural_similarity`（SSIM）関数は画像の類似性を比較するために使用され、アプリケーションの画像マッチング精度を向上させます。 [詳細](https://scikit-image.org/docs/stable/auto_examples/transform/plot_ssim.html)
  - **`hashlib:`** 各画像に対して一意のハッシュを生成し、すべての画像が一意に識別され効率的に管理されることを保証します。 [詳細](https://docs.python.org/3/library/hashlib.html)

- **_複数のインデックスをサポート_** 🗂️

  - **`画像ハッシュ:`** 画像の一意のハッシュを生成して一意の識別と効率的な管理を確保します。
  - **`ResNet50による特徴抽出:`** 画像から堅牢な特徴表現を抽出するためにResNet50モデルを利用します。
  - **`コサイン類似度:`** 画像から抽出された特徴ベクトルを使用して画像間の類似性を測定します。

-----------------

## PicTraceの始め方: 🚀
_PicTraceは開発プロセスを効率化するために設計された強力な画像トレースと比較ツールです。これらの手順に従って環境を設定し、アプリケーションを正常に起動してください。_

### 前提条件
PicTraceを使用するには、次のコンポーネントがインストールされていることを確認してください：

- **Python 3.8以上:** PicTraceはPythonで構築されています。最新バージョンのPythonは[公式ウェブサイト](https://www.python.org/downloads/)からダウンロードできます。
- **pip:** Pythonのパッケージインストーラーで、Python 3.4以降にプリインストールされています。必要な依存関係をインストールするためにpipを使用します。
- **Git:** PicTraceリポジトリをクローンするために必要です。システムにGitがインストールされていない場合は、[Gitの公式サイト](https://git-scm.com/downloads)のインストール手順に従ってください。

### PicTraceのセットアップ手順:
1. **リポジトリをクローン**

_まず、PicTraceのソースコードをローカルマシンに取得します。次のコマンドを使用してGitHubからリポジトリをクローンします:_

```git clone https://github.com/solrikk/PicTrace.git```

2. **_仮想環境の設定:_** ✔️

_仮想環境は、プロジェクトの依存関係をグローバルなPython設定から分離し、異なるプロジェクト間でのバージョンの競合を防ぐために重要です。仮想環境を作成してアクティブ化するために、以下のコマンドを実行します:_

仮想環境を作成してアクティブ化するには、以下のコマンドを使用します:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux および MacOS
source venv/bin/activate
```

3. **_依存関係のインストール:_** ✔️
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

## 結果: 👨‍💻
_詳細な情報やノイズ、歪みの存在が考えられる複雑な画像に対しては、**20%** 以上の類似性でも重要な共通特徴が存在することを示している可能性があります。そのような場合、タスクの複雑さやアルゴリズムの制限により、類似性の割合が低くなることが予想されます。_
|画像 1 vs 画像 2|類似度|画像|
|:-:|:-:|:-:|
|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/result_3-1.png" alt="" width="500"/>|**27.12%**|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/palegleam.jpg" alt="" width="300"/>|
|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/result_2.png" alt="" width="500"/>|**25.44%**|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/ryan-yao.jpg" alt="" width="300"/>|
|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/result_3.png" alt="" width="500"/>|**44.16%**|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/taro-ohtani.jpg" alt="" width="300"/>|

## 例: 📋
(**_コメント付きコード_**)

```Python 
async def find_similar_images(file_path):
    # 画像に関する情報を含むデータベースからデータをロードする。
    db_data = load_db()
    # 指定されたファイルパスからターゲット画像を読み取る。
    target_image = cv2.imread(file_path)
    # 事前にトレーニングされたモデルを使用してターゲット画像から特徴を抽出する。
    target_features = extract_features(target_image)
    # HTTPリクエストを処理するためのaiohttp非同期セッションを作成する。
    async with aiohttp.ClientSession() as session:
        # データベースの各画像に対してcompare_images関数の非同期タスクを作成する。
        tasks = [
            compare_images(session, entry, target_features) for entry in db_data
            if "url" in entry  # 画像URLを含むエントリのみを比較する。
        ]
        # すべてのタスクが完了するのを待って結果を収集する。
        results = await asyncio.gather(*tasks)
    # 類似度スコアが0より大きい結果のみを保持するようにフィルタリングする。
    valid_results = filter(lambda x: x[0] > 0, results)   
    # フィルタリングされた結果を類似度スコアの降順でソートし、上位5件を取得する。
    sorted_results = sorted(valid_results, key=lambda x: x[0], reverse=True)[:5]
    # 類似画像のURLを格納するリストを作成する。
    similar_images = []
    for result in sorted_results:
        if result[1]:
            similar_images.append(result[1])
    # 類似画像のURLリストを返す。
    return similar_images
```

-----------------

## _OpenCV (オープンソースコンピュータビジョンライブラリ) 🌐:_

<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/OpenCV%20-%20result/parrot.png" width="95%" /> 

**OpenCV** は画像およびビデオ処理のための強力なコンピュータビジョンライブラリです。機械ビジョン、画像認識、ビデオ分析などに関連する分野で広く使用されています。ライブラリには、オブジェクト検出、顔認識、運動追跡、ビデオ操作などの画像分析用の広範なアルゴリズムが含まれています。

**OpenCV** の主な機能は次のとおりです：
1. **画像の読み込みと保存 🖼️**: さまざまな画像フォーマットをサポートし、画像の読み込み、サイズ変更、および保存を簡単に行うことができ、大規模なデータセットを扱う上で重要です。
2. **画像処理 ✨**: 画像のフィルタリング、グレースケールへの変換、サイズ変更、回転、およびその他の操作のための機能を提供し、分析前の画像の前処理に重要です。
3. **オブジェクト検出 🔍**: エッジ、コーナー、およびその他のポイントを検出するアルゴリズムを含み、フレーム内の特定のオブジェクトの識別および追跡に役立ちます。
4. **オブジェクト認識 👁️**: 顔、ジェスチャー、および画像およびビデオ内のその他のオブジェクトを認識するためのツールを提供し、多くのコンピュータビジョンアプリケーションに重要です。

## ニューラルネットワークモデル (ResNet50) 🧠:

![image](https://github.com/Solrikk/PicTrace/assets/70236693/d47bd022-8a05-48fc-b6c8-147ec99520ce)

**ResNet50** (Residual Network) モデルは、画像分類および特徴抽出タスクのための最も人気があり強力なディープラーニングアーキテクチャの1つです。あなたのニューラルネットワークモデル **ResNet50** は次の利点を提供します：

1. **ディープレジデュアルネットワーク 🏗️**: ディープニューラルネットワークのトレーニングを容易にし、非常に深いアーキテクチャを構築できるようにし、勾配消失のリスクを排除します。
2. **事前トレーニング済みの重み 🎓**: モデルはImageNetデータセットで事前トレーニングされた重みを持ち、トレーニングの速度を大幅に向上させ、画像分類タスクの精度を向上させます。
3. **特徴抽出 🔑**: モデルは画像から特徴を抽出するために使用でき、認知データ分析および機械学習に関連するタスクに役立ちます。
4. **柔軟性 🚀**: モデルは、分類タスクと画像特徴の抽出および比較タスクの両方に使用でき、あなたのアプリケーションに適しています。

**OpenCV** と **ResNet50** を組み合わせることで、自動オブジェクト認識や画像分類などの複雑なタスクを実行できる強力なコンピュータビジョンアプリケーションを作成できます。

---

コンピュータビジョンで使用されるORBメソッドは、オブジェクト認識、画像マッチング、およびトラッキングに関連するタスクで特に人気があります。このメソッドは、画像上のキーポイントを迅速に見つけ、それらを効率的に比較できる方法で記述することに重点を置いています。

<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/ORB/images/ORB3.png" width="65%" /> 

1. **向き付きFAST (加速セグメントテストからの特徴)🚀:** このコンポーネントは、画像上の関心点（またはキーポイント）を検出する役割を担います。それは、周囲と比較して際立つコーナーやエッジを迅速に識別します。このようにして、画像の意味のあるまたは独特のセクションを特定することができます。
2. **回転BRIEF (バイナリロバスト独立基本特徴) 🔄:** キーポイントが検出された後、比較のためにキーポイントの記述を生成する必要があります。BRIEFはキーポイントの短いバイナリ記述を生成しますが、画像の回転に対して耐性がありません。ここで「回転」の部分が重要です - ORBは画像が回転しても安定した記述を提供します。

これらの2つのアプローチを組み合わせることで、ORBは、視点、スケール、照明の変化にもかかわらず、画像を迅速かつ効率的に一致させる方法を提供します。

PicTraceは、アップロードされた画像に似た画像を見つけるために、**SSIM** と **ORB** の両方のメソッドを使用します。ここでは、それぞれの方法があなたのアプリケーションのコンテキストでどのように機能し、類似画像の検索にどのように貢献するかについて簡単に説明します：

## PicTraceでのSSIMの機能:
1. **画像のリサイズ 🔧:** アップロードされた画像とデータベース内の各画像を比較する際、両方の画像は同じ寸法（256x256ピクセル）にリサイズされます。これにより、比較が標準化され、より効率的になります。
2. **グレースケールへの変換 🌑:** 両方の画像はグレースケールに変換されます。これにより、色の違いに気を取られることなく、構造と光の強度に集中して比較が行えます。
3. **構造的類似性の比較 🧩:** SSIMメソッドはこれらのグレースケール画像を比較し、構造的な類似性を評価します。高いスコアは、画像が構造的に類似していることを意味します。

## PicTraceでのORBの機能:
1. **キーポイントの検出 📍:** ORBはまず、アップロードされた画像と各データベース画像の両方にキーポイントを特定します。これらのポイントは簡単に識別でき、画像間で比較が可能です。
2. **キーポイントの記述 🖊️:** 検出された各キーポイントについて、ORBはそのキーポイントの特性を要約する一意の記述子を生成します。この記述子は画像の回転にも不変です。
3. **キーポイントのマッチング 🔗:** アプリケーションはアップロードされた画像と各データベース画像の間でキーポイントをマッチングします。このプロセスには、アップロードされた画像の記述子と類似した記述子を持つデータベース画像のキーポイントを見つけることが含まれます。
4. **マッチのスコア付け 🏅:** 2枚の画像間でマッチするキーポイントが多いほど、ORBに基づく類似度スコアは高くなります。このスコアは、画像が共有する特色の数を反映しています。

**SSIM** と **ORB** の両方のメソッドを組み合わせることで、アップロードされた画像に似た画像を見つけて比較するための強力で正確な方法を提供します。
