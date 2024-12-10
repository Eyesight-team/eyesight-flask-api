from flask import Flask, jsonify, request
from google.cloud import firestore
from datetime import datetime

app = Flask(__name__)

FIRESTORE_CREDENTIALS = "./capstone-project-441604-4d88bad0e9e4.json"
db = firestore.Client.from_service_account_json(FIRESTORE_CREDENTIALS)

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
    tes_kelayakan = data.get('tes_kelayakan') 
    confidence_level = data.get('confidence_level') 

    if nama_barang is None or tes_kelayakan is None or confidence_level is None:
        return jsonify({"error": "Invalid input"}), 400

    status = "Lolos" if tes_kelayakan >= 70 and confidence_level >= 70 else "Tidak Lolos"

    prediction_data = {
        "nama_barang": nama_barang,
        "tes_kelayakan": tes_kelayakan,
        "confidence": confidence_level,
        "status": status,
        "processed_at": datetime.utcnow().isoformat()
    }

    prediction_id = save_prediction(prediction_data)

    return jsonify({"id": prediction_id, "result": prediction_data}), 201

@app.route('/predict/histories', methods=['GET'])
def get_histories():
    predictions = get_predictions()
    return jsonify(predictions), 200

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
