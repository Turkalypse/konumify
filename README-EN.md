![KonumifyLogosu](https://i.ibb.co/f1FJgSF/konumifywhite.png)

This repository contains two versions of a Flask application that utilizes Google Cloud services to analyze image files and extract location-based information. The key difference between the two versions is the implementation of the Places API:

- `app.py`: Uses the standard Places API.
- `appv2.py`: Utilizes the new Places API.

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
   - Application supports multiple languages (Turkish, English, German, Spanish, Russian).
   - Language selection is handled via Flask-Babel.

4. **Dynamic Satellite Maps**:
   - Displays satellite images of detected locations using Google Maps Static API.

---

## Requirements

### APIs Used

- **Google Cloud Vision API**: For image analysis.
- **Google Places API**:
  - Standard version in `app.py`.
  - New version in `appv2.py`.
- **Google Geocoding API**: For reverse geocoding coordinates to addresses.
- **Google Maps Static API**: For generating satellite map images.
- **Google Custom Search API**: For keyword-based web searches.

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
   git clone https://github.com/yourusername/places-api-project.git
   cd places-api-project
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your Google Cloud credentials:
   - Create a `.env` file in the project directory with the following keys:
     ```env
     FLASK_SECRET_KEY=YOUR_SECRET_KEY # Create one with flask_secret_key_maker.py
     GOOGLE_APPLICATION_CREDENTIALS=json-file-name.json
     GEOCODING_API_KEY=API_KEY
     PLACES_API_KEY=${GEOCODING_API_KEY} # Same with GEOCODING_API_KEY
     CUSTOM_SEARCH_JSON_API=${GEOCODING_API_KEY} # Same with GEOCODING_API_KEY ile aynıdır
     ```

---

## Usage

1. Start the application:
   ```bash
   python app.py  # For standard Places API
   python appv2.py  # For new Places API
   ```

2. Open a browser and navigate to `http://127.0.0.1:5000`.

3. Upload an image and let the application analyze it.

---

## Directory Structure

```
places-api-project/
├── app.py            # Standard Places API implementation
├── appv2.py          # New Places API implementation
├── templates/        # HTML templates
├── translations/     # Language files
├── static/           # Static files (CSS, images)
├── uploads/          # Temporary folder for uploaded images
├── .env              # Environment variables
├── requirements.txt  # Python dependencies
└── README.md         # Project documentation
```

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contributions

Contributions are welcome! Feel free to fork the repository, create a feature branch, and submit a pull request.

## Sample
![KonumifyPhoto](https://i.ibb.co/2FkwxF5/FSM.jpg)
![KonumifyIndex](https://i.ibb.co/YthQtmB/1-en.jpg)
![KonumifyResult](https://i.ibb.co/jVgyWXm/2-en.jpg)
