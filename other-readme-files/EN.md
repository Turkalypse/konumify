![KonumifyLogosu](../static/konumify.png)

This repository contains two versions of a Flask application that utilizes Google Cloud services to analyze image files and extract location-based information. The key difference between the two versions is the implementation of the Places API:

- `app.py`: Uses the Places API.
- `appv2.py`: Utilizes the Places API (New).

---

## Features

1. **Image Analysis**:
   - Extracts EXIF metadata from uploaded images.
   - Performs OCR (Optical Character Recognition) to analyze text in images.
   - Uses Google Cloud Vision API for landmark detection and web detection.

2. **Google Places API Integration**:
   - Retrieves detailed information about locations from text queries and coordinates.
   - `appv2.py` adopts the new Places API endpoints and methods for enhanced accuracy.

3. **Multi-language Support**:
   - Turkish, English, German, Spanish, Hindi, Japanese, Dutch, Russian, and Chinese languages are supported.
   - Language selection is handled via Flask-Babel.

4. **Dynamic Satellite Maps**:
   - Displays satellite images of detected locations using Google Maps Static API.

---

## Requirements

### APIs Used

- [Google Cloud Vision API](https://cloud.google.com/vision/docs): For image analysis.
- [Google Places API](https://developers.google.com/maps/documentation/places/web-service/choose-api):
  - [Standard version](https://developers.google.com/maps/documentation/places/web-service/search) `app.py`.
  - [New version](https://developers.google.com/maps/documentation/places/web-service/op-overview) `appv2.py`.
- [Google Geocoding API](https://developers.google.com/maps/documentation/geocoding): For reverse geocoding coordinates to addresses.
- [Google Maps Static API](https://developers.google.com/maps/documentation/maps-static): For generating satellite map images.
- [Google Custom Engine ID](https://programmablesearchengine.google.com/controlpanel/all): For keyword-based web searches.
  - Search engine ID is required (i.e., the CX value). 'Image search' and 'Search the entire web' must be enabled. It is recommended to set your country for the 'Region'.

### Python Libraries

The following libraries are required for this project:

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

1. Clone the repository:
   ```bash
   git clone https://github.com/Turkalypse/konumify
   cd konumify
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install the en_core_web_sm model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. Set up your Google Cloud credentials:
   - Create a `.env` file in the project directory with the following keys:
     ```env
     FLASK_SECRET_KEY=YOUR-SECRET-KEY # Create one with flask_secret_key_maker.py
     GOOGLE_APPLICATION_CREDENTIALS=json-file-name.json
     GEOCODING_API_KEY=YOUR-API-KEY
     PLACES_API_KEY=${GEOCODING_API_KEY} # Same with GEOCODING_API_KEY
     CUSTOM_SEARCH_JSON_API=${GEOCODING_API_KEY} # Same with GEOCODING_API_KEY ile aynıdır
     CUSTOM_SEARCH_ENGINE_ID=your-search-engine-ID
     ```

---

## Usage

1. Start the application:
   ```bash
   python app.py  # For Places API
   python appv2.py  # For Places API (New)
   ```

2. Open a browser and navigate to `http://127.0.0.1:5000`.

3. Upload an image and let the application analyze it.

---

## Directory Structure

```
places-api-project/
├── app.py            # Standard Places API implementation
├── appv2.py          # New Places API implementation
├── templates/        # HTML templates folder
├── translations/     # Language files folder
├── static/           # Static files folder (CSS, images)
├── uploads/          # Temporary folder for uploaded images (automatically generated, no need to create it yourself)
├── .env              # Environment variables
├── requirements.txt  # Python libraries
```

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Sample
![KonumifyPhoto](https://i.imgur.com/XCFBe3B.jpeg)
![KonumifyIndex](https://i.imgur.com/2Jhlrmn.png)
![KonumifyResult](https://i.imgur.com/6XamAqd.png)
