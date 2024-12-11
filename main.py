from flask import Flask, jsonify, request
from google.cloud import firestore
from datetime import datetime
import requests

app = Flask(__name__)

FIRESTORE_CREDENTIALS = "./capstone-project-441604-4d88bad0e9e4.json"
db = firestore.Client.from_service_account_json(FIRESTORE_CREDENTIALS)

JETSON_URL = "http://<jetson-ip-address>:<port>/predict" #waiting for Jetson URL

def save_prediction(data):
    
    doc_ref = db.collection('predictions').document()
    data['id'] = doc_ref.id 
    doc_ref.set(data)
    return doc_ref.id

def get_predictions():
    predictions = db.collection('predictions').stream()
    results = []
    for doc in predictions:
        data = doc.to_dict()
        data['id'] = doc.id  
        results.append(data)
    return results

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    nama_barang = data.get('nama_barang')
    
    if nama_barang is None:
        return jsonify({"error": "Invalid input"}), 400

    try:
        jetson_response = requests.post(JETSON_URL, json=data)
        jetson_response.raise_for_status()  
        jetson_result = jetson_response.json()

        tes_kelayakan = jetson_result.get('tes_kelayakan')
        confidence_level = jetson_result.get('confidence_level')

        if tes_kelayakan is None or confidence_level is None:
            return jsonify({"error": "Invalid response from Jetson"}), 500

        status = "Lolos" if tes_kelayakan >= 70 and confidence_level >= 70 else "Tidak Lolos"

        prediction_data = {
            "nama_barang": nama_barang,
            "tes_kelayakan": tes_kelayakan,
            "confidence_level": confidence_level,
            "status": status,
            "processed_at": datetime.utcnow().isoformat()
        }

        prediction_id = save_prediction(prediction_data)

        return jsonify({"id": prediction_id, "result": prediction_data}), 201

    except request.RequestException as e:
        return jsonify({"error": f"Failed to connect to Jetson: {str(e)}"}), 500

@app.route('/predict/histories', methods=['GET'])
def get_histories():
    predictions = get_predictions()
    return jsonify(predictions), 200

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
