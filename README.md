# Heart Rate Detection Using Retina and Eye Blinking Analysis

## Output Screenshot

![Output Screenshot](Screenshots/image.png)

## Project Overview

This project is a real-time Computer Vision application developed using Python, OpenCV, and MediaPipe. The system focuses on the eye region and analyzes retinal intensity variations to estimate heart rate while simultaneously monitoring eye blinking activity.

The application continuously detects both eyes using MediaPipe Face Mesh and extracts a Region of Interest (ROI) around the eye area. Signal processing techniques such as filtering and frequency analysis are applied to estimate physiological frequency and heart rate.

The system strictly follows safety conditions by stopping all calculations whenever the eyes are not detected.

## Features

* Real-time webcam monitoring
* Eye detection using MediaPipe Face Mesh
* Eye landmark tracking
* Retina Region of Interest (ROI) extraction
* Blink detection using Eye Aspect Ratio (EAR)
* Frequency estimation using signal processing
* Heart rate estimation in BPM
* Automatic reset when eyes are not detected
* Flask-based web interface
* Real-time dashboard updates

## Dashboard Metrics

The system displays:

* Eye Status
* Blink Count
* Frequency (Hz)
* Heart Rate (BPM)

When eyes are not detected:

* Eye Status = Not Detected
* Frequency = N/A
* Heart Rate = N/A

## Technologies Used

* Python
* Flask
* OpenCV
* MediaPipe
* NumPy
* SciPy
* HTML
* CSS
* JavaScript

## Project Structure

```text
Heart_rate_detection_retina/
│
├── app.py
├── requirements.txt
├── README.md
│
├── modules/
│   ├── eye_detector.py
│   ├── blink_detector.py
│   ├── retina_signal.py
│   ├── frequency_analyzer.py
│   └── heart_rate.py
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── dashboard.js
│
└── Screenshots/
    └── image.png
```

## Installation

```bash
pip install -r requirements.txt
```

## Run Project

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

in your browser.

## Future Enhancements

* Improved retinal signal extraction
* Advanced motion compensation
* Better illumination normalization
* Graph visualization of physiological signals
* Improved heart-rate estimation accuracy

## Author

Sowmya Arigila
B.Tech Computer Science
