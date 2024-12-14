# Flask ile Görüntü Analizi ve Konum Tespiti

Bu Flask web uygulaması, EXIF meta verileri, OCR (Optik Karakter Tanıma) ve Google Vision API gibi çeşitli yöntemlerle görüntü analizi ve konum tespiti yapar. Uygulama, görüntülerden metin çıkarabilir, coğrafi konum bilgilerini analiz edebilir ve ayrıntılı yer açıklamaları ve uydu görüntüleri sunabilir.

## Projede Kullanılan API'ler

### 1. Google Vision API
- **Amaç**: Görüntüleri analiz etmek ve içindeki yer işaretlerini, metinleri ve diğer görsel özellikleri tespit etmek için kullanılır.
- **Dokümantasyon**: [Google Vision API Dokümantasyonu](https://cloud.google.com/vision/docs)

### 2. Google Geocoding API
- **Amaç**: GPS koordinatlarından (enlem ve boylam) adres bilgisi elde etmek için kullanılır.
- **Dokümantasyon**: [Geocoding API Dokümantasyonu](https://developers.google.com/maps/documentation/geocoding/start)

### 3. Google Places API
- **Amaç**: Metin sorgusu veya yer kimliğinden (Place ID) yer detayları, adı, adresi ve coğrafi konumu almak için kullanılır.
- **Dokümantasyon**: [Places API Dokümantasyonu](https://developers.google.com/maps/documentation/places/web-service/overview)

### 4. Google Maps Static API
- **Amaç**: Coğrafi koordinatlara dayalı statik harita görüntüleri oluşturmak için kullanılır (uydu görüntüleri dahil).
- **Dokümantasyon**: [Google Maps Static API Dokümantasyonu](https://developers.google.com/maps/documentation/static-maps)

## Gereksinimler

### Bağlımlıkları Yüklemek
Gerekli bağlımlıkları aşağıdaki komutla yükleyebilirsiniz:

```bash
pip install -r requirements.txt
```

### `requirements.txt`

Bu projede kullanılan gerekli Python paketleri:

```
Flask
google-cloud-vision
requests
spacy
pillow
werkzeug
```

### Google Cloud Kimlik Bilgileri
Uygulamayı çalıştırmadan önce Google Cloud kimlik bilgilerinizi ayarladığınızdan emin olun:
1. Bir Google Cloud projesi oluşturun ve Vision API ile Geocoding API'yi etkinleştirin.
2. Google Cloud projeniz için JSON anahtar dosyasını indirin.
3. `GOOGLE_APPLICATION_CREDENTIALS` ortam değişkenini JSON anahtar dosyanızın yoluna ayarlayın:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credentials.json"
```

### Ortam Değişkenleri
- `GOOGLE_APPLICATION_CREDENTIALS`: Google Cloud kimlik bilgileri dosyanızın yolu.
- `GEOCODING_API_KEY`: Google Geocoding API anahtarınız.
- `PLACES_API_KEY`: Google Places API anahtarı (Geocoding API anahtarıyla aynı olabilir).

## Uygulamayı Çalıştırma
1. Depoyu yerel makinenize klonlayın:
   ```bash
   git clone https://github.com/yourusername/yourproject.git
   cd yourproject
   ```
2. Flask geliştirme sunucusunu çalıştırın:
   ```bash
   python app.py
   ```
3. Tarayıcınızda `http://127.0.0.1:5000` adresine giderek bir görüntü yükleyin ve konum detaylarını görün.

## Dizin Yapısı
```
/project-directory
    /uploads             # Yüklenmiş görüntüler için geçici depolama alanı
    app.py               # Ana Flask uygulama dosyası
    /templates
        index.html       # Ana sayfa şablonu
        result.html      # Görüntü analizi sonuçlarını gösteren şablon
    /static
        style.css         # Opsiyonel stil dosyası
    requirements.txt      # Python bağlımlıkları listesi
```

## Sorun Giderme
- Google API anahtarlarınızın ve kimlik bilgilerinizin doğru bir şekilde ayarlandığından emin olun.
- Uygulama konum tespiti yapamazsa, görüntünün net bir metin veya tanınabilir bir yer işareti içerdiğinden emin olun.

## Lisans
Bu proje MIT Lisansı altında lisanslanmıştır - detaylar için [LICENSE](LICENSE) dosyasına bakın.

