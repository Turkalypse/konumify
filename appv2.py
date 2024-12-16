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
from collections import Counter

nlp = spacy.load('en_core_web_sm')

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'x-yyyyyy-zzzzzzzzzzzz.json'
VISION_CLIENT = vision.ImageAnnotatorClient()
GEOCODING_API_KEY = 'API_ANAHTARI' # GEOCODING ve PLACES API (NEW) aynıdır
PLACES_API_KEY = GEOCODING_API_KEY

# Yüklenen fotoğraflar geçici olarak 'uploads' klasörüne (otomatik oluşturulur) kopyalanır ve analiz tamamlanınca yer kaplamamak için silinir.
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
            # 1. EXIF verilerinin kontrolü
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
            if 'error' not in vision_data and all(vision_data.get(key) is not None for key in ('latitude', 'longitude', 'address')):
                print("\033[92mVision API yöntemi ile bulundu\033[0m")
                satellite_image_url = get_satellite_image_url(vision_data['latitude'], vision_data['longitude'])
                return render_template('result.html', place_info=vision_data, satellite_image_url=satellite_image_url)
            else:
                print("\033[93mVision API ile yer bulma başarısız.\033[0m")
                
            # YENİ: Vision API sonuçları yetersizse Web Detection sürecini kullan
            if any(vision_data.get(key) is None for key in ('description', 'latitude', 'longitude', 'address')):
                print("\033[93mSonuçlar yetersiz, Web Detection işleme geçiliyor.\\033[0m")
                vision_data_web = analyze_image_with_web_detection(filepath)
                if 'error' not in vision_data_web:
                    top_keywords = extract_top_keywords(vision_data_web)
                    search_results = search_with_keywords(top_keywords)
                    return render_template('result2.html', top_keywords=top_keywords, search_results=search_results)
                else:
                    print("\033[93mWeb Detection başarısız.\033[0m")

            print("\033[93mAnaliz tamamlandı ancak sonuç bulunamadı. Daha sade veya spesifik bir metin kullanmayı deneyin.\033[0m")
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)

    return render_template('index.html')

# YENİ
def analyze_image_with_web_detection(filepath):
    try:
        with io.open(filepath, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)

        # Web Detection
        response = VISION_CLIENT.web_detection(image=image)
        web_entities = response.web_detection.web_entities
        print("\033[94mWeb Detection Response:\033[0m", response)

        if web_entities:
            print("\033[92mWeb Entity Detection Successful\033[0m")
            return {
                'web_entities': web_entities
            }

        print("\033[93mWeb Detection'da hiçbir sonuç bulunamadı.\033[0m")
        return {'error': 'Herhangi bir web varlığı tespit edilemedi'}

    except Exception as e:
        print(f"\033[91mVision API hatası:\033[0m {e}")
        return {'error': 'Vision API ile analiz edilemedi'}

def extract_top_keywords(vision_data):
    web_entities = vision_data.get('web_entities', [])
    text_data = " ".join([entity.description for entity in web_entities])

    doc = nlp(text_data)
    words = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]
    word_counts = Counter(words)
    top_keywords = [word for word, _ in word_counts.most_common(3)]

    print(f"\033[94mEn çok geçen 3 kelime:\033[0m {top_keywords}")
    return top_keywords

def search_with_keywords(keywords):
    results = []
    try:
        for keyword in keywords:
            search_url = "https://www.googleapis.com/customsearch/v1"
            params = {
                'q': keyword,
                'cx': 'c06054d0f86e8475f',
                'key': GEOCODING_API_KEY,
                'siteSearch': '.tr',
            }
            response = requests.get(search_url, params=params).json()
            if 'items' in response:
                for item in response['items'][:3]:  # İlk 3 sonucu al
                    results.append({
                        'title': item['title'],
                        'url': item['link']
                    })
        print(f"\033[94mArama sonuçları:\033[0m {results}")
    except Exception as e:
        print(f"Google Search API hatası: {e}")
    return results
# YENİ bitiş
    
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
            lat, lng, address = None, None, None

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
            
            # Eğer algılanan metin 2 veya daha az karakter uzunluğundaysa, hemen çık
            if len(detected_text) <= 2:
                print("\033[93mAlgılanan metin 2 veya daha az karakter uzunluğunda, atlanıyor.\033[0m")
                return {'error': 'Metin 2 veya daha az karakter uzunluğunda olduğu için geçersiz.'}
            
            # NLP uygulama
            doc = nlp(detected_text)

            # Temizleme işlemleri
            cleaned_text = clean_text_for_query(detected_text)

            # Varlık tanıma
            entities = [(ent.text, ent.label_) for ent in doc.ents]
            print("\033[92mVarlıklar:\033[0m", entities)

            # Anahtar kelimeleri bulma ve 2 veya daha az karakterli kelimeleri filtreleme
            keywords = set(token.lemma_ for token in doc if token.is_alpha and not token.is_stop and len(token.lemma_) > 2)
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
    """
    Bir yerin detaylarını almak için text query kullanarak çağrı yapar.
    """
    try:
        places_url = "https://places.googleapis.com/v1/places:searchText"
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": api_key,
            "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,places.location"
        }
        payload = {
            "textQuery": query
        }

        response = requests.post(places_url, json=payload, headers=headers).json()

        # API yanıtını kontrol et
        if response.get("places"):
            place = response["places"][0]  # İlk sonucu döner
            return {
                "place_id": place.get("id"),
                "name": place.get("displayName", {}).get("text"),
                "address": place.get("formattedAddress"),
                "latitude": place.get("location", {}).get("latitude"),
                "longitude": place.get("location", {}).get("longitude")
            }
        else:
            return {"error": "Yer bulunamadı."}
    except Exception as e:
        print(f"Places API hatası: {e}")
        return {"error": "API çağrısı başarısız."}

def get_place_details_from_id(place_id, api_key):
    """
    Place ID kullanarak yer detaylarını alır.
    """
    try:
        place_details_url = f"https://places.googleapis.com/v1/places/{place_id}"
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": api_key,
            "X-Goog-FieldMask": "id,displayName,formattedAddress,location"
        }

        response = requests.get(place_details_url, headers=headers).json()

        # API yanıtını kontrol et
        if response.get("displayName"):
            return {
                "description": response.get("displayName", {}).get("text"),
                "latitude": response.get("location", {}).get("latitude"),
                "longitude": response.get("location", {}).get("longitude"),
                "address": response.get("formattedAddress")
            }
        else:
            return {"error": "Yer detayları alınamadı."}
    except Exception as e:
        print(f"Places API detay alım hatası: {e}")
        return {"error": "API çağrısı başarısız."}

if __name__ == '__main__':
    app.run(debug=True)
    
