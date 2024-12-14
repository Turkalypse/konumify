# ![KonumifyLogosu](https://i.ibb.co/f1FJgSF/konumifywhite.png)

Bu proje, EXIF meta verileri, OCR (Optik Karakter Tanıma) ve Google API'leriyle birlikte görüntü analizi ve konum tespiti yapar.

## Projede kullanılan API'ler

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

### Paketleri yükleme
Gerekli paketleri aşağıdaki komutla yükleyebilirsiniz:

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

### Google Cloud kimlik bilgileri
Uygulamayı çalıştırmadan önce Google Cloud kimlik bilgilerinizi ayarladığınızdan emin olun:
1. Bir Google Cloud projesi oluşturun ve Vision API ile Geocoding API'yi etkinleştirin.
2. Google Cloud projeniz için JSON anahtar dosyasını indirin.
3. `GOOGLE_APPLICATION_CREDENTIALS` ortam değişkenini JSON anahtar dosyanızın yoluna ayarlayın:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credentials.json"
```

### Ortam değişkenleri
- `GOOGLE_APPLICATION_CREDENTIALS`: Google Cloud kimlik bilgileri dosyanızın yolu.
- `GEOCODING_API_KEY`: Google Geocoding API anahtarınız.
- `PLACES_API_KEY`: Google Places API anahtarı (Geocoding API anahtarıyla aynı olabilir).

## Başlatma
1. Depoyu cihazınıza klonlayın:
   ```bash
   git clone https://github.com/Turkalypse/konumify-test.git
   cd konumify
   ```
2. Başlatın:
   ```bash
   python app.py
   ```
3. Tarayıcınızda `http://127.0.0.1:5000` adresine giderek bir görüntü yükleyin ve konum detaylarını görün.

## Dizin yapısı
```
/project-directory
    /uploads             # Yüklenmiş görüntüler için geçici depolama alanı (otomatik oluşturulur)
    app.py               # Ana dosya
    /templates
        index.html       # Ana sayfa şablonu
        result.html      # Görüntü analizi sonuçlarını gösteren şablon
    /static
        style.css         # Stil dosyası
    requirements.txt      # Python paketleri listesi
```

## Sorun giderme
- Google API anahtarlarınızın ve kimlik bilgilerinizin doğru bir şekilde ayarlandığından emin olun.
- Uygulama henüz konum tespiti yapamayabilir ve benzerlik olduğu için yanlış konum tespiti yapabilir. Projem henüz yeni. İyileştirmeler zamanla yapılacaktır.
- Yakında 'nasıl kurulur ve nasıl kullanılır' gibisinden rehber videosu eklenecektir.

## Lisans
Bu proje MIT Lisansı altında lisanslanmıştır - detaylar için [LICENSE](LICENSE) dosyasına bakın.

## Örnek sonuç:

# ![KonumifyIndex](https://i.ibb.co/0CVZQNJ/image.jpg)
# ![KonumifyIndex](https://i.ibb.co/J5x6qzD/index.png)
# ![KonumifyResult](https://i.ibb.co/vBgcZbj/result.png)
