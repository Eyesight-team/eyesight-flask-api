from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
import requests

app = Flask(__name__)

cred = credentials.Certificate("./capstone-project-441604-4d88bad0e9e4.json")
initialize_app(cred)
db = firestore.client()

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    camera_device = data.get("camera_device", "")

    jetson_response = requests.post("http://jetson-endpoint/predict", json={"camera_device": camera_device})
    jetson_data = jetson_response.json()

    item_name = jetson_data.get("item_name")
    confidence_level = jetson_data.get("confidence_level")

    status = "Lolos" if confidence_level > 70 else "Tidak Lolos"

    prediction_data = {
        "id": data.get("id"),
        "nama_barang": item_name,
        "confidence_level": confidence_level,
        "status": status,
        "timestamp": firestore.SERVER_TIMESTAMP
    }

    db.collection("predictions").add(prediction_data)

    return jsonify(prediction_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
