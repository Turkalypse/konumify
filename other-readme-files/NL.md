![KonumifyLogo](../static/konumify.png)

Deze repository bevat twee versies van een Flask-applicatie die Google Cloud-services gebruikt om afbeeldingsbestanden te analyseren en locatiegebaseerde informatie te extraheren. Het belangrijkste verschil tussen de twee versies is de implementatie van de Places API:

- `app.py`: Gebruikt de Places API.
- `appv2.py`: Gebruikt de Places API (Nieuw).

---

## Functies

1. **Beeldanalyse**:
   - Haalt EXIF-metadata op uit geüploade afbeeldingen.
   - Voert OCR (Optical Character Recognition) uit om tekst in afbeeldingen te analyseren.
   - Gebruikt de Google Cloud Vision API voor herkenning van herkenningspunten en webdetectie.

2. **Integratie met de Google Places API**:
   - Haalt gedetailleerde informatie over locaties op basis van tekstquery's en coördinaten.
   - `appv2.py` maakt gebruik van de nieuwe eindpunten en methoden van de Places API voor verbeterde nauwkeurigheid.

3. **Meertalige ondersteuning**:
   - De applicatie ondersteunt meerdere talen (Turks, Engels, Duits, Spaans, Russisch, Nederlands).
   - Taalkeuze wordt beheerd via Flask-Babel.

4. **Dynamische satellietkaarten**:
   - Toont satellietbeelden van gedetecteerde locaties met behulp van de Google Maps Static API.

---

## Vereisten

### Gebruikte API's

- [Google Cloud Vision API](https://cloud.google.com/vision/docs): Voor beeldanalyse.
- [Google Places API](https://developers.google.com/maps/documentation/places/web-service/choose-api):
  - [Standaardversie](https://developers.google.com/maps/documentation/places/web-service/search) `app.py`.
  - [Nieuwe versie](https://developers.google.com/maps/documentation/places/web-service/op-overview) `appv2.py`.
- [Google Geocoding API](https://developers.google.com/maps/documentation/geocoding): Voor reverse geocodering van coördinaten naar adressen.
- [Google Maps Static API](https://developers.google.com/maps/documentation/maps-static): Voor het genereren van satellietkaartbeelden.
- [Google Custom Search API](https://developers.google.com/custom-search/v1/introduction): Voor zoekopdrachten op basis van trefwoorden.

### Python-bibliotheken

De volgende bibliotheken zijn vereist voor dit project:

- `Flask`
- `Flask-Babel`
- `requests`
- `spacy`
- `google-cloud-vision`
- `Pillow`
- `python-dotenv`
- `Werkzeug`

---

## Installatie

1. Clone de repository:
   ```bash
   git clone https://github.com/yourusername/places-api-project.git
   cd places-api-project
   ```

3. Installeer de vereisten:
   ```bash
   pip install -r requirements.txt
   ```

4. Stel je Google Cloud-referenties in:
   - Maak een `.env`-bestand in de projectmap met de volgende sleutels:
     ```env
     FLASK_SECRET_KEY=UW_GEHEIME_SLEUTEL # Maak een met flask_secret_key_maker.py
     GOOGLE_APPLICATION_CREDENTIALS=json-bestands-naam.json
     GEOCODING_API_KEY=API_KEY
     PLACES_API_KEY=${GEOCODING_API_KEY} # Gelijk aan GEOCODING_API_KEY
     CUSTOM_SEARCH_JSON_API=${GEOCODING_API_KEY} # Gelijk aan GEOCODING_API_KEY
     ```

---

## Gebruik

1. Start de applicatie:
   ```bash
   python app.py  # Voor Places API
   python appv2.py  # Voor Places API (Nieuw)
   ```

2. Open een browser en ga naar `http://127.0.0.1:5000`.

3. Upload een afbeelding en laat de applicatie deze analyseren.

---

## Directorystructuur

```
places-api-project/
├── app.py            # Standaardimplementatie van de Places API
├── appv2.py          # Nieuwe implementatie van de Places API
├── templates/        # HTML-sjablonenmap
├── translations/     # Map met taalbestanden
├── static/           # Map met statische bestanden (CSS, afbeeldingen)
├── uploads/          # Tijdelijke map voor geüploade afbeeldingen (wordt automatisch gegenereerd, hoeft niet handmatig te worden aangemaakt)
├── .env              # Omgevingsvariabelen
├── requirements.txt  # Python-bibliotheken
```

---

## Licentie

Dit project is gelicentieerd onder de MIT-licentie. Zie het bestand [LICENSE](LICENSE) voor meer details.

---

## Bijdragen

Bijdragen zijn welkom! Voel je vrij om de repository te forken, een nieuwe functietak te maken en een pull request in te dienen.

## Voorbeeld
![KonumifyFoto](https://i.ibb.co/fSNRsb9/ERSMS.jpg)
![KonumifyIndex](https://i.ibb.co/2qkG8Jg/1-nl.png)
![KonumifyResultaat](https://i.ibb.co/pj9J63Q/2-nl.png)
