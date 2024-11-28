# OCR Service

Bu servis, base64 formatında kodlanmış resimleri alıp OCR (Optical Character Recognition) işlemi yaparak metne dönüştüren bir web servisidir.

## Gereksinimler

- Python 3.9+
- Tesseract OCR
- Virtual Environment (venv)

## Kurulum

1. Tesseract OCR'ı yükleyin (macOS için):
```bash
brew install tesseract
```

2. Projeyi klonlayın ve dizine gidin:
```bash
cd /path/to/ocr_assistant
```

3. Virtual environment oluşturun ve aktive edin:
```bash
python -m venv .venv
source .venv/bin/activate
```

4. Gerekli Python paketlerini yükleyin:
```bash
pip install flask flask-cors opencv-python pytesseract pillow numpy
```

## Çalıştırma

1. Virtual environment'ı aktive edin (eğer aktif değilse):
```bash
source .venv/bin/activate
```

2. Flask uygulamasını başlatın:
```bash
python ocr_processor.py
```

Servis http://localhost:8080 adresinde çalışmaya başlayacaktır.

## Kullanım

### Web Arayüzü ile Kullanım

1. Web tarayıcınızda http://localhost:8080 adresine gidin
2. Base64 formatındaki resim kodunu metin kutusuna yapıştırın
3. "Process Image" butonuna tıklayın
4. OCR sonucu sayfada görüntülenecektir

### API ile Kullanım

POST isteği yaparak servisi kullanabilirsiniz:

```bash
curl -X POST http://localhost:8080/ocr \
-H "Content-Type: application/json" \
-d '{"image": "base64_encoded_image_string"}'
```

### Örnek Yanıt

Başarılı durumda:
```json
{
    "success": true,
    "text": "extracted_text"
}
```

Hata durumunda:
```json
{
    "success": false,
    "error": "error_message"
}
```

## Notlar

- Base64 kodlu resim verisi saf base64 string olmalıdır (örn: "data:image/png;base64," öneki olmadan)
- OCR işlemi için Tesseract kullanılmaktadır
- Servis varsayılan olarak 8080 portunda çalışır
