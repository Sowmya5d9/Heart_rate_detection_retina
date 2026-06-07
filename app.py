from flask import Flask, render_template, Response, jsonify
import cv2
import numpy as np
import time

from modules.eye_detector import EyeDetector
from modules.blink_detector import BlinkDetector
from modules.retina_signal import RetinaSignal
from modules.frequency_analyzer import FrequencyAnalyzer
from modules.heart_rate import HeartRateEstimator

app = Flask(__name__)

camera_running = False
cap = None

metrics = {
    "eye_status": "Not Detected",
    "blink_count": 0,
    "frequency": "N/A",
    "heart_rate": "N/A",
    "processing": "Paused"
}


def generate_frames():

    global cap
    global camera_running
    global metrics

    eye_detector = EyeDetector()
    blink_detector = BlinkDetector()
    retina_signal = RetinaSignal(max_samples=120)
    frequency_analyzer = FrequencyAnalyzer()
    heart_rate_estimator = HeartRateEstimator()

    while True:

        if not camera_running:

            metrics["eye_status"] = "Not Detected"
            metrics["frequency"] = "N/A"
            metrics["heart_rate"] = "N/A"
            metrics["processing"] = "Paused"

            heart_rate_estimator.reset()

            blank = np.zeros(
                (480, 640, 3),
                dtype=np.uint8
            )

            cv2.putText(
                blank,
                "Camera Stopped",
                (180, 240),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2
            )

            ret, buffer = cv2.imencode(
                ".jpg",
                blank
            )

            frame = buffer.tobytes()

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n"
                + frame +
                b"\r\n"
            )

            time.sleep(0.05)
            continue

        ret, frame = cap.read()

        if not ret:
            continue

        frame = cv2.flip(frame, 1)

        detected, left_eye, right_eye = (
            eye_detector.detect_eyes(frame)
        )

        if detected and left_eye and right_eye:

            metrics["eye_status"] = "Detected"
            metrics["processing"] = "Running"

            ear, blink_count = (
                blink_detector.update(
                    left_eye,
                    right_eye
                )
            )

            metrics["blink_count"] = blink_count

            roi = retina_signal.extract_roi(
                frame,
                left_eye,
                right_eye
            )

            if roi is not None:

                success = (
                    retina_signal.update_signal(
                        roi
                    )
                )

                if success:

                    signal_buffer, time_buffer = (
                        retina_signal.get_signal()
                    )

                    if retina_signal.is_ready():

                        frequency = (
                            frequency_analyzer.analyze(
                                signal_buffer,
                                time_buffer
                            )
                        )

                        freq_text, hr_text = (
                            heart_rate_estimator.get_display_values(
                                frequency
                            )
                        )

                        metrics["frequency"] = freq_text
                        metrics["heart_rate"] = hr_text

                    else:

                        metrics["frequency"] = "Collecting..."
                        metrics["heart_rate"] = "Calculating..."

                else:

                    metrics["frequency"] = "N/A"
                    metrics["heart_rate"] = "N/A"

            else:

                metrics["frequency"] = "N/A"
                metrics["heart_rate"] = "N/A"

            for point in left_eye:

                cv2.circle(
                    frame,
                    point,
                    2,
                    (0, 255, 0),
                    -1
                )

            for point in right_eye:

                cv2.circle(
                    frame,
                    point,
                    2,
                    (0, 255, 0),
                    -1
                )

        else:

            metrics["eye_status"] = "Not Detected"
            metrics["frequency"] = "N/A"
            metrics["heart_rate"] = "N/A"
            metrics["processing"] = "Paused"

            retina_signal.reset()
            heart_rate_estimator.reset()

        ret, buffer = cv2.imencode(
            ".jpg",
            frame
        )

        frame_bytes = buffer.tobytes()

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + frame_bytes +
            b"\r\n"
        )


@app.route("/")
def home():

    return render_template(
        "index.html"
    )


@app.route("/video_feed")
def video_feed():

    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/metrics")
def get_metrics():

    return jsonify(metrics)


@app.route("/start_camera")
def start_camera():

    global cap
    global camera_running

    if cap is None:

        cap = cv2.VideoCapture(0)

        cap.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            640
        )

        cap.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            480
        )

    camera_running = True

    return jsonify({
        "status": "started"
    })


@app.route("/stop_camera")
def stop_camera():

    global cap
    global camera_running
    global metrics

    camera_running = False

    metrics["eye_status"] = "Not Detected"
    metrics["blink_count"] = 0
    metrics["frequency"] = "N/A"
    metrics["heart_rate"] = "N/A"
    metrics["processing"] = "Paused"

    if cap is not None:

        cap.release()
        cap = None

    return jsonify({
        "status": "stopped"
    })


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        threaded=True
    )