import numpy as np
import time
import cv2


class RetinaSignal:

    def __init__(self, max_samples=120):

        self.max_samples = max_samples

        self.signal_buffer = []
        self.time_buffer = []

    def extract_roi(self, frame, left_eye, right_eye):

        if left_eye is None or right_eye is None:
            return None

        points = left_eye + right_eye

        if len(points) == 0:
            return None

        h, w, _ = frame.shape

        x_min = max(min(p[0] for p in points) - 5, 0)
        y_min = max(min(p[1] for p in points) - 5, 0)

        x_max = min(max(p[0] for p in points) + 5, w)
        y_max = min(max(p[1] for p in points) + 5, h)

        if x_max <= x_min or y_max <= y_min:
            return None

        roi = frame[y_min:y_max, x_min:x_max]

        if roi.size == 0:
            return None

        return roi

    def normalize_roi(self, roi):

        try:

            roi = cv2.GaussianBlur(
                roi,
                (3, 3),
                0
            )

            roi = cv2.cvtColor(
                roi,
                cv2.COLOR_BGR2RGB
            )

            return roi

        except Exception:
            return roi

    def update_signal(self, roi):

        if roi is None:
            return False

        if roi.size == 0:
            return False

        roi = self.normalize_roi(roi)

        green_channel = roi[:, :, 1]

        green_mean = np.mean(green_channel)

        if np.isnan(green_mean):
            return False

        self.signal_buffer.append(float(green_mean))
        self.time_buffer.append(time.time())

        if len(self.signal_buffer) > self.max_samples:

            self.signal_buffer.pop(0)
            self.time_buffer.pop(0)

        return True

    def get_signal(self):

        return (
            self.signal_buffer.copy(),
            self.time_buffer.copy()
        )

    def reset(self):

        self.signal_buffer.clear()
        self.time_buffer.clear()

    def is_ready(self):

        # Reduced from 150
        # Allows faster BPM estimation

        return len(self.signal_buffer) >= 60

    def get_signal_quality(self):

        if len(self.signal_buffer) < 20:
            return 0

        signal = np.array(
            self.signal_buffer
        )

        return np.std(signal)