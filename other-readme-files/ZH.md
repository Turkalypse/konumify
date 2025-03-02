![Konumify标志](../static/konumify.png)

本仓库包含两个版本的 Flask 应用程序，采用谷歌云服务分析图像文件，并提取基于位置的信息。两个版本的主要区别是 Places API 的实现方式：

- `app.py`：使用 Places API。
- `appv2.py`：使用 Places API (新版)。

---

## 功能

1. **图像分析**：
   - 提取上传图像中的 EXIF 充足数据。
   - 采用 OCR (光学实物识别) 分析图像文本。
   - 使用 Google Cloud Vision API 进行地标检测和网络检测。

2. **Google Places API 集成**：
   - 通过文本查询和坐标提取地点详细信息。
   - `appv2.py` 采用新的 Places API 终端点和方法，提高准确性。

3. **多语言支持**：
   - 支持土耳其语、英语、德语、西班牙语、印地语、日语、荷兰语、俄语和中文。
   - 语言选择通过 Flask-Babel 进行处理。

4. **动态卫星地图**：
   - 使用 Google Maps Static API 显示检测到地点的卫星图像。

---

## 要求

### 使用的 API

- [Google Cloud Vision API](https://cloud.google.com/vision/docs)：用于图像分析。
- [Google Places API](https://developers.google.com/maps/documentation/places/web-service/choose-api):
  - [标准版](https://developers.google.com/maps/documentation/places/web-service/search) `app.py`。
  - [新版](https://developers.google.com/maps/documentation/places/web-service/op-overview) `appv2.py`。
- [Google Geocoding API](https://developers.google.com/maps/documentation/geocoding): 用于将坐标反向解释为地址。
- [Google Maps Static API](https://developers.google.com/maps/documentation/maps-static): 用于生成卫星地图图像。
- [Google Custom Engine ID](https://programmablesearchengine.google.com/controlpanel/all): 用于基于关键词的网络搜索。
  - 需要搜索引擎 ID（即 CX 值）。必须启用“图片搜索”和“在整个网络中搜索”。建议选择“区域”为土耳其。

### 必需的 Python 库

本项目需要以下库：

- `Flask`
- `Flask-Babel`
- `requests`
- `spacy`
- `google-cloud-vision`
- `Pillow`
- `python-dotenv`
- `Werkzeug`

---

## 安装

1. 克隆仓库：
   ```bash
   git clone https://github.com/yourusername/places-api-project.git
   cd places-api-project
   ```

2. 安装依赖项：
   ```bash
   pip install -r requirements.txt
   ```

3. 安装 en_core_web_sm 模型:
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. 设置 Google Cloud 凭资凭证：
   - 在项目目录中创建 `.env` 文件，含有以下键：
     ```env
     FLASK_SECRET_KEY=你的秘密密钥 # 通过 flask_secret_key_maker.py 创建
     GOOGLE_APPLICATION_CREDENTIALS=文件名.json
     GEOCODING_API_KEY=API_KEY
     PLACES_API_KEY=${GEOCODING_API_KEY} # 与 GEOCODING_API_KEY 相同
     CUSTOM_SEARCH_JSON_API=${GEOCODING_API_KEY} # 与 GEOCODING_API_KEY 相同
     CUSTOM_SEARCH_ENGINE_ID=您的搜索引擎-ID
     ```

---

## 使用

1. 启动应用程序：
   ```bash
   python app.py  # 使用 Places API
   python appv2.py  # 使用 Places API (新版)
   ```

2. 打开浏览器，进入 `http://127.0.0.1:5000`。

3. 上传图像，应用程序将分析图像。

---

## 目录结构

```
places-api-project/
├─ app.py            # 标准 Places API 实现
├─ appv2.py          # 新 Places API 实现
├─ templates/        # HTML 模板文件夹
├─ translations/     # 语言文件夹
├─ static/           # 静态文件夹 (CSS，图像)
├─ uploads/          # 上传图像的临时文件夹 (自动生成，无需自行创建)
├─ .env              # 环境变量
├─ requirements.txt  # Python 库
```

---

## 许可证

本项目按 MIT 许可证进行授权。详情见 [LICENSE](LICENSE) 文件。

---

## 示例
![Konumify照片](https://i.imgur.com/BIvAe3F.jpeg)
![KonumifyIndex](https://i.imgur.com/58vIn6K.png)
![Konumify结果](https://i.imgur.com/D5uTudX.png)
