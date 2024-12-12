# **Eyesight Flask API Documentation**
**_Giving Prediction From Jetson_**

This project sets up a Flask API that uses a TensorFlow Lite model to make predictions based on uploaded images. The model used in this project is `Fruits-fp16.tflite`, and it classifies various types of fruits.

## Prerequisites

Before you begin, make sure you have the following installed on your system:

- Python 3.8 or higher
- pip (Python package installer)

## Setup Instructions
1. Clone this repository <br>
   `git clone https://github.com/Eyesight-team/eyesight-flask-api.git`
3. Install required dependencies <br>
   `pip install -r requirements.txt`
4. Set up Firestore credentials 

### The Flask API running on
`http://127.0.0.1:8080/predict`

## API Endpoints
### POST /predict
<pre>
{
    "id": "prediction-id",
    "result": {
        "label": "label",
        "confidence": "confidence",
        "status": "status",
        "timestamp": datetime.utcnow().isoformat()
    }
}
</pre>

### GET /predict/histories
<pre>
  [
    {
        "id": "prediction-id",
        "label": "label",
        "confidence": "confidence",
        "status": "status",
        "timestamp": datetime.utcnow().isoformat()
    },
    ...
]
</pre>

## Deploy on Google Cloud Run



