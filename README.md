# [Click to access the English README](README-EN.md)

![KonumifyLogosu](https://i.ibb.co/f1FJgSF/konumifywhite.png)

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
   - Uygulama, Türkçe, İngilizce, Almanca, İspanyolca, Rusça gibi birden fazla dili destekler.
   - Dil seçimi Flask-Babel aracılığıyla gerçekleştirilir.

4. **Dinamik Uydu Haritaları**:
   - Google Maps Static API'yi kullanarak algılanan konumların uydu görüntülerini gösterir.

---

## Gereksinimler

### Kullanılan API'ler

- [Google Cloud Vision API](https://cloud.google.com/vision/docs): Görsel analizi için.
- [Google Places API](https://developers.google.com/maps/documentation/places/web-service/choose-api):
  - `app.py` [standart sürüm](https://developers.google.com/maps/documentation/places/web-service/).
  - `appv2.py` [yeni sürüm](https://developers.google.com/maps/documentation/places/web-service/op-overview).
- [Google Geocoding API](https://developers.google.com/maps/documentation/geocoding): Koordinatları adreslere dönüştürmek için.
- [Google Maps Static API](https://developers.google.com/maps/documentation/maps-static): Uydu haritaları oluşturmak için.
- [Google Custom Search API](https://developers.google.com/custom-search/v1/introduction): Anahtar kelime tabanlı web aramaları için.

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

3. Google Cloud kimlik bilgilerinizi ayarlayın:
   - Proje dizininde `.env` dosyasındaki aşağıdaki gerekli yerleri düzenleyin:
     ```env
     FLASK_SECRET_KEY=GİZLİ_ANAHTAR # flask_secret_key_maker.py dosyasıyla bir tane oluşturun
     GOOGLE_APPLICATION_CREDENTIALS=json-dosya-adi.json
     GEOCODING_API_KEY=API_ANAHTARI
     PLACES_API_KEY=${GEOCODING_API_KEY} # GEOCODING_API_KEY ile aynıdır
     CUSTOM_SEARCH_JSON_API=${GEOCODING_API_KEY} # GEOCODING_API_KEY ile aynıdır
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

## Katkılar

Katkılar memnuniyetle karşılanır! Depoyu fork'layarak, bir özellik dalı oluşturarak ve bir pull request göndererek katkıda bulunabilirsiniz.

## Örnek
![KonumifyFotograf](https://i.ibb.co/2FkwxF5/FSM.jpg)
![KonumifyIndex](https://i.ibb.co/wyFBXjG/1.jpg)
![KonumifySonuc](https://i.ibb.co/gPQ34zc/2.jpg)
