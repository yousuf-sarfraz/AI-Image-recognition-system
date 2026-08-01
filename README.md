# 🧠 AI Image Recognition System

An AI-powered web application built with **Python** and **Flask** that performs **object detection** and **Optical Character Recognition (OCR)** on uploaded images. The system uses **YOLOv8** to detect and classify objects, while **EasyOCR** extracts readable text from images. Users can upload an image through a modern, responsive web interface and instantly receive annotated detection results, extracted text, and confidence scores.

## ✨ Features

* 🖼️ Upload images through an intuitive web interface
* 🤖 Detect multiple objects using the YOLOv8 deep learning model
* 📝 Extract text from images using EasyOCR
* 🎯 Display object detection confidence scores
* 📄 Present OCR results in a clean and readable format
* 📱 Responsive design for desktop and mobile devices
* ⚡ Fast and efficient image processing

## 🛠️ Technologies Used

* Python
* Flask
* YOLOv8 (Ultralytics)
* EasyOCR
* OpenCV
* HTML5
* CSS3
* JavaScript

   ```

:
🏗️ System Architecture

* **Flask** manages the backend, routing, and application logic.
* **YOLOv8** detects and classifies objects in uploaded images.
* **EasyOCR** extracts text from images.
* **OpenCV** preprocesses images before analysis.
* **HTML, CSS, and JavaScript** provide a responsive and interactive user interface.

## 📄 License

This project is developed for educational and learning purposes.

---

This project demonstrates how modern computer vision and OCR technologies can be integrated into a practical web application for intelligent image analysis.
📁 Project Structure

AI-Image-Recognition-System/
│
├── app.py                  # Main Flask application
├── config.py               # Configuration settings
├── requirements.txt        # Project dependencies
├── README.md               # Project documentation
│
├── models/
│   └── yolov8n.pt          # YOLOv8 model weights
│
├── routes/
│   └── main.py             # Application routes
│
├── services/
│   ├── detector.py         # YOLO object detection
│   ├── ocr.py              # EasyOCR text extraction
│   ├── image_processor.py  # OpenCV image preprocessing
│   └── utils.py            # Helper functions
│
├── templates/
│   ├── index.html
│   ├── result.html
│   ├── about.html
│   └── layout.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── uploads/                # Uploaded images
└── results/                # Processed output images