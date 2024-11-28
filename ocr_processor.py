import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import requests
import json
import base64
import io
import sys
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

def preprocess_image(image):
    print("Starting image preprocessing")  # Debug log
    opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    print("Converted to OpenCV format")  # Debug log
    
    gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
    print("Converted to grayscale")  # Debug log
    
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    print("Resized image")  # Debug log
    
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    gray = clahe.apply(gray)
    print("Applied CLAHE")  # Debug log
    
    denoised = cv2.fastNlMeansDenoising(gray)
    print("Applied denoising")  # Debug log
    
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharpened = cv2.filter2D(denoised, -1, kernel)
    print("Applied sharpening")  # Debug log
    
    height, width = sharpened.shape
    num_sections = 3
    section_width = width // num_sections
    result = np.zeros_like(sharpened)
    
    for i in range(num_sections):
        start = i * section_width
        end = start + section_width if i < num_sections-1 else width
        section = sharpened[:, start:end]
        threshold = cv2.threshold(section, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[0]
        section_binary = cv2.threshold(section, threshold, 255, cv2.THRESH_BINARY)[1]
        result[:, start:end] = section_binary
    
    print("Applied adaptive thresholding")  # Debug log
    
    kernel = np.ones((3,3),np.uint8)
    result = cv2.morphologyEx(result, cv2.MORPH_CLOSE, kernel)
    print("Applied morphological operations")  # Debug log
    
    result_pil = Image.fromarray(result)
    print("Converted back to PIL format")  # Debug log
    return result_pil

def extract_text(image):
    try:
        print("Starting OCR process")  # Debug log
        preprocessed = preprocess_image(image)
        print("Image preprocessing completed")  # Debug log
        
        # OCR yapılandırmasını değiştiriyoruz
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(preprocessed, config=custom_config)
        print("Raw OCR output:", repr(text))  # Debug log - ham çıktıyı gösterir
        
        cleaned_text = text.strip()
        print("Cleaned OCR output:", repr(cleaned_text))  # Debug log
        return cleaned_text
    except Exception as e:
        print("Error in extract_text:", str(e))  # Debug log
        return None

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/ocr', methods=['POST'])
def process_image():
    try:
        # Get base64 image from request
        data = request.get_json()
        print("Received data:", data)  # Debug log
        
        if not data or 'image' not in data:
            return jsonify({'error': 'No image data provided'}), 400

        # Decode base64 image
        try:
            image_data = base64.b64decode(data['image'])
            print("Successfully decoded base64")  # Debug log
            image = Image.open(io.BytesIO(image_data))
            print("Successfully opened image")  # Debug log
        except Exception as e:
            print("Error decoding image:", str(e))  # Debug log
            return jsonify({'error': 'Invalid image data: ' + str(e)}), 400

        # Process image and extract text
        result = extract_text(image)
        print("Extracted text:", result)  # Debug log
        
        if not result:
            return jsonify({
                'success': False,
                'error': 'No text extracted from image'
            }), 400
        
        return jsonify({
            'success': True,
            'text': result
        })
    except Exception as e:
        print("Error processing request:", str(e))  # Debug log
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
