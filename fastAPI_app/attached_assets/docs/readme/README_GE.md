![Logo](https://github.com/Solrikk/PicTrace/blob/main/assets/OpenCV%20-%20result/bee.jpg)

<div align="center">
  <h3>
    <a href="https://github.com/Solrikk/PicTrace/blob/main/README.md">English</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/README_RU.md">Russian</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/README_GE.md">⭐Deutsch⭐</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/README_JP.md">Japanese</a> |
    <a href="README_KR.md">Korean</a> |
    <a href="README_CN.md">Chinese</a>
  </h3>
</div>

-----------------

# PicTrace 🔍

_**PicTrace**_ ist eine hocheffiziente Bildabgleichsplattform, die Computer Vision mit _**OpenCV**_, Deep Learning mit _**TensorFlow**_ und dem _**ResNet50-Modell**_, asynchrone Verarbeitung mit _**aiohttp**_ sowie das _**FastAPI**_-Webframework für schnelle und genaue Bildersuche nutzt. PicTrace ermöglicht es Benutzern, Bilder direkt hochzuladen oder URLs bereitzustellen und durchforstet schnell eine umfangreiche Datenbank, um ähnliche Bilder zu finden. Asynchrone Verarbeitung sorgt für eine reibungslose und schnelle visuelle Suche und verbessert das Benutzererlebnis.

# Online-Demos:

Neugierig zu sehen, wie _PicTrace_ in Echtzeit funktioniert? 

Erkunden Sie mein Online-Demo und erleben Sie die Fähigkeiten meiner Bildabgleichsplattform.

[Online Demo](https://PicTrace.replit.app) - **Probieren Sie es aus und überzeugen Sie sich selbst!**

![PicTrace Demo](https://github.com/Solrikk/PicTrace/blob/main/assets/gif/Pictrace.gif)

## Inhaltsverzeichnis:
1. [Funktionen ⚡](#funktionen-⚡)
2. [Erste Schritte mit PicTrace 🚀](#erste-schritte-mit-pictrace-🚀)
   - [Voraussetzungen](#voraussetzungen)
   - [Schritte zur Einrichtung von PicTrace](#schritte-zur-einrichtung-von-pictrace)
   - [Starten der Anwendung](#starten-der-anwendung)
3. [Ergebnisse: 👨‍💻](#ergebnisse-👨‍💻)
4. [Beispiele: 📋](#beispiele-📋)
   - [Code mit Kommentaren](#code-mit-kommentaren)
5. [Wie SSIM in PicTrace funktioniert](#wie-ssim-in-pictrace-funktioniert)
6. [Wie ORB in PicTrace funktioniert](#wie-orb-in-pictrace-funktioniert)
7. [Kombinieren von SSIM und ORB](#kombinieren-von-ssim-und-orb)
8. [OpenCV (Open Source Computer Vision Library) 🌐](#opencv-open-source-computer-vision-library-🌐)
9. [Neuronales Netzwerkmodell (ResNet50) 🧠](#neuronales-netzwerkmodell-resnet50-🧠)
10. [Endauswahl ähnlicher Bilder](#endauswahl-ähnlicher-bilder)

## Funktionen: ⚡
- **_Unterstützt mehrere Technologien_** 💼

    _**Python**_ mit diesen leistungsstarken Bibliotheken:
  - **`FastAPI:`** Ideal für die Erstellung von Webanwendungen und die Handhabung von HTTP-Anfragen, bekannt für hohe Leistung und Unterstützung asynchroner Operationen. [Details](https://fastapi.tiangolo.com/)
  - **`aiohttp:`** Perfekt für die Handhabung asynchroner HTTP-Anfragen, wie das Herunterladen von Bildern über URLs, wodurch Ihre App schneller und effizienter wird. [Details](https://docs.aiohttp.org/en/stable/index.html)
  - **`OpenCV (cv2):`** Eine robuste Computer-Vision-Bibliothek für fortgeschrittene Bildverarbeitung, einschließlich Laden, Größenänderung und Vergleich von Bildern, ein kritischer Bestandteil für Ihre bildbezogenen Aufgaben. [Details](https://docs.opencv.org/)
  - **`numpy:`** Eine vielseitige Bibliothek zur Arbeit mit mehrdimensionalen Arrays, oft in Verbindung mit OpenCV für effiziente Bildverarbeitung verwendet. [Mehr Info](https://numpy.org/doc/)
  - **`scikit-image:`** Insbesondere die `structural_similarity` (SSIM) Funktion aus dieser Bibliothek wird verwendet, um die Ähnlichkeit von Bildern zu vergleichen und die Genauigkeit Ihrer Anwendung beim Bildabgleich zu erhöhen. [Details](https://scikit-image.org/docs/stable/auto_examples/transform/plot_ssim.html)
  - **`hashlib:`** Wird verwendet, um eindeutige Hashes für jedes Bild zu generieren, wodurch jedes Bild eindeutig identifiziert und effizient verwaltet werden kann. [Mehr Info](https://docs.python.org/3/library/hashlib.html)

- **_Unterstützt mehrere Indizes_** 🗂️

  - **`Bild-Hashing:`** Erstellen von eindeutigen Hashes für Bilder zur Sicherstellung der eindeutigen Identifikation und effizienten Verwaltung.
  - **`Merkmalextraktion mit ResNet50:`** Nutzt das ResNet50-Modell zur Extraktion robuster Merkmalsdarstellungen aus Bildern.
  - **`Kosinus-Ähnlichkeit:`** Messen der Ähnlichkeit zwischen Bildern mittels Kosinus-Ähnlichkeit auf den aus den Bildern extrahierten Merkmalsvektoren.

-----------------

## Erste Schritte mit PicTrace: 🚀
_PicTrace ist ein leistungsstarkes Werkzeug zur Bildverfolgung und -vergleichung, das entwickelt wurde, um Ihren Entwicklungsprozess zu optimieren. Befolgen Sie diese Schritte, um Ihre Umgebung einzurichten und die Anwendung erfolgreich zu starten._

### Voraussetzungen
Um mit PicTrace zu arbeiten, stellen Sie sicher, dass folgende Komponenten installiert sind:

- **Python 3.8 oder höher:** PicTrace ist in Python geschrieben. Sie können die neueste Version von Python von der [offiziellen Website](https://www.python.org/downloads/) herunterladen.
- **pip:** Der Paket-Installer für Python, der ab Python 3.4 und höher vorinstalliert ist. Wir verwenden pip, um die notwendigen Abhängigkeiten zu installieren.
- **Git:** Erforderlich zum Klonen des PicTrace-Repositories. Falls Git noch nicht auf Ihrem System installiert ist, folgen Sie den Installationsanweisungen auf der [offiziellen Git-Website](https://git-scm.com/downloads).

### Schritte zur Einrichtung von PicTrace:
1. **Repository klonen**

_Zuerst erhalten Sie eine Kopie des PicTrace-Quellcodes auf Ihrem lokalen Computer. Verwenden Sie die folgenden Befehle, um das Repository von GitHub zu klonen:_

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

## Ergebnisse: 👨‍💻
_Für komplexe Bilder mit vielen Details und möglicher Anwesenheit von Rauschen oder Verzerrungen kann selbst eine Ähnlichkeit auf dem Niveau von **20%** und darüber auf das Vorhandensein signifikanter gemeinsamer Merkmale hinweisen. In solchen Fällen kann aufgrund der Komplexität der Aufgabe und der Einschränkungen des Algorithmus ein niedriger Prozentsatz der Ähnlichkeit erwartet werden._
|Bild 1 vs Bild 2|Ähnlichkeit|Bild|
|:-:|:-:|:-:|
|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/result_3-1.png" alt="" width="500"/>|**27,12%**|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/palegleam.jpg" alt="" width="300"/>|
|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/result_2.png" alt="" width="500"/>|**25,44%**|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/ryan-yao.jpg" alt="" width="300"/>|
|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/result_3.png" alt="" width="500"/>|**44,16%**|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/taro-ohtani.jpg" alt="" width="300"/>|

## Beispiele: 📋
(**_Code mit Kommentaren_**)

```Python 
async def find_similar_images(file_path):
    # Laden Sie die Daten aus der Datenbank, die Informationen über Bilder enthält.
    db_data = load_db()
    # Lesen Sie das Zielbild von dem angegebenen Dateipfad.
    target_image = cv2.imread(file_path)
    # Extrahieren Sie Merkmale aus dem Zielbild unter Verwendung eines vortrainierten Modells.
    target_features = extract_features(target_image)
    # Erstellen Sie eine aiohttp-asynchrone Sitzung zur Handhabung von HTTP-Anfragen.
    async with aiohttp.ClientSession() as session:
        # Erstellen Sie asynchrone Aufgaben für die Funktion compare_images für jedes Bild in der Datenbank.
        tasks = [
            compare_images(session, entry, target_features) for entry in db_data
            if "url" in entry  # Vergleiche nur für Einträge, die eine Bild-URL enthalten.
        ]
        # Warten Sie, bis alle Aufgaben abgeschlossen sind und sammeln Sie die Ergebnisse.
        results = await asyncio.gather(*tasks)
    # Filtern Sie die Ergebnisse und behalten Sie nur diejenigen mit einem Ähnlichkeitswert größer als 0 bei.
    valid_results = filter(lambda x: x[0] > 0, results)   
    # Sortieren Sie die gefilterten Ergebnisse nach dem Ähnlichkeitswert in absteigender Reihenfolge und nehmen Sie die Top 5.
    sorted_results = sorted(valid_results, key=lambda x: x[0], reverse=True)[:5]
    # Erstellen Sie eine Liste zur Speicherung der URLs der ähnlichen Bilder.
    similar_images = []
    for result in sorted_results:
        if result[1]:
            similar_images.append(result[1])
    # Geben Sie die Liste der URLs der ähnlichen Bilder zurück.
    return similar_images
```

-----------------

## _OpenCV (Open Source Computer Vision Library) 🌐:_

<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/OpenCV%20-%20result/parrot.png" width="95%" /> 

**OpenCV** ist eine leistungsstarke Computer-Vision-Bibliothek, die Werkzeuge zur Verarbeitung von Bildern und Videos bereitstellt. Sie wird in vielen Bereichen verwendet, die mit maschinellem Sehen, Bilderkennung, Videoanalyse und mehr zu tun haben. Die Bibliothek umfasst eine breite Palette von Algorithmen zur Bildanalyse, wie Objekterkennung, Gesichtserkennung, Bewegungserkennung, Videomanipulation und mehr.

Die wichtigsten Funktionen von **OpenCV** sind:
1. **Bilder laden und speichern 🖼️**: Unterstützt verschiedene Bildformate und ermöglicht das einfache Laden, Ändern der Größe und Speichern von Bildern, was für die Verarbeitung großer Datenmengen entscheidend ist.
2. **Bildverarbeitung ✨**: Bietet Funktionen zum Filtern von Bildern, Umwandeln in Graustufen, Ändern der Größe, Drehen und anderen Manipulationen. Dies ist wichtig für die Vorverarbeitung von Bildern vor der Analyse.
3. **Objekterkennung 🔍**: Beinhaltet Algorithmen zur Erkennung von Kanten, Ecken und anderen wichtigen Punkten, die helfen, bestimmte Objekte in einem Bild zu identifizieren und zu verfolgen.
4. **Objekterkennung 👁️**: Bietet Werkzeuge zur Erkennung von Gesichtern, Gesten und anderen Objekten in Bildern und Videos, was für viele Computer-Vision-Anwendungen entscheidend ist.

## Neuronales Netzwerkmodell (ResNet50) 🧠:

![image](https://github.com/Solrikk/PicTrace/assets/70236693/d47bd022-8a05-48fc-b6c8-147ec99520ce)

Das **ResNet50**-Modell (Residual Network) ist eine der beliebtesten und leistungsstärksten Deep-Learning-Architekturen für Aufgaben der Bildklassifikation und Merkmalsextraktion. Ihr neuronales Netzwerkmodell **ResNet50** bietet folgende Vorteile:

1. **Tiefe Residual-Netzwerke 🏗️**: Verwenden Residual-Netzwerke, um das Training tiefer neuronaler Netzwerke zu erleichtern, was den Aufbau sehr tiefer Architekturen ohne das Risiko verschwindender Gradienten ermöglicht.
2. **Vorgefertigte Gewichte 🎓**: Das Modell wird mit vortrainierten Gewichten auf dem ImageNet-Datensatz geliefert, was das Training erheblich beschleunigen und die Genauigkeit bei Bildklassifikationsaufgaben verbessern kann.
3. **Merkmalextraktion 🔑**: Das Modell kann zur Extraktion von Merkmalen aus Bildern verwendet werden, was für Aufgaben der kognitiven Datenanalyse und des maschinellen Lernens nützlich ist.
4. **Flexibilität 🚀**: Das Modell kann sowohl zur Klassifikation als auch zur Extraktion und Vergleich von Bildmerkmalen verwendet werden, was für Ihre Anwendung geeignet ist.

Zusammen können **OpenCV** und **ResNet50** verwendet werden, um leistungsstarke Computer-Vision-Anwendungen zu erstellen, die visuelle Daten analysieren und komplexe Aufgaben wie die automatische Objekterkennung und Bildklassifikation ausführen können.

---

Die ORB-Methode, die im Computer-Vision-Bereich verwendet wird, ist besonders beliebt für Aufgaben im Zusammenhang mit der Objekterkennung, dem Abgleichen von Bildern und dem Tracking. Diese Methode konzentriert sich darauf, schnell Schlüsselpunkte auf Bildern zu finden und zu beschreiben, um einen effizienten Vergleich zu ermöglichen.

<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/ORB/images/ORB3.png" width="65%" /> 

1. **Oriented FAST (Features from Accelerated Segment Test) 🚀:** Diese Komponente ist für die Erkennung von interessanten Punkten (oder Schlüsselpunkten) auf dem Bild verantwortlich. Sie identifiziert schnell Ecken oder Kanten, die sich im Vergleich zu ihrer Umgebung abheben, wodurch signifikante oder einzigartige Bereiche des Bildes identifiziert werden können.

2. **Rotated BRIEF (Binary Robust Independent Elementary Features) 🔄:** Nachdem die Schlüsselpunkte gefunden wurden, ist es notwendig, eine Beschreibung für jeden zu erstellen, um den Vergleich mit Schlüsselpunkten eines anderen Bildes zu ermöglichen. BRIEF erzeugt eine kurze binäre Beschreibung der Punkte, jedoch fehlt es an Widerstandsfähigkeit gegen Bildrotationen. Hier kommt der Teil "rotated" ins Spiel - ORB fügt die Fähigkeit hinzu, Punkte stabil zu beschreiben, auch wenn Bilder gedreht werden.

Durch die Kombination dieser beiden Ansätze bietet ORB eine schnelle und effiziente Möglichkeit, Bilder trotz Änderungen des Betrachtungswinkels, der Skalierung oder der Beleuchtung abzugleichen.

PicTrace verwendet sowohl **SSIM** als auch **ORB**-Methoden, um Bilder zu finden, die einem hochgeladenen Bild ähneln. Hier ist eine vereinfachte Erklärung, wie jede Methode im Kontext Ihrer Anwendung funktioniert und zum Finden ähnlicher Bilder beiträgt:

## Wie SSIM in PicTrace funktioniert:
1. **Bilder skalieren 🔧:** Beim Vergleich des hochgeladenen Bildes mit jedem Bild in der Datenbank werden beide Bilder auf die gleichen Abmessungen (256x256 Pixel) skaliert. Dies standardisiert den Vergleich und macht ihn fairer und effizienter.
2. **Konvertieren in Graustufen 🌑:** Beide Bilder werden in Graustufen konvertiert. Dies vereinfacht den Vergleich, indem der Fokus auf die Struktur und die Lichtintensität gelegt wird, anstatt durch Farbunterschiede abgelenkt zu werden.
3. **Vergleich der strukturellen Ähnlichkeit 🧩:** Die SSIM-Methode vergleicht dann diese Graustufenbilder, um ihre strukturelle Ähnlichkeit zu bewerten. Ein hoher Wert bedeutet, dass die Bilder strukturell ähnlich sind.

## Wie ORB in PicTrace funktioniert:
1. **Erkennung von Schlüsselpunkten 📍:** ORB identifiziert zuerst Schlüsselpunkte sowohl auf dem hochgeladenen Bild als auch auf jedem Datenbankbild. Diese Punkte sind leicht erkennbar und können zwischen den Bildern verglichen werden.
2. **Beschreibung der Schlüsselpunkte 🖊️:** Für jeden erkannten Schlüsselpunkt erzeugt ORB einen eindeutigen Deskriptor, der die Merkmale des Schlüsselpunktes zusammenfasst. Dieser Deskriptor ist unempfindlich gegenüber Bildrotationen.
3. **Abgleich der Schlüsselpunkte 🔗:** Die Anwendung gleicht die Schlüsselpunkte zwischen dem hochgeladenen Bild und jedem Datenbankbild ab. Der Prozess umfasst das Finden von Schlüsselpunkten im Datenbankbild, die ähnliche Deskriptoren wie das hochgeladene Bild haben.
4. **Bewertung der Übereinstimmungen 🏅:** Je mehr Schlüsselpunkte zwischen zwei Bildern übereinstimmen, desto höher ist der Ähnlichkeitswert auf der Grundlage von ORB. Dieser Wert spiegelt wider, wie viele charakteristische Merkmale die Bilder teilen.

Zusammen bieten die Methoden **SSIM** und **ORB** eine robuste und genaue Möglichkeit, ähnliche Bilder zum hochgeladenen Bild zu finden und zu vergleichen.
