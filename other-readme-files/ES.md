![LogotipoKonumify](../static/konumify.png)

Este repositorio contiene dos versiones de una aplicación Flask que utiliza los servicios de Google Cloud para analizar archivos de imagen y extraer información basada en ubicación. La principal diferencia entre las dos versiones es la implementación de la API de Places:

- `app.py`: Utiliza la API de Places.
- `appv2.py`: Utiliza la API de Places (Nueva).

---

## Características

1. **Análisis de imágenes**:
   - Extrae metadatos EXIF de las imágenes cargadas.
   - Realiza OCR (Reconocimiento Óptico de Caracteres) para analizar texto en las imágenes.
   - Utiliza la API Google Cloud Vision para detección de lugares emblemáticos y detección web.

2. **Integración con la API de Google Places**:
   - Recupera información detallada sobre ubicaciones a partir de consultas de texto y coordenadas.
   - `appv2.py` adopta los nuevos puntos finales y métodos de la API de Places para mayor precisión.

3. **Soporte multilingüe**:
   - La aplicación admite varios idiomas (turco, inglés, alemán, español, ruso).
   - La selección de idioma se gestiona mediante Flask-Babel.

4. **Mapas satelitales dinámicos**:
   - Muestra imágenes satelitales de las ubicaciones detectadas utilizando la API Google Maps Static.

---

## Requisitos

### APIs Utilizadas

- [Google Cloud Vision API](https://cloud.google.com/vision/docs): Para el análisis de imágenes.
- [Google Places API](https://developers.google.com/maps/documentation/places/web-service/choose-api):
  - [Versión estándar](https://developers.google.com/maps/documentation/places/web-service/search) `app.py`.
  - [Nueva versión](https://developers.google.com/maps/documentation/places/web-service/op-overview) `appv2.py`.
- [Google Geocoding API](https://developers.google.com/maps/documentation/geocoding): Para geocodificación inversa de coordenadas a direcciones.
- [Google Maps Static API](https://developers.google.com/maps/documentation/maps-static): Para generar imágenes de mapas satelitales.
- [Google Custom Search API](https://developers.google.com/custom-search/v1/introduction): Para búsquedas web basadas en palabras clave.

### Librerías de Python

Se requieren las siguientes librerías para este proyecto:

- `Flask`
- `Flask-Babel`
- `requests`
- `spacy`
- `google-cloud-vision`
- `Pillow`
- `python-dotenv`
- `Werkzeug`

---

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/yourusername/places-api-project.git
   cd places-api-project
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configura tus credenciales de Google Cloud:
   - Crea un archivo `.env` en el directorio del proyecto con las siguientes claves:
     ```env
     FLASK_SECRET_KEY=TU_CLAVE_SECRETA # Crear con flask_secret_key_maker.py
     GOOGLE_APPLICATION_CREDENTIALS=nombre-archivo-json.json
     GEOCODING_API_KEY=API_KEY
     PLACES_API_KEY=${GEOCODING_API_KEY} # Igual que GEOCODING_API_KEY
     CUSTOM_SEARCH_JSON_API=${GEOCODING_API_KEY} # Igual que GEOCODING_API_KEY
     ```

---

## Uso

1. Inicia la aplicación:
   ```bash
   python app.py  # Para API de Places
   python appv2.py  # Para API de Places (Nueva)
   ```

2. Abre un navegador y navega a `http://127.0.0.1:5000`.

3. Sube una imagen y deja que la aplicación la analice.

---

## Estructura del directorio

```
places-api-project/
├── app.py            # Implementación estándar de la API de Places
├── appv2.py          # Nueva implementación de la API de Places
├── templates/        # Carpeta de plantillas HTML
├── translations/     # Carpeta de archivos de idioma
├── static/           # Carpeta de archivos estáticos (CSS, imágenes)
├── uploads/          # Carpeta temporal para imágenes subidas (se genera automáticamente, no es necesario crearla manualmente)
├── .env              # Variables de entorno
├── requirements.txt  # Librerías de Python
```

---

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

## Contribuciones

¡Las contribuciones son bienvenidas! Siéntete libre de hacer un fork del repositorio, crear una rama para nuevas funciones y enviar un pull request.

## Ejemplo
![KonumifyFoto](https://i.ibb.co/mFTBnfm/GUELL.jpg)
![KonumifyIndex](https://i.ibb.co/YcvdcZf/1-es.png)
![KonumifyResultado](https://i.ibb.co/0nW2XsZ/2-es.png)
