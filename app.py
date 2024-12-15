import os
import io
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from google.cloud import vision
import logging
import requests
import spacy
from PIL import Image
from PIL.ExifTags import TAGS

nlp = spacy.load('en_core_web_sm')

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'x-yyyyyy-zzzzzzzzzzzz.json'
VISION_CLIENT = vision.ImageAnnotatorClient()
GEOCODING_API_KEY = 'API_ANAHTARI'
PLACES_API_KEY = GEOCODING_API_KEY

# Yüklenen fotoğraflar geçici olarak 'uploads' klasörüne (otomatik oluşturulur) kopyalanır ve analiz tamamlanınca yer kaplamamak için silinir
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            print("\033[91mDosya yüklenmedi\033[0m")
            return "Dosya yüklenmedi"
        file = request.files['file']
        if file.filename == '':
            print("\033[91mDosya seçilmedi\033[0m")
            return "Dosya seçilmedi"
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            # 1. EXIF verilerininin kontrolü
            exif_data = extract_exif(filepath)
            if exif_data:
                print("\033[92mEXIF yöntemi ile bulundu\033[0m")
                return render_template('result.html', place_info=exif_data)
            else:
                print("\033[93mEXIF verisi bulunamadı, diğer yöntemlere geçiliyor…\033[0m")

            # 2.1. OCR ile metin algılama ve yer bilgisi bulma
            ocr_data = analyze_image_with_ocr(filepath)
            if 'text' in ocr_data:
                cleaned_text = clean_text_for_query(ocr_data['text'])
                print(f"\033[94mAlgılanan Metin: {ocr_data['text']}\033[0m")

                # 2.2. Places API ile analiz
                place_details = get_place_details(cleaned_text, PLACES_API_KEY)
                if 'place_id' in place_details:
                    detailed_place = get_place_details_from_id(place_details['place_id'], PLACES_API_KEY)
                    if detailed_place:
                        print("\033[92mOCR ve Places API yöntemi ile bulundu\033[0m")
                        satellite_image_url = get_satellite_image_url(detailed_place['latitude'], detailed_place['longitude'])
                        return render_template('result.html', place_info=detailed_place, satellite_image_url=satellite_image_url)
                else:
                    print("\033[93mPlaces API ile yer bulma başarısız. Diğer yöntemlere geçiliyor…\033[0m")
            else:
                print("\033[93mOCR ile metin algılama başarısız. Diğer yöntemlere geçiliyor…\033[0m")

            # 3. Vision API ile analiz
            vision_data = analyze_image(filepath)
            if 'error' not in vision_data:
                print("\033[92mVision API yöntemi ile bulundu\033[0m")
                satellite_image_url = get_satellite_image_url(vision_data['latitude'], vision_data['longitude'])
                return render_template('result.html', place_info=vision_data, satellite_image_url=satellite_image_url)
            else:
                print("\033[93mVision API ile yer bulma başarısız.\033[0m")

            print("\033[93mAnaliz tamamlandı ancak sonuç bulunamadı. Daha sade veya spesifik bir metin kullanmayı deneyin.\033[0m")
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)

    return render_template('index.html')

# EXIF verilerini çekme
def extract_exif(filepath):
    try:
        image = Image.open(filepath)
        exif_data = image._getexif()
        if exif_data:
            gps_info = {}
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                if tag_name == 'GPSInfo':
                    gps_info = value
            if gps_info:
                lat, lng = get_coordinates(gps_info)
                if lat and lng:
                    address = get_address_from_coordinates(lat, lng)
                    if address:
                        return {
                            'description': 'EXIF GPS verisi bulundu.',
                            'latitude': lat,
                            'longitude': lng,
                            'address': address
                        }
        print("\033[93mEXIF verisi eksik bilgi nedeniyle başarısız.\033[0m")
        return None
    except Exception as e:
        print(f"EXIF okuma hatası: {e}")
        return None

# Koordinatların alımı
def get_coordinates(gps_info):
    def convert_to_degrees(value):
        d = value[0][0] / value[0][1]
        m = value[1][0] / value[1][1]
        s = value[2][0] / value[2][1]
        return d + (m / 60.0) + (s / 3600.0)

    try:
        lat = convert_to_degrees(gps_info[2])
        if gps_info[1] == 'S':
            lat = -lat
        lng = convert_to_degrees(gps_info[4])
        if gps_info[3] == 'W':
            lng = -lng
        return lat, lng
    except KeyError:
        return None, None

# Adresin alımı
def get_address_from_coordinates(lat, lng):
    try:
        geocoding_url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={GEOCODING_API_KEY}"
        geocoding_response = requests.get(geocoding_url).json()
        return geocoding_response['results'][0]['formatted_address'] if geocoding_response['results'] else "Adres bulunamadı"
    except Exception as e:
        print(f"Geocoding hatası: {e}")
        return "Adres alınamadı"

# Google Maps Static API ile uydu görüntüsü
def get_satellite_image_url(lat, lng):
    static_map_url = "https://maps.googleapis.com/maps/api/staticmap?"
    params = {
        "center": f"{lat},{lng}",
        "zoom": "15",
        "size": "600x300",
        "maptype": "satellite",
        "key": GEOCODING_API_KEY
    }
    response = f"{static_map_url}{requests.compat.urlencode(params)}"
    return response

# Vision API ile resim analizi
def analyze_image(filepath):
    try:
        with io.open(filepath, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)

        # 1. Landmark Detection
        response = VISION_CLIENT.landmark_detection(image=image)
        landmarks = response.landmark_annotations
        print("\033[94mLandmark Detection Response:\033[0m", response)
        if landmarks:
            landmark = landmarks[0]
            description = landmark.description
            lat = landmark.locations[0].lat_lng.latitude
            lng = landmark.locations[0].lat_lng.longitude
            address = get_address_from_coordinates(lat, lng)
            print("\033[92mLandmark Detection Successful:\033[0m", {
                'description': description,
                'latitude': lat,
                'longitude': lng,
                'address': address
            })
            return {
                'description': description,
                'latitude': lat,
                'longitude': lng,
                'address': address
            }

        # 2. Web Detection
        response = VISION_CLIENT.web_detection(image=image)
        web_entities = response.web_detection.web_entities
        print("\033[94mWeb Detection Response:\033[0m", response)
        if web_entities:
            primary_entity = max(web_entities, key=lambda e: e.score if e.description else 0)
            description = primary_entity.description if primary_entity and primary_entity.description else "Belirlenemedi"
            lat, lng = None, None
            address = None

            if description:
                geocode_result = get_coordinates_from_description(description)
                if geocode_result:
                    lat, lng = geocode_result.get('latitude'), geocode_result.get('longitude')
                    address = geocode_result.get('address')

            print("\033[92mWeb Detection Successful:\033[0m", {
                'description': description,
                'latitude': lat,
                'longitude': lng,
                'address': address
            })
            return {
                'description': description,
                'latitude': lat,
                'longitude': lng,
                'address': address
            }

        print("\033[93mNo Results Found:\033[0m Landmark ve Web Detection başarısız.")
        return {'error': 'Herhangi bir yer veya web varlığı tespit edilemedi'}

    except Exception as e:
        print(f"\033[91mVision API hatası:\033[0m {e}")
        return {'error': 'Vision API ile analiz edilemedi'}

def get_coordinates_from_description(description):
    """Description kullanarak Google Maps Geocoding API'den koordinat ve adres alır."""
    try:
        geocoding_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={description}&key={GEOCODING_API_KEY}"
        response = requests.get(geocoding_url).json()
        if response.get('results'):
            location = response['results'][0]['geometry']['location']
            address = response['results'][0]['formatted_address']
            return {
                'latitude': location['lat'],
                'longitude': location['lng'],
                'address': address
            }
        else:
            print("\033[93mGeocoding API'den sonuç alınamadı.\033[0m")
            return None
    except Exception as e:
        print(f"\033[91mGeocoding API hatası:\033[0m {e}")
        return None

def analyze_image_with_ocr(filepath):
    try:
        with io.open(filepath, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = VISION_CLIENT.text_detection(image=image)
        texts = response.text_annotations
        if texts:
            detected_text = texts[0].description
            
            # NLP uygulama
            doc = nlp(detected_text)

            # Temizleme işlemleri
            cleaned_text = clean_text_for_query(detected_text)

            # Varlık tanıma
            entities = [(ent.text, ent.label_) for ent in doc.ents]
            print("\033[92mVarlıklar:\033[0m", entities)

            # Anahtar kelimeleri bulma
            keywords = set(token.lemma_ for token in doc if token.is_alpha and not token.is_stop)
            print("\033[92mAnahtar Kelimeler:\033[0m", keywords)

            return {'text': detected_text, 'cleaned_text': cleaned_text, 'entities': entities, 'keywords': list(keywords)}
        else:
            return {'error': 'Metin algılanamadı'}
    except Exception as e:
        print(f"OCR işlemi sırasında hata: {e}")
        return {'error': 'OCR işlemi başarısız'}

def clean_text_for_query(text):
    return ' '.join(word for word in text.split() if word.isalnum())

# Places API ile yer bilgisi almak için burada…

def get_place_details(query, api_key):
    """Metin sorgusundan yer detaylarını alır."""
    try:
        places_url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={query}&inputtype=textquery&fields=place_id&key={api_key}"
        response = requests.get(places_url).json()
        return response
    except Exception as e:
        print(f"Places API hatası: {e}")
        return {}

def get_place_details_from_id(place_id, api_key):
    """Place ID'den yer detaylarını alır."""
    try:
        place_details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}"
        response = requests.get(place_details_url).json()
        if 'result' in response:
            result = response['result']
            location = result['geometry']['location']
            return {
                'description': result.get('name'),
                'latitude': location.get('lat'),
                'longitude': location.get('lng'),
                'address': result.get('formatted_address')
            }
        return None
    except Exception as e:
        print(f"Places API detay alım hatası: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True)
