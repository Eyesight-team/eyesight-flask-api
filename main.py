import os
from flask import Flask, request, jsonify
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)


cred = credentials.Certificate("./key.json")
firebase_admin.initialize_app(cred)
store = firestore.client()

@app.route('/predict', methods=['POST'])
def post_predict():
    try:
        input_data = request.get_json()
        
        #dummy
        #jetson_response = {
        #    "label": "apple",
        #    "confidence": 0.85,
        #}

        prediction_result = {
            "id": os.urandom(8).hex(),
            "label": jetson_response["label"],
            "confidence": jetson_response["confidence"],
            "status": "Lolos" if jetson_response["confidence"] > 0.7 else "Tidak Lolos",
            "timestamp": datetime.now().isoformat(),
            "device": "Jetson Nano",
        }

        store.collection('predictions').add(prediction_result)

        return jsonify(prediction_result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/predict', methods=['GET'])
def get_predict():
    try:
        # Ambil data dari request
        #input_data = request.get_json()

        # Kirim permintaan ke Jetson (ganti `JETSON_URL` dengan URL Jetson)
        #JETSON_URL = "http://<JETSON_IP>:<PORT>/predict"
        # jetson_response = requests.post(JETSON_URL, json=input_data).json()

        #dummy test
        #jetson_response = {
        #    "label": "apple",
        #    "confidence": 0.85,
        #}

        prediction_result = {
            "id": os.urandom(8).hex(),
            "label": jetson_response["label"],
            "confidence": jetson_response["confidence"],
            "status": "Lolos" if jetson_response["confidence"] > 0.7 else "Tidak Lolos",
            "timestamp": datetime.now().isoformat(),
            "device": "Jetson Nano",
        }

        return jsonify(prediction_result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/predict/histories', methods=['GET'])
def get_histories():
    try:

        predictions_ref = store.collection('predictions')
        docs = predictions_ref.stream()

        histories = []
        for doc in docs:
            history = doc.to_dict()
            history['id'] = doc.id 
            histories.append(history)

        return jsonify(histories), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return "Service is running!"

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
