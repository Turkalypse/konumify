import os
import io
import re
import logging
import requests
import spacy
from flask import Flask, render_template, request, session, redirect
from flask_babel import Babel, _
from werkzeug.utils import secure_filename
from google.cloud import vision
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS, GPSTAGS
from collections import Counter
from dotenv import load_dotenv

load_dotenv()

nlp = spacy.load('en_core_web_sm')

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

app.secret_key = os.getenv('FLASK_SECRET_KEY')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
VISION_CLIENT = vision.ImageAnnotatorClient()
GEOCODING_API_KEY = os.getenv('GEOCODING_API_KEY')
PLACES_API_KEY = os.getenv('PLACES_API_KEY')
CUSTOM_SEARCH_JSON_API = os.getenv('CUSTOM_SEARCH_JSON_API')
CUSTOM_SEARCH_ENGINE_ID = os.getenv('CUSTOM_SEARCH_ENGINE_ID')

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

LANGUAGES = {
    'tr': 'Türkçe',
    'en': 'English',
    'de': 'Deutsch',
    'nl': 'Nederlands',
    'es': 'Español',
    'ru': 'Русский',
    'hi': 'हिन्दी',
    'zh': '中文',
    'ja': '日本語'
}

babel = Babel()

def get_locale():
    return session.get('lang', request.accept_languages.best_match(LANGUAGES.keys()))

babel.init_app(app, locale_selector=get_locale)

@app.context_processor
def inject_locale():
    return dict(get_locale=get_locale)

app.config['BABEL_DEFAULT_LOCALE'] = 'tr'

@app.route('/set_language', methods=['POST'])
def set_language():
    language = request.form.get('language')
    if language in LANGUAGES:
        session['lang'] = language
    print("Session güncellendi:", session)
    return redirect(request.referrer)

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
            exif_data = extract_exif(filepath)
            if exif_data:
                print("\033[92mEXIF yöntemi ile bulundu\033[0m")
                satellite_image_url = get_satellite_image_url(exif_data['latitude'], exif_data['longitude'])
                return render_template('sonuc.html', place_info=exif_data, satellite_image_url=satellite_image_url)
                print("\033[94mEXIF dönüş değeri:\033[0m {exif_data}")
                return render_template('sonuc.html', place_info=exif_data)
            else:
                print("\033[93mEXIF verisi bulunamadı, diğer yöntemlere geçiliyor…\033[0m")

            ocr_data = analyze_image_with_ocr(filepath)
            if ocr_data:
                place_details = get_place_details(ocr_data['cleaned_text'], PLACES_API_KEY)
                if 'place_id' in place_details:
                    detailed_place = get_place_details_from_id(place_details['place_id'], PLACES_API_KEY)
                    if detailed_place:
                        print("\033[92mOCR ve Places API yöntemi ile bulundu\033[0m")
                        satellite_image_url = get_satellite_image_url(detailed_place['latitude'], detailed_place['longitude'])
                        return render_template('sonuc.html', place_info=detailed_place, satellite_image_url=satellite_image_url)
                else:
                    print("\033[93mPlaces API ile yer bulma başarısız. Diğer yöntemlere geçiliyor…\033[0m")
            else:
                print("\033[93mOCR ile yeterli metin algılanamadı, diğer yöntemlere geçiliyor...\033[0m")

            vision_data = analyze_image(filepath)
            if 'error' not in vision_data and all(vision_data.get(key) is not None for key in ('latitude', 'longitude', 'address')):
                print("\033[92mVision API yöntemi ile bulundu\033[0m")
                satellite_image_url = get_satellite_image_url(vision_data['latitude'], vision_data['longitude'])
                return render_template('sonuc.html', place_info=vision_data, satellite_image_url=satellite_image_url)
            else:
                print("\033[93mVision API ile yer bulma başarısız. Diğer yöntemlere geçiliyor...\033[0m")

            if any(vision_data.get(key) is None for key in ('description', 'latitude', 'longitude', 'address')):
                print("\033[93mSonuçlar yetersiz, Web Detection işleme geçiliyor.\033[0m")
                vision_data_web = analyze_image_with_web_detection(filepath)
                if 'error' not in vision_data_web:
                    top_keywords = extract_top_keywords(vision_data_web)
                    if not top_keywords or len(top_keywords) < 3:
                        top_keywords = [("Bilinmiyor", 0)] * 3
                    search_results = search_with_keywords(top_keywords)
                    return render_template('bulunamadi.html', top_keywords=top_keywords, search_results=search_results)
                else:
                    print("\033[93mWeb Detection başarısız.\033[0m")

            print("\033[93mAnaliz tamamlandı ancak sonuç bulunamadı. Daha sade veya spesifik bir metin kullanmayı deneyin.\033[0m")

        finally:
            if os.path.exists(filepath):
                os.remove(filepath)

    return render_template('index.html')

# EXIF kısmı

def get_exif_data(image_path):
    img = Image.open(image_path)
    exif_data = img._getexif()
    if not exif_data:
        return None

    gps_info = {}
    for tag, value in exif_data.items():
        tag_name = TAGS.get(tag, tag)
        if tag_name == "GPSInfo":
            for key in value.keys():
                sub_tag = GPSTAGS.get(key, key)
                gps_info[sub_tag] = value[key]

    return gps_info

def convert_to_degrees(value):
    d, m, s = value
    return d + (m / 60.0) + (s / 3600.0)

def extract_exif(filepath):
    try:
        image = Image.open(filepath)
        exif_data = image._getexif()
        
        if not exif_data:
            print("\033[91mEXIF verisi bulunamadı.\033[0m")
            return None
        
        exif = {ExifTags.TAGS.get(tag, tag): value for tag, value in exif_data.items() if tag in ExifTags.TAGS}
        
        gps_info = exif.get("GPSInfo")
        print(f"\033[94mGPSInfo içeriği:\033[0m {gps_info}")
        
        if gps_info:
            coordinates = get_coordinates(gps_info)
            print(f"\033[92mEXIF koordinatları bulundu:\033[0m {coordinates}")
            
            if coordinates:
                address = get_address_from_coordinates(coordinates[0], coordinates[1])
                return {
                    'description': address,
                    'latitude': coordinates[0],
                    'longitude': coordinates[1],
                    'address': address
                }
        else:
            print("\033[93mGPSInfo bulunamadı.\033[0m")
            return None
    except Exception as e:
        print(f"\033[91mEXIF verileri okunamadı: {e}\033[0m")
        return None
        
# EXIF kısmı

def get_coordinates(gps_info):
    if gps_info is None:
        return None

    gps_latitude = gps_info.get(2)
    gps_latitude_ref = gps_info.get(1)
    gps_longitude = gps_info.get(4)
    gps_longitude_ref = gps_info.get(3)

    if not gps_latitude or not gps_longitude:
        return None

    lat = convert_to_degrees(gps_latitude)
    lon = convert_to_degrees(gps_longitude)

    if isinstance(gps_latitude_ref, bytes):
        gps_latitude_ref = gps_latitude_ref.decode()
    if isinstance(gps_longitude_ref, bytes):
        gps_longitude_ref = gps_longitude_ref.decode()

    if gps_latitude_ref == 'S':
        lat = -lat
    if gps_longitude_ref == 'W':
        lon = -lon

    return lat, lon

def get_address_from_coordinates(lat, lng):
    try:
        geocoding_url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={GEOCODING_API_KEY}"
        response = requests.get(geocoding_url).json()

        if response.get('results'):
            return response['results'][0]['formatted_address']
        else:
            return "Adres bulunamadı"
    except Exception as e:
        print(f"\033[91mGeocoding API hatası:\033[0m {e}")
        return "Adres alınamadı"

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

def analyze_image_with_web_detection(filepath):
    try:
        with io.open(filepath, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)

        response = VISION_CLIENT.web_detection(image=image)
        web_detection = response.web_detection
        print("\033[94mWeb Detection Response:\033[0m", response)

        if web_detection:
            print("\033[92mWeb Detection Başarılı\033[0m")

            web_data = {
                'full_matching_images': [image.url for image in web_detection.full_matching_images],
                'partial_matching_images': [image.url for image in web_detection.partial_matching_images],
                'pages_with_matching_images': [
                    {'url': page.url, 'title': page.page_title} for page in web_detection.pages_with_matching_images
                ]
            }
            return web_data
        else:
            print("\033[93mWeb Detection'da hiçbir sonuç bulunamadı.\033[0m")
            return {'error': 'Herhangi bir web verisi tespit edilemedi'}

    except Exception as e:
        print(f"\033[91mVision API hatası:\033[0m {e}")
        return {'error': 'Vision API ile analiz edilemedi'}

def extract_top_keywords(web_data):
    """
    Web Detection verilerinden URL'ler ve page_title'lardaki kelimeleri analiz eder.
    Alan adları, uzantılar, tamamen sayılardan oluşan ifadeler ve "com" gibi gereksiz kelimeleri filtreler.
    """
    ignore_list = {"https", "http", "www", "net", "org", "jpg", "png", "jpeg", 
                   "webp", "html", "php", "uploads", "cdn", "storage", "crop", 
                   "images", "resize", "files", "com", "thumbs", "content"}

    word_counts_per_source = {}

    def analyze_text(source, text, category):
        clean_text = re.sub(r'[^\w\s]', ' ', text)
        clean_text = re.sub(r'\b\d+\b', '', clean_text)
        
        words = [word.lower() for word in clean_text.split() 
                 if len(word) > 2 and word.lower() not in ignore_list]
        
        if source not in word_counts_per_source:
            word_counts_per_source[source] = {'URL': Counter(), 'page_title': Counter()}
        word_counts_per_source[source][category].update(words)

    if 'full_matching_images' in web_data:
        source_name = 'full_matching_images'
        for url in web_data[source_name]:
            analyze_text(source_name, url, 'URL')

    if 'partial_matching_images' in web_data:
        source_name = 'partial_matching_images'
        for url in web_data[source_name]:
            analyze_text(source_name, url, 'URL')

    if 'pages_with_matching_images' in web_data:
        source_name = 'pages_with_matching_images'
        for page in web_data[source_name]:
            analyze_text(source_name, page['url'], 'URL')
            analyze_text(source_name, page['title'], 'page_title')

    print("\n\033[94mKaynaklara Göre Kelime Sayımları (URL ve Page Title Ayrımı):\033[0m")
    for source, categories in word_counts_per_source.items():
        print(f"\n\033[92m{source}:\033[0m")
        for category, counts in categories.items():
            print(f"  \033[93m{category}:\033[0m")
            for word, count in counts.most_common(5):
                print(f"    {word}: {count}")

    total_word_counts = Counter()
    for categories in word_counts_per_source.values():
        for counts in categories.values():
            total_word_counts.update(counts)

    print("\n\033[94mTüm Kaynaklardan En Çok Geçen 3 Kelime:\033[0m")
    for word, count in total_word_counts.most_common(3):
        print(f"  {word}: {count}")

    return total_word_counts.most_common(3)

def search_with_keywords(keywords):
    results = []
    try:
        for keyword, _ in keywords:
            print(f"\n\033[94m'{keyword}' kelimesi Google'da aratılıyor...\033[0m")
            search_url = "https://www.googleapis.com/customsearch/v1"
            params = {
                'q': keyword,
                'cx': CUSTOM_SEARCH_ENGINE_ID,
                'key': CUSTOM_SEARCH_JSON_API,
                'lr': 'lang_tr',
                'siteSearch': 'tr'
            }
            response = requests.get(search_url, params=params)

            if response.status_code != 200:
                print(f"\033[91mHata: HTTP {response.status_code}\033[0m")
                if response.status_code == 403:
                    error_message = response.json().get('error', {}).get('message', 'Yetkilendirme veya kota hatası')
                    print(f"\033[93mDetay:\033[0m {error_message}")
                    if "quota" in error_message.lower():
                        print("\033[91mKota sınırı aşılmış! API kotasını kontrol edin.\033[0m")
                continue

            json_response = response.json()
            total_results = json_response.get('searchInformation', {}).get('totalResults', '0')
            print(f"\033[92mToplam sonuç sayısı:\033[0m {total_results}")

            if 'items' in json_response:
                print(f"\033[93m'{keyword}' için bulunan ilk 3 başlık:\033[0m")
                for item in json_response['items'][:3]:
                    title = item['title']
                    link = item['link']
                    print(f"  - \033[96mBaşlık:\033[0m {title}")
                    print(f"    \033[96mURL:\033[0m {link}")
                    results.append({
                        'title': title,
                        'url': link
                    })
            else:
                print(f"\033[91m'{keyword}' için sonuç bulunamadı.\033[0m")
    except Exception as e:
        print(f"\033[91mGoogle Search API hatası:\033[0m {e}")
    return results

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

# OCR kontrol kısmı

def is_valid_text(text):
    if re.match(r'^\d+$', text):
        return False
    if re.match(r'\d{4}[-/]\d{2}[-/]\d{2}', text):
        return False
    return True

def analyze_image_with_ocr(filepath):
    try:
        with io.open(filepath, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = VISION_CLIENT.text_detection(image=image)
        texts = response.text_annotations
        
        if texts:
            detected_text = texts[0].description.strip()
            
            if len(detected_text) <= 3 or not is_valid_text(detected_text):
                print("\033[93mGeçersiz metin tespit edildi, geçiliyor...\033[0m")
                return None
            
            doc = nlp(detected_text)

            cleaned_text = clean_text_for_query(detected_text)

            entities = [(ent.text, ent.label_) for ent in doc.ents if len(ent.text) > 3 and not ent.text.isdigit()]
            print("\033[92mVarlıklar:\033[0m", entities)

            keywords = {token.lemma_ for token in doc if token.is_alpha and not token.is_stop and len(token.lemma_) > 3}
            print("\033[92mAnahtar Kelimeler:\033[0m", keywords)

            return {'text': detected_text, 'cleaned_text': cleaned_text, 'entities': entities, 'keywords': list(keywords)}
        else:
            print("\033[93mMetin algılanamadı, diğer yöntemlere geçiliyor...\033[0m")
            return None
    except Exception as e:
        print(f"\033[91mOCR işlemi sırasında hata: {e}\033[0m")
        return None

def clean_text_for_query(text):
    return ' '.join(word for word in text.split() if word.isalnum() and len(word) > 3)
	
# OCR kontrol kısmı

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
    
