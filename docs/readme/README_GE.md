![Logo](https://github.com/Solrikk/PicTrace/blob/main/assets/OpenCV%20-%20result/bee.jpg)

<div align="center">
  <h3>
    <a href="https://github.com/Solrikk/PicTrace/blob/main/README.md">Englisch</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/docs/readme/README_RU.md">Russisch</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/docs/readme/README_GE.md">✦ Deutsch ✦</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/docs/readme/README_JP.md">Japanisch</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/docs/readme/README_KR.md">Koreanisch</a> |
    <a href="https://github.com/Solrikk/PicTrace/blob/main/docs/readme/README_CN.md">Chinesisch</a>
  </h3>
</div>

-----------------

# PicTrace 🔍

✨ **PicTrace** ist eine fortschrittliche Anwendung in **Python**, ausgestattet mit einer **grafischen Benutzeroberfläche (GUI)** und einer **Webversion auf FastAPI**, die es Benutzern ermöglicht, **visuell ähnliche Bilder** aus einem umfangreichen **Fotoarchiv** zu identifizieren. Durch die Nutzung von **Deep-Learning-Fähigkeiten** und **komplexen Bildverarbeitungsmethoden** bietet **PicTrace** **schnelle und präzise Suchfunktionen**, die es ideal für Aufgaben wie **Katalogisierung**, **Organisation** und **Analyse großer visueller Datensätze** machen.

# Demos:

Möchten Sie sehen, wie _PicTrace_ in Echtzeit funktioniert? 

**Probieren Sie es aus und überzeugen Sie sich selbst!**

https://pictrace.replit.app/

![Demo PicTrace](https://github.com/Solrikk/PicTrace/blob/main/assets/gif/Pictrace.gif)

## Einstieg in PicTrace:
| **Betriebssystem** | **Installations- und Startbefehle** |
|--------------------|-----------------------------------|
| 🐧**Linux**        | ```bash sudo git clone https://github.com/Solrikk/PicTrace.git cd PicTrace sudo pip install poetry sudo poetry install sudo poetry run python3 main.py ``` |
| 🍎**macOS**        | ```bash sudo git clone https://github.com/Solrikk/PicTrace.git cd PicTrace sudo pip install poetry sudo poetry install sudo poetry run python3 main.py ``` |
| 🪟**Windows**      | Öffnen Sie die Eingabeaufforderung als Administrator und führen Sie aus: ```bash git clone https://github.com/Solrikk/PicTrace.git cd PicTrace pip install poetry poetry install poetry run python main.py ``` |

![Demo PicTrace](https://github.com/Solrikk/PicTrace/blob/main/assets/gif/shell-PicTrrace.gif)

-----------------

## Funktionen ⚡

- **_Unterstützung mehrerer Technologien_**
    - **Tkinter**: Bietet eine benutzerfreundliche Oberfläche für die Anwendung, um den Benutzern eine bequeme Interaktion mit PicTrace zu ermöglichen. [Details](https://docs.python.org/3/library/tkinter.html)
    - **TensorFlow und Keras**: Wird verwendet, um das ResNet50-Modell zu laden und Merkmale aus Bildern zu extrahieren, was eine hohe Genauigkeit und Effizienz in der Bildverarbeitung gewährleistet. [Details](https://www.tensorflow.org/api_docs/python/tf/keras)
    - **numpy**: Eine vielseitige Bibliothek zur Arbeit mit mehrdimensionalen Arrays, die effektive Berechnungen und Datenverarbeitung erleichtert. [Details](https://numpy.org/doc/)
    - **Pillow (PIL)**: Eine Bibliothek zur Bildbearbeitung, die zum Laden, Skalieren und Speichern von Bildern verwendet wird. [Details](https://pillow.readthedocs.io/en/stable/)
    - **pickle**: Ein Modul zur Serialisierung und Deserialisierung von Python-Objekten, das zum Speichern und Laden von zuvor berechneten Bildmerkmalen verwendet wird. [Details](https://docs.python.org/3/library/pickle.html)
    - **hashlib**: Wird verwendet, um eindeutige Hashwerte für jedes Bild zu generieren, wodurch eine effiziente Verwaltung jedes Bildes ermöglicht wird. [Details](https://docs.python.org/3/library/hashlib.html)
    - **scikit-image**: Speziell die Funktion `structural_similarity (SSIM)` aus dieser Bibliothek wird verwendet, um die Ähnlichkeit von Bildern zu vergleichen und die Genauigkeit Ihrer Anwendung beim Abgleichen von Bildern zu erhöhen. [Details](https://scikit-image.org/docs/stable/api/skimage.metrics.html#skimage.metrics.structural_similarity)
    - **OpenCV (cv2)**: Eine zuverlässige Bibliothek für Computer Vision, die für die komplexe Bildverarbeitung verwendet wird, einschließlich Laden, Skalieren und Vergleichen von Bildern. [Details](https://docs.opencv.org/master/)
    - **zipfile**: Bearbeitet ZIP-Archive, die Bilder enthalten, und erleichtert die Verwaltung von Bildsammlungen. [Details](https://docs.python.org/3/library/zipfile.html)

-----------------

## Ergebnisse: 
_Für komplexe Bilder mit vielen Details und möglichem Rauschen oder Verzerrungen kann sogar eine Ähnlichkeit von **20%** und höher auf signifikante gemeinsame Merkmale hinweisen. In solchen Fällen kann eine niedrige Ähnlichkeit aufgrund der Komplexität der Aufgabe und der Einschränkungen des Algorithmus erwartet werden._
|Bild 1 vs Bild 2|Ähnlichkeit|Bild|
|:-:|:-:|:-:|
|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/result_3-1.png" alt="" width="500"/>|**27,12%**|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/palegleam.jpg" alt="" width="300"/>|
|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/result_2.png" alt="" width="500"/>|**25,44%**|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/ryan-yao.jpg" alt="" width="300"/>|
|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/result_3.png" alt="" width="500"/>|**44,16%**|<img src="https://github.com/Solrikk/PicTrace/blob/main/assets/result/images/taro-ohtani.jpg" alt="" width="300"/>|

## Beispiele: 
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
