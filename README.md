# Heart Rate Detection Using Retina and Eye Blinking Analysis
## Output Screenshot


![output Screenshot](Screenshots/image.png)



## Overview

This project is a real-time computer vision application that:

- Detects both eyes using MediaPipe Face Mesh
- Tracks eye landmarks
- Detects eye blinks using Eye Aspect Ratio (EAR)
- Extracts eye-region intensity signals
- Applies signal processing techniques
- Estimates dominant frequency
- Calculates Heart Rate (BPM)
- Displays N/A when eyes are not detected

## Features

- Real-time webcam monitoring
- Eye detection
- Blink counting
- Blink frequency calculation
- Frequency estimation
- Heart-rate estimation
- Automatic reset when eyes disappear

## Technologies

- Python
- OpenCV
- MediaPipe
- NumPy
- SciPy

## Installation

```bash
pip install -r requirements.txt

