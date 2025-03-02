![KonumifyLogo](../static/konumify.png)

यह रिपॉजिटरी दो वर्शन की Flask एप्लिकेशन को शामिल करता है, जो Google Cloud सेवाओं का उपयोग करके छवि फ़ाइलों का विश्लेषण करता है और स्थान-आधारित जानकारी निकालता है। इन दोनों वर्शन के बीच मुख्य अंतर Places API का कार्यान्वयन है:

- `app.py`: Places API का उपयोग करता है।
- `appv2.py`: Places API (नया) का उपयोग करता है।

---

## विशेषताएँ

1. **छवि विश्लेषण**:
   - अपलोड की गई छवियों से EXIF मेटाडेटा निकालता है।
   - छवियों में टेक्स्ट का विश्लेषण करने के लिए OCR (ऑप्टिकल कैरेक्टर रिकॉग्निशन) करता है।
   - लैंडमार्क डिटेक्शन और वेब डिटेक्शन के लिए Google Cloud Vision API का उपयोग करता है।

2. **Google Places API एकीकरण**:
   - टेक्स्ट क्वेरी और कोऑर्डिनेट्स से स्थानों के बारे में विस्तृत जानकारी प्राप्त करता है।
   - `appv2.py` नए Places API एंडपॉइंट्स और विधियों को उच्च सटीकता के लिए अपनाता है।

3. **बहुभाषी समर्थन**:
   - तुर्की, अंग्रेज़ी, जर्मन, स्पेनिश, हिंदी, जापानी, डच, रूसी और चीनी भाषाएँ समर्थित हैं।
   - भाषा चयन Flask-Babel के माध्यम से प्रबंधित होता है।

4. **डायनेमिक सैटेलाइट मैप्स**:
   - Google Maps Static API का उपयोग करके पहचाने गए स्थानों के सैटेलाइट चित्र प्रदर्शित करता है।

---

## आवश्यकताएँ

### उपयोग की गई API

- [Google Cloud Vision API](https://cloud.google.com/vision/docs): छवि विश्लेषण के लिए।
- [Google Places API](https://developers.google.com/maps/documentation/places/web-service/choose-api):
  - [मानक संस्करण](https://developers.google.com/maps/documentation/places/web-service/search) `app.py`।
  - [नया संस्करण](https://developers.google.com/maps/documentation/places/web-service/op-overview) `appv2.py`।
- [Google Geocoding API](https://developers.google.com/maps/documentation/geocoding): कोऑर्डिनेट्स को पते में बदलने के लिए।
- [Google Maps Static API](https://developers.google.com/maps/documentation/maps-static): सैटेलाइट मैप चित्र बनाने के लिए।
- [Google Custom Engine ID](https://programmablesearchengine.google.com/controlpanel/all): कीवर्ड आधारित वेब खोजों के लिए।
  - सर्च इंजन का आईडी के लिए आवश्यक है (यानी CX मान)। "इमेज सर्च" और "पूरे वेब पर खोजें" को सक्षम होना चाहिए। "क्षेत्र" के लिए अपना देश अनुशंसित है।.

### पायथन लाइब्रेरीज़

इस प्रोजेक्ट के लिए निम्नलिखित लाइब्रेरीज़ की आवश्यकता है:

- `Flask`
- `Flask-Babel`
- `requests`
- `spacy`
- `google-cloud-vision`
- `Pillow`
- `python-dotenv`
- `Werkzeug`

---

## स्थापना

1. रिपॉजिटरी क्लोन करें:
   ```bash
   git clone https://github.com/yourusername/places-api-project.git
   cd places-api-project
   ```

2. निर्भरताएँ इंस्टॉल करें:
   ```bash
   pip install -r requirements.txt
   ```

3. en_core_web_sm मॉडल को इंस्टॉल करें:
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. अपनी Google Cloud क्रेडेंशियल्स सेट करें:
   - प्रोजेक्ट डायरेक्टरी में `.env` फ़ाइल बनाएं और निम्नलिखित कुंजियों को जोड़ें:
     ```env
     FLASK_SECRET_KEY=आपकी-गुप्त-कुंजी # flask_secret_key_maker.py का उपयोग करके बनाएँ
     GOOGLE_APPLICATION_CREDENTIALS=json-फ़ाइल-नाम.json
     GEOCODING_API_KEY=आपकी-API-KEY
     PLACES_API_KEY=${GEOCODING_API_KEY} # GEOCODING_API_KEY के समान
     CUSTOM_SEARCH_JSON_API=${GEOCODING_API_KEY} # GEOCODING_API_KEY के समान
     CUSTOM_SEARCH_ENGINE_ID=आपकी-सर्च-इंजन-का-आईडी
     ```

---

## उपयोग

1. एप्लिकेशन शुरू करें:
   ```bash
   python app.py  # Places API के लिए
   python appv2.py  # Places API (नया) के लिए
   ```

2. ब्राउज़र खोलें और `http://127.0.0.1:5000` पर जाएं।

3. एक छवि अपलोड करें और एप्लिकेशन को इसे विश्लेषण करने दें।

---

## निर्देशिका संरचना

```
places-api-project/
├── app.py            # Places API का मानक कार्यान्वयन
├── appv2.py          # Places API का नया कार्यान्वयन
├── templates/        # HTML टेम्पलेट्स फ़ोल्डर
├── translations/     # भाषा फ़ाइलों का फ़ोल्डर
├── static/           # स्थिर फ़ाइलों का फ़ोल्डर (CSS, छवियाँ)
├── uploads/          # अपलोड की गई छवियों के लिए अस्थायी फ़ोल्डर (स्वतः निर्मित, इसे स्वयं बनाने की आवश्यकता नहीं है)
├── .env              # पर्यावरण चर
├── requirements.txt  # पायथन लाइब्रेरीज़
```

---

## लाइसेंस

यह प्रोजेक्ट MIT लाइसेंस के तहत लाइसेंस प्राप्त है। अधिक जानकारी के लिए [LICENSE](LICENSE) फ़ाइल देखें।

---

## उदाहरण
![Konumifyफ़ोटो](https://i.imgur.com/ovvhnKq.jpeg)
![KonumifyIndex](https://i.imgur.com/2DP8HCz.png)
![Konumifyपरिणाम](https://i.imgur.com/DUHpuXp.png)
