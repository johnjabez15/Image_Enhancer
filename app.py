from flask import Flask, render_template, request, send_file
import os
import cv2
from PIL import Image
import numpy as np
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ENHANCED_FOLDER = 'enhanced'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ENHANCED_FOLDER, exist_ok=True)

def enhance_image(image_path):
    img = cv2.imread(image_path)
    enhanced = cv2.detailEnhance(img, sigma_s=10, sigma_r=0.15)
    filename = f"enhanced_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
    enhanced_path = os.path.join(ENHANCED_FOLDER, filename)
    cv2.imwrite(enhanced_path, enhanced)
    return enhanced_path

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        img = request.files['image']
        if img:
            path = os.path.join(UPLOAD_FOLDER, img.filename)
            img.save(path)
            enhanced_path = enhance_image(path)
            return render_template('index.html', enhanced_image=enhanced_path)
    return render_template('index.html', enhanced_image=None)

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(ENHANCED_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
