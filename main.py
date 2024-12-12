import os
from flask import Flask, request, jsonify
import tensorflow as tf
import cv2  # type: ignore
import numpy as np
from werkzeug.utils import secure_filename

import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

cred = credentials.Certificate("./key.json")
firebaseapp = firebase_admin.initialize_app(cred)
store = firestore.client()

UPLOADS_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

if not os.path.exists(UPLOADS_FOLDER):
    os.makedirs(UPLOADS_FOLDER)
    
interpreter = tf.lite.Interpreter(model_path='Fruits-fp16.tflite')
interpreter.allocate_tensors()

labels = [line.strip() for line in open('labels.txt')]
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def predict_image(image_path):

    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (640, 640))

    img = img / 255.0
    img = img.astype(np.float32)

    input_tensor = interpreter.get_input_details()[0]['index']
    interpreter.set_tensor(input_tensor, [img])
    interpreter.invoke()

    output_details = interpreter.get_output_details()
    output = interpreter.get_tensor(output_details[0]['index'])

    boxes = output[0][:, :4]  # Koordinat bounding box
    scores = output[0][:, 4:5]  # Skor kepercayaan
    classes = output[0][:, 5:]  # Kelas objek

    results = []
    for i in range(len(scores)):
        if scores[i] > 0.5:
            class_id = int(classes[i][0])
            label = labels[class_id]
            confidence = scores[i][0] * 100
            results.append({
                "label": label,
                "confidence": confidence
            })
    if results:
        max_confidence = max(results, key=lambda x: x['confidence'])
        return max_confidence
    else:
        return []

@app.route('/predict', methods=['POST'])
def predict():
    doc_ref = store.collection(u'predictions')

    # Access the camera
    cap = cv2.VideoCapture(0) 

    if not cap.isOpened():
        return jsonify({"error": "Gagal membuka kamera"}), 400

    ret, frame = cap.read()
    if not ret:
        return jsonify({"error": "Gagal menangkap gambar"}), 400

    filename = "temp_image.jpg"
    cv2.imwrite(filename, frame)

    results = predict_image(filename)
    if results and results['confidence'] > 70:
        results['status'] = 'Lolos'
    else:
        results['status'] = 'Tidak Lolos'

    results['timestamp'] = datetime.now().isoformat()

    doc_ref.add(results)

    os.remove(filename)

    cap.release()
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
