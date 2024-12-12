# Flask API with TensorFlow Lite

This project sets up a Flask API that uses a TensorFlow Lite model to make predictions based on uploaded images. The model used in this project is `Fruits-fp16.tflite`, and it classifies various types of fruits.

## Prerequisites

Before you begin, make sure you have the following installed on your system:

- Python 3.8 or higher
- pip (Python package installer)

## Setup Instructions

### 1. Clone the Repository

Clone this repository to your local machine:

```bash
    git clone url
```

### 2. install dependency

Clone this repository to your local machine:

```bash
    pip install -r requirements.txt
```

### 3. Run the app flask !

Clone this repository to your local machine:

```bash
    python main.py
```

### Api Documentations

``` http
url    :  http://localhost:5000/predict
method :  post
body (form data) : file

```


