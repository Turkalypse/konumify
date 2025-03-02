# [Click for README files in other languages.](other-readme-files/)

![KonumifyLogosu](static/konumify.png)

Bu depo, Google Cloud hizmetlerini kullanarak görsel dosyalarını analiz eden ve konum tabanlı bilgiler çıkaran iki farklı Flask uygulaması içerir. İki sürüm arasındaki temel fark, Places API'nin uygulanma şeklidir:

- `app.py`: Places API kullanılır.
- `appv2.py`: Places API (New) kullanılır.

---

## Özellikler

1. **Görsel Analizi**:
   - Yüklenen görsellerden EXIF meta verilerini çıkarır.
   - Görsellerdeki metinleri analiz etmek için OCR (Optik Karakter Tanıma) uygular.
   - Google Cloud Vision API'yi kullanarak yer işaretlerini ve web içeriğini algılar.

2. **Google Places API Entegrasyonu**:
   - Metin sorguları ve koordinatlarla konum detaylarını alır.
   - `appv2.py`, gelişmiş doğruluk için yeni Places API uç noktalarını ve yöntemlerini benimser.

3. **Çok Dilli Destek**:
   - Türkçe, İngilizce, Almanca, İspanyolca, Hintçe, Japonca, Felemenkçe, Rusça ve Çince dilleri desteklenmektedir.
   - Dil seçimi Flask-Babel aracılığıyla gerçekleştirilir.

4. **Dinamik Uydu Haritaları**:
   - Google Maps Static API'yi kullanarak algılanan konumların uydu görüntülerini gösterir.

---

## Gereksinimler

### Kullanılan API'ler

- [Google Cloud Vision API](https://cloud.google.com/vision/docs): Görsel analizi için.
- [Google Places API](https://developers.google.com/maps/documentation/places/web-service/choose-api):
  - `app.py` [standart sürüm](https://developers.google.com/maps/documentation/places/web-service/search).
  - `appv2.py` [yeni sürüm](https://developers.google.com/maps/documentation/places/web-service/op-overview).
- [Google Geocoding API](https://developers.google.com/maps/documentation/geocoding): Koordinatları adreslere dönüştürmek için.
- [Google Maps Static API](https://developers.google.com/maps/documentation/maps-static): Uydu haritaları oluşturmak için.
- [Google Custom Engine ID](https://programmablesearchengine.google.com/controlpanel/all): Anahtar kelime tabanlı web aramaları için.
  - Arama motoru kimliği için lazım (yani CX değeri). "Resim arama" ve "Tüm web'de ara" açık olmalı. "Bölge", Türkiye tavsiye edilir.

### Python Kütüphaneleri

Bu projede aşağıdaki kütüphaneler gereklidir:

- `Flask`
- `Flask-Babel`
- `requests`
- `spacy`
- `google-cloud-vision`
- `Pillow`
- `python-dotenv`
- `Werkzeug`

---

## Kurulum

1. Depoyu klonlayın:
   ```bash
   git clone https://github.com/yourusername/places-api-project.git
   cd places-api-project
   ```

2. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

3. en_core_web_sm dil modelini yükleyin:
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. Google Cloud kimlik bilgilerinizi ayarlayın:
   - Proje dizininde `.env` dosyasındaki aşağıdaki gerekli yerleri düzenleyin:
     ```env
     FLASK_SECRET_KEY=GİZLİ-ANAHTAR # flask_secret_key_maker.py dosyasıyla bir tane oluşturun
     GOOGLE_APPLICATION_CREDENTIALS=json-dosya-adi.json
     GEOCODING_API_KEY=API-ANAHTARINIZ
     PLACES_API_KEY=${GEOCODING_API_KEY} # GEOCODING_API_KEY ile aynıdır
     CUSTOM_SEARCH_JSON_API=${GEOCODING_API_KEY} # GEOCODING_API_KEY ile aynıdır
     CUSTOM_SEARCH_ENGINE_ID=arama_motoru_kimliğiniz
     ```

---

## Kullanım

1. Uygulamayı başlatın:
   ```bash
   python app.py  # Places API için
   python appv2.py  # Places API (New) için
   ```

2. Bir tarayıcı açın ve `http://127.0.0.1:5000` adresine gidin.

3. Bir görsel yükleyin ve uygulamanın analiz etmesini bekleyin.

---

## Dizin Yapısı

```
places-api-project/
├── app.py            # Standart Places API uygulaması
├── appv2.py          # Yeni Places API uygulaması
├── templates/        # HTML şablonları klasörü
├── translations/     # Dil dosyaları klasörü
├── static/           # Statik dosyalar klasörü (CSS, görseller)
├── uploads/          # Yüklenen geçici dosyalar klasörü (otomatik olarak oluşturulur, sizin oluşturmanıza gerek yoktur)
├── .env              # Ortam değişkenleri
├── requirements.txt  # Python kütüphaneleri
```

---

## Lisans

Bu proje MIT Lisansı ile lisanslanmıştır. Daha fazla bilgi için [LICENSE](LICENSE) dosyasına bakın.

---

## Örnek
![KonumifyFotograf](https://i.imgur.com/Hkfhnqv.jpeg)
![KonumifyIndex](https://i.imgur.com/ZVxcw74.png)
![KonumifySonuc](https://i.imgur.com/E3niPzb.png)
