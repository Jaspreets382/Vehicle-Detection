# Flask Object Detection Service

This repository contains a lightweight Flask-based web service for running object detection/model inference using Yolov4/5 files. It serves a simple HTML frontend and provides endpoints for uploading or processing video/imagery.

## 🚀 Features

- Python/Flask application (`app.py`/`app1.py`)
- Static assets (`static/` with CSS, JavaScript, and images)
- HTML templates for user interaction
- Pre-trained model files (`yolov4.weights`, `yolov4.cfg`, `yolov5s.pt`)
- Support for video processing stored under `videos/`

## 🛠️ Prerequisites

- Python 3.8+ (Windows environment shown)
- `pip` for dependency installation

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Jaspreets382/Vehicle-Detection.git flask_project
   cd flask_project
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate    # Windows
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt  # create this file with needed libraries
   ```

> ⚠️ **Note:** The actual `requirements.txt` is not included in the repo; you will need to generate it with the dependencies you use (Flask, OpenCV, torch, etc.).

## 🧠 Usage

Run the Flask server:
```bash
python app1.py runserver
```

Then open your browser at `http://127.0.0.1:5000/` to access the web interface.

The application allows you to upload or process media and returns detection results based on YOLO models.

## 🗂️ Project Structure

```
flask_project/
├── app.py            # main Flask application (older?)
├── app1.py           # current entry point
├── static/           # CSS, JS, images
├── templates/        # HTML templates
├── videos/           # store or process video files
├── yolov4.cfg
├── yolov4.weights
└── yolov5s.pt
```

## 🔐 Security & .gitignore

Large models, weights, and any sensitive files (e.g. `.env`) are ignored via `.gitignore`. Ensure you don’t commit them accidentally.

## 📄 License

This project is open source; 

## ✨ Contributions

Feel free to fork, modify, or extend the service. Submit pull requests or open issues for improvements.

