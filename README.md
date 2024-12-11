# **Eyesight Flask API Documentation**
**_Giving Prediction From Jetson_**

## Installation
1. Clone this repository <br>
   `git clone https://github.com/Eyesight-team/eyesight-flask-api.git`
3. Install required dependencies <br>
   `pip install -r requirements.txt`
4. Set up Firestore credentials 
5. Update the Jetson URL<br>
   `JETSON_URL = "http://<jetson-ip-address>:<port>/predict"`

### The Flask API running on
`http://127.0.0.1:8080`

## API Endpoints
### POST /predict
<pre>
{
    "id": "prediction-id",
    "result": {
        "nama_barang": "nama_barang",
        "tes_kelayakan": "tes_kelayakan",
        "confidence_level": "confidence_level",
        "status": "status",
        "processed_at": datetime.utcnow().isoformat()
    }
}
</pre>

### GET /predict/histories
<pre>
  [
    {
        "id": "prediction-id",
        "nama_barang": "nama_barang",
        "tes_kelayakan": "tes_kelayakan",
        "confidence_level": "confidence_level",
        "status": "status",
        "processed_at": datetime.utcnow().isoformat()
    },
    ...
]
</pre>

## Deploy on Google Cloud Run
