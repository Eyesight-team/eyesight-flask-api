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
# Konfigurasi upload
UPLOADS_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
# Buat folder uploads jika belum ada
if not os.path.exists(UPLOADS_FOLDER):
    os.makedirs(UPLOADS_FOLDER)
# Muat model TensorFlow Lite
interpreter = tf.lite.Interpreter(model_path='Fruits-fp16.tflite')
interpreter.allocate_tensors()
# Muat label
labels = [line.strip() for line in open('labels.txt')]
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
# Fungsi untuk melakukan prediksi
def predict_image(image_path):
    # Muat gambar
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (640, 640))
    # Ubah tipe data gambar ke FLOAT32
    img = img / 255.0
    img = img.astype(np.float32)
    # Lakukan prediksi
    input_tensor = interpreter.get_input_details()[0]['index']
    interpreter.set_tensor(input_tensor, [img])
    interpreter.invoke()
    # Dapatkan output
    output_details = interpreter.get_output_details()
    output = interpreter.get_tensor(output_details[0]['index'])
    # Proses output
    boxes = output[0][:, :4]  # Koordinat bounding box
    scores = output[0][:, 4:5]  # Skor kepercayaan
    classes = output[0][:, 5:]  # Kelas objek
    # Tampilkan hasil prediksi
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
# Route untuk prediksi gambar
@app.route('/predict', methods=['POST'])
def predict():
    doc_ref = store.collection(u'predictions')
    # Cek apakah file terkirim
    if 'image' not in request.files:
        return jsonify({"error": "Tidak ada file terkirim"}), 400
    file = request.files['image']
    # Cek apakah file kosong
    if file.filename == "":
        return jsonify({"error": "File kosong"}), 400
    # Cek ekstensi file
    if not allowed_file(file.filename):
        return jsonify({"error": "Ekstensi file tidak didukung"}), 400
    # Simpan file ke folder uploads
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOADS_FOLDER, filename)
    file.save(filepath)
    # Lakukan prediksi
    results = predict_image(filepath)
    if(results['confidence'] > 70):
        results['status'] = 'lolos'
    else:
        results['status'] = 'tidak lolos'
    doc_ref.add(results)
    # Hapus file setelah diproses
    os.remove(filepath)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)