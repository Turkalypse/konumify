# Places API Project

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

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your Google Cloud credentials:
   - Create a `.env` file in the project directory with the following keys:
     ```env
     FLASK_SECRET_KEY=your_secret_key
     GOOGLE_APPLICATION_CREDENTIALS=path_to_your_service_account_key.json
     GEOCODING_API_KEY=your_geocoding_api_key
     PLACES_API_KEY=your_places_api_key
     CUSTOM_SEARCH_JSON_API=your_custom_search_api_key
     ```

5. Create an `uploads` folder in the project root:
   ```bash
   mkdir uploads
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
├── static/           # Static files (CSS, JS, images)
├── uploads/          # Temporary folder for uploaded images
├── .env              # Environment variables (not included in the repository)
├── requirements.txt  # Python dependencies
└── README.md         # Project documentation
```

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contributions

Contributions are welcome! Feel free to fork the repository, create a feature branch, and submit a pull request.
