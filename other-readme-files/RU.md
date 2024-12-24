![ЛоготипKonumify](../static/konumify.png)

Этот репозиторий содержит две версии приложения Flask, которое использует сервисы Google Cloud для анализа изображений и извлечения информации, связанной с местоположением. Основное различие между двумя версиями заключается в реализации API Places:

- `app.py`: Использует API Places.
- `appv2.py`: Использует API Places (новая версия).

---

## Возможности

1. **Анализ изображений**:
   - Извлекает метаданные EXIF из загруженных изображений.
   - Выполняет OCR (оптическое распознавание символов) для анализа текста на изображениях.
   - Использует API Google Cloud Vision для обнаружения достопримечательностей и анализа веб-данных.

2. **Интеграция с API Google Places**:
   - Получает подробную информацию о местах из текстовых запросов и координат.
   - `appv2.py` использует новые конечные точки и методы API Places для повышения точности.

3. **Многоязычная поддержка**:
   - Приложение поддерживает несколько языков (турецкий, английский, немецкий, испанский, русский).
   - Выбор языка осуществляется через Flask-Babel.

4. **Динамические спутниковые карты**:
   - Отображает спутниковые изображения обнаруженных мест с помощью API Google Maps Static.

---

## Требования

### Используемые API

- [Google Cloud Vision API](https://cloud.google.com/vision/docs): Для анализа изображений.
- [Google Places API](https://developers.google.com/maps/documentation/places/web-service/choose-api):
  - [Стандартная версия](https://developers.google.com/maps/documentation/places/web-service/search) `app.py`.
  - [Новая версия](https://developers.google.com/maps/documentation/places/web-service/op-overview) `appv2.py`.
- [Google Geocoding API](https://developers.google.com/maps/documentation/geocoding): Для обратного геокодирования координат в адреса.
- [Google Maps Static API](https://developers.google.com/maps/documentation/maps-static): Для создания спутниковых изображений карт.
- [Google Custom Search API](https://developers.google.com/custom-search/v1/introduction): Для поиска в интернете по ключевым словам.

### Библиотеки Python

Для этого проекта необходимы следующие библиотеки:

- `Flask`
- `Flask-Babel`
- `requests`
- `spacy`
- `google-cloud-vision`
- `Pillow`
- `python-dotenv`
- `Werkzeug`

---

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/yourusername/places-api-project.git
   cd places-api-project
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Настройте учетные данные Google Cloud:
   - Создайте файл `.env` в каталоге проекта с следующими ключами:
     ```env
     FLASK_SECRET_KEY=ВАШ_СЕКРЕТНЫЙ_КЛЮЧ # Создайте с помощью flask_secret_key_maker.py
     GOOGLE_APPLICATION_CREDENTIALS=json-файл-имя.json
     GEOCODING_API_KEY=API_KEY
     PLACES_API_KEY=${GEOCODING_API_KEY} # Совпадает с GEOCODING_API_KEY
     CUSTOM_SEARCH_JSON_API=${GEOCODING_API_KEY} # Совпадает с GEOCODING_API_KEY
     ```

---

## Использование

1. Запустите приложение:
   ```bash
   python app.py  # Для API Places
   python appv2.py  # Для API Places (новая версия)
   ```

2. Откройте браузер и перейдите по адресу `http://127.0.0.1:5000`.

3. Загрузите изображение и позвольте приложению его проанализировать.

---

## Структура каталога

```
places-api-project/
├── app.py            # Реализация стандартного API Places
├── appv2.py          # Реализация нового API Places
├── templates/        # Папка HTML-шаблонов
├── translations/     # Папка языковых файлов
├── static/           # Папка статических файлов (CSS, изображения)
├── uploads/          # Временная папка для загруженных изображений (создается автоматически, не нужно создавать вручную)
├── .env              # Переменные окружения
├── requirements.txt  # Библиотеки Python
```

---

## Лицензия

Этот проект лицензирован по лицензии MIT. Подробнее см. в файле [LICENSE](LICENSE).

---

## Вклад

Приветствуются любые вклады! Не стесняйтесь форкнуть репозиторий, создать ветку для новой функции и отправить pull request.

## Пример
![ФотографияKonumify](https://i.ibb.co/R7srhNY/REDSQ.jpg)
![KonumifyIndex](https://i.ibb.co/dpnTRRh/1-ru.png)
![РезультатKonumify](https://i.ibb.co/NyYfvMF/2-ru.png)
