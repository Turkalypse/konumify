![KonumifyLogo](../static/konumify.png)

Dieses Repository enthält zwei Versionen einer Flask-Anwendung, die Google Cloud-Dienste nutzt, um Bilddateien zu analysieren und ortsbezogene Informationen zu extrahieren. Der Hauptunterschied zwischen den beiden Versionen liegt in der Implementierung der Places API:

- `app.py`: Verwendet die Places API.
- `appv2.py`: Nutzt die Places API (Neu).

---

## Funktionen

1. **Bildanalyse**:
   - Extrahiert EXIF-Metadaten aus hochgeladenen Bildern.
   - Führt OCR (Optical Character Recognition) durch, um Text in Bildern zu analysieren.
   - Verwendet die Google Cloud Vision API für Landmarkenerkennung und Web-Erkennung.

2. **Integration der Google Places API**:
   - Ruft detaillierte Informationen über Orte aus Textanfragen und Koordinaten ab.
   - `appv2.py` verwendet die neuen Endpunkte und Methoden der Places API für verbesserte Genauigkeit.

3. **Mehrsprachige Unterstützung**:
   - Türkisch, Englisch, Deutsch, Spanisch, Hindi, Japanisch, Niederländisch, Russisch und Chinesisch werden unterstützt.
   - Die Sprachauswahl wird über Flask-Babel gehandhabt.

4. **Dynamische Satellitenkarten**:
   - Zeigt Satellitenbilder der erkannten Orte mithilfe der Google Maps Static API an.

---

## Anforderungen

### Verwendete APIs

- [Google Cloud Vision API](https://cloud.google.com/vision/docs): Für die Bildanalyse.
- [Google Places API](https://developers.google.com/maps/documentation/places/web-service/choose-api):
  - [Standardversion](https://developers.google.com/maps/documentation/places/web-service/search) `app.py`.
  - [Neu Version](https://developers.google.com/maps/documentation/places/web-service/op-overview) `appv2.py`.
- [Google Geocoding API](https://developers.google.com/maps/documentation/geocoding): Für die Umkehrgeokodierung von Koordinaten zu Adressen.
- [Google Maps Static API](https://developers.google.com/maps/documentation/maps-static): Für die Erstellung von Satellitenkartenbildern.
- [Google Custom Search API](https://developers.google.com/custom-search/v1/introduction): Für keywordbasierte Websuchen.

### Python-Bibliotheken

Die folgenden Bibliotheken sind für dieses Projekt erforderlich:

- `Flask`
- `Flask-Babel`
- `requests`
- `spacy`
- `google-cloud-vision`
- `Pillow`
- `python-dotenv`
- `Werkzeug`

---

## Installation

1. Klonen Sie das Repository:
   ```bash
   git clone https://github.com/yourusername/places-api-project.git
   cd places-api-project
   ```

2. Installieren Sie die Abhängigkeiten:
   ```bash
   pip install -r requirements.txt
   ```

3. Installieren Sie das en_core_web_sm Modell:
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. Richten Sie Ihre Google Cloud-Anmeldedaten ein:
   - Erstellen Sie eine `.env`-Datei im Projektverzeichnis mit den folgenden Schlüsseln:
     ```env
     FLASK_SECRET_KEY=IHR_GEHEIMER_SCHLÜSSEL # Mit flask_secret_key_maker.py erstellen
     GOOGLE_APPLICATION_CREDENTIALS=json-datei-name.json
     GEOCODING_API_KEY=API_KEY
     PLACES_API_KEY=${GEOCODING_API_KEY} # Identisch mit GEOCODING_API_KEY
     CUSTOM_SEARCH_JSON_API=${GEOCODING_API_KEY} # Identisch mit GEOCODING_API_KEY
     ```

---

## Nutzung

1. Starten Sie die Anwendung:
   ```bash
   python app.py  # Für Places API
   python appv2.py  # Für Places API (Neu)
   ```

2. Öffnen Sie einen Browser und navigieren Sie zu `http://127.0.0.1:5000`.

3. Laden Sie ein Bild hoch und lassen Sie die Anwendung es analysieren.

---

## Verzeichnisstruktur

```
places-api-project/
├── app.py            # Standard Places API-Implementierung
├── appv2.py          # Neue Places API-Implementierung
├── templates/        # HTML-Vorlagenordner
├── translations/     # Sprachdateienordner
├── static/           # Ordner für statische Dateien (CSS, Bilder)
├── uploads/          # Temporärer Ordner für hochgeladene Bilder (wird automatisch erstellt, muss nicht selbst erstellt werden)
├── .env              # Umgebungsvariablen
├── requirements.txt  # Python-Bibliotheken
```

---

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert. Siehe die [LICENSE](LICENSE)-Datei für Details.

---

## Beispiel
![KonumifyFoto](https://i.imgur.com/6zgPIs9.png)
![KonumifyIndex](https://i.imgur.com/2Rc1OkD.png)
![KonumifyErgebnis](https://i.imgur.com/uzsVpj0.png)
