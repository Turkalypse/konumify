![KonumifyLogo](../static/konumify.png)

このリポジトリは、Google Cloud サービスを使用して画像ファイルを分析し、住所情報を抽出する Flask アプリケーションの 2 つのバージョンを含みます。両者の違いは Places API の実装にあります:

- `app.py`: Places API を使用します。
- `appv2.py`: Places API (新規) を使用します。

---

## 機能

1. **画像分析**:
   - アップロードされた画像から EXIF メタデータを抽出します。
   - 画像の文字を分析するために OCR (光学実践認識) を実行します。
   - Google Cloud Vision API を使用して地名の特定およびウェブ検出を行います。

2. **Google Places API インテグレーション**:
   - テキストクエリおよび座標から地域に関する詳細情報を収集します。
   - `appv2.py` は、新しい Places API のエンドポイントおよびメソッドを採用し、精度を向上させています。

3. **多言語サポート**:
   - トルコ語、英語、ドイツ語、スペイン語、ヒンディー語、日本語、オランダ語、ロシア語、中国語がサポートされています。
   - Flask-Babel を使用して言語選択を行います。

4. **動的サテライトマップ**:
   - Google Maps Static API を使用して、特定された場所のサテライト画像を表示します。

---

## 必要な削除要件

### 使用される API

- [Google Cloud Vision API](https://cloud.google.com/vision/docs): 画像分析用。
- [Google Places API](https://developers.google.com/maps/documentation/places/web-service/choose-api):
  - [標準版](https://developers.google.com/maps/documentation/places/web-service/search) `app.py`。
  - [新規](https://developers.google.com/maps/documentation/places/web-service/op-overview) `appv2.py`。
- [Google Geocoding API](https://developers.google.com/maps/documentation/geocoding): 座標から住所を逆コード化するために使用します。
- [Google Maps Static API](https://developers.google.com/maps/documentation/maps-static): サテライトマップ画像を作成するために使用します。
- [Google Custom Engine ID](https://programmablesearchengine.google.com/controlpanel/all): キーワードを使用したウェブ検索用。
  - 検索エンジン ID が必要です（つまり CX 値）。「画像検索」と「ウェブ全体を検索」を有効にしてください。「地域」にはご自身の国を推奨します。

### Python ライブラリ

以下のライブラリが必要です:

- `Flask`
- `Flask-Babel`
- `requests`
- `spacy`
- `google-cloud-vision`
- `Pillow`
- `python-dotenv`
- `Werkzeug`

---

## インストール

1. リポジトリをクローンします:
   ```bash
   git clone https://github.com/yourusername/places-api-project.git
   cd places-api-project
   ```

2. 依存関係をインストールします:
   ```bash
   pip install -r requirements.txt
   ```

3. en_core_web_sm モデルをインストールします:
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. Google Cloud の証明情報を構築します:
   - プロジェクトディレクトリに `.env` ファイルを作成し、以下のキーを記入します:
     ```env
     FLASK_SECRET_KEY=YOUR-SECRET-KEY # flask_secret_key_maker.py で作成
     GOOGLE_APPLICATION_CREDENTIALS=json-file-name.json
     GEOCODING_API_KEY=YOUR-API-KEY
     PLACES_API_KEY=${GEOCODING_API_KEY} # GEOCODING_API_KEY と同じ
     CUSTOM_SEARCH_JSON_API=${GEOCODING_API_KEY} # GEOCODING_API_KEY と同じ
     CUSTOM_SEARCH_ENGINE_ID=あなたの検索エンジン-ID
     ```

---

## 使用法

1. アプリケーションを起動します:
   ```bash
   python app.py  # Places API 用
   python appv2.py  # Places API (新規)
   ```

2. ブラウザを開き、`http://127.0.0.1:5000`にアクセスします。

3. 画像をアップロードし、アプリケーションに分析させます。

---

## ディレクトリ構成

```
places-api-project/
├── app.py            # 標準 Places API 実装
├── appv2.py          # 新 Places API 実装
├── templates/        # HTML テンプレートフォルダ
├── translations/     # 言語ファイルフォルダ
├── static/           # スタティックファイルフォルダ (CSS, 画像)
├── uploads/          # アップロードされた画像用の両時フォルダ (自動作成されるので自分で作成する必要はありません)
├── .env              # 環境変数
├── requirements.txt  # Python ライブラリ
```

---

## ライセンス

このプロジェクトは MIT ライセンスのもとにライセンスされています。詳細については [LICENSE](LICENSE) ファイルをご覧ください。

---

## サンプル
![Konumify写真](https://i.imgur.com/8hYtkvJ.jpeg)
![KonumifyIndex](https://i.imgur.com/W1WpAZ8.png)
![Konumify結果](https://i.imgur.com/kb7Bxo0.png)
